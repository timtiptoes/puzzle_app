from flask import Flask, render_template, request, send_file, session, redirect, url_for
from flask import make_response
import os
import re
from functools import wraps, update_wrapper
from datetime import datetime
from model import InputForm
from puzzlegen import puzzlesheet
from puzzlegen import crosswordsheet
from utils import get_categories
from db import init_db, log_puzzle, get_log

app = Flask(__name__)
app.secret_key = 'ph#Kw9!mZqL2vXnR'
init_db()

_LOG_PASSWORD = os.environ['PUZZLE_PASSWORD']
_LOG_PER_PAGE = 25


def clue_filename(clue):
    unsafe = set('/\\:*?"<>|\0\'')
    safe = "".join(c for c in clue if c not in unsafe)
    return safe.strip().replace(" ", "_") + ".pdf"


def _latex_escape(s):
    chars = {'&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
             '_': r'\_', '{': r'\{', '}': r'\}',
             '~': r'\textasciitilde{}', '^': r'\textasciicircum{}',
             '\\': r'\textbackslash{}'}
    return ''.join(chars.get(c, c) for c in s)


def _generate_prize_slips(clues, prize_text):
    safe_prize = _latex_escape(prize_text)
    cols = 3
    spacing = 5.5  # cm between circle centers
    rows_tex = []
    for row_start in range(0, len(clues), cols):
        batch = clues[row_start:row_start + cols]
        nodes = []
        for j in range(len(batch)):
            num = row_start + j + 1
            safe_clue = _latex_escape(batch[j])
            nname = "N%d" % j
            nodes.append(
                "  \\node[draw=none, minimum width=5cm, minimum height=4cm,\n"
                "         inner sep=5pt, align=center, text width=3.5cm] (%s)\n"
                "    at (%.1fcm,0) {\\textbf{\\Large %d}\\\\[4pt]\\small %s\\\\[2pt]{\\fontsize{8}{9.6}\\selectfont %s}};\n"
                "  \\draw[decorate, line width=1.5pt] (%s.north west) rectangle (%s.south east);\n"
                % (nname, j * spacing, num, safe_prize, safe_clue, nname, nname)
            )
        rows_tex.append(
            "\\begin{center}\\begin{tikzpicture}"
            "[decoration={snake, amplitude=2.5pt, segment length=8pt}]\n"
            + "".join(nodes)
            + "\\end{tikzpicture}\\end{center}\n\\vspace{5mm}\n"
        )
    tex = (
        "\\documentclass{article}\n"
        "\\usepackage[a4paper,margin=0.75in]{geometry}\n"
        "\\usepackage{tikz}\n"
        "\\usetikzlibrary{decorations.pathmorphing}\n"
        "\\begin{document}\n"
        "\\pagenumbering{gobble}\n"
        + "".join(rows_tex)
        + "\\end{document}\n"
    )
    with open("tmp/prize_slips.tex", "wb") as f:
        f.write(tex.encode('utf-8'))
    os.system("pdflatex --interaction=nonstopmode --output-directory tmp tmp/prize_slips.tex")


def _generate_clue_list(clues):
    items = "\n".join("  \\item " + _latex_escape(clue) for clue in clues)
    tex = r"""\documentclass[12pt]{article}
\usepackage[a4paper,margin=1in]{geometry}
\begin{document}
\pagenumbering{gobble}
\begin{center}{\Large\textbf{Clue List}}\end{center}
\vspace{1em}
\large
\begin{enumerate}
""" + items + r"""
\end{enumerate}
\end{document}
"""
    with open("tmp/clue_list.tex", "wb") as f:
        f.write(tex.encode('utf-8'))
    os.system("pdflatex --interaction=nonstopmode --output-directory tmp tmp/clue_list.tex")


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


@app.route("/puzzle", methods=['GET', 'POST'])
def puzzle():
    categories = get_categories()
    form = InputForm(request.form)
    return render_template('view.html', form=form, my_categories=categories)


@app.route("/clue_ideas", methods=['GET'])
def clue_ideas():
    return render_template('clue_ideas.html')


def _build_instructions(puzzle_types):
    seen = set()
    instrs = []
    for pt in puzzle_types:
        instr = puzzlesheet.instructions_map.get(pt)
        if instr and instr not in seen:
            seen.add(instr)
            instrs.append(instr)
    return " $\\cdot$ ".join(instrs) or "Solve each problem to find the letter above"


def _generate_puzzle(clue, puzzle_types, instructions, number=None):
    slug = clue_filename(clue)[:-4] or "puzzle"
    sheet = puzzlesheet.puzzlesheet(slug, "", clue, savetex=True, number=number)
    sheet.add_section(puzzle_types, 6, "", instructions)
    sheet.write()
    log_puzzle(clue, "mixed: " + ", ".join(puzzle_types))
    return clue_filename(clue)


@app.route("/make_mixed_puzzle", methods=['POST'])
def make_mixed_puzzle():
    puzzle_types = request.form.getlist("puzzle_types")
    is_multi = request.form.get("multi_clue") == "1"
    raw = request.form.get("clue", "").strip()
    prize_text = request.form.get("prize_text", "").strip()
    if not raw or not puzzle_types:
        return redirect(url_for('puzzle'))
    instructions = _build_instructions(puzzle_types)
    if is_multi:
        lines = [l.strip() for l in raw.splitlines() if l.strip()][:50]
        results = []
        for i, clue in enumerate(lines):
            fname = _generate_puzzle(clue, puzzle_types, instructions, number=i + 1)
            results.append({'clue': clue, 'filename': fname})
        _generate_clue_list(lines)
        if prize_text:
            _generate_prize_slips(lines, prize_text)
        session['has_prize_slips'] = bool(prize_text)
        session['multi_results'] = results
        return redirect(url_for('multi_result'))
    else:
        clue = raw
        _generate_puzzle(clue, puzzle_types, instructions, number=1)
        if prize_text:
            _generate_prize_slips([clue], prize_text)
        session['has_prize_slips'] = bool(prize_text)
        session['last_clue'] = clue
        return redirect(url_for('puzzle_result'))


@app.route("/multi_result")
def multi_result():
    results = session.get('multi_results')
    if not results:
        return redirect(url_for('puzzle'))
    return render_template('multi_result.html', results=results,
                           has_prize_slips=session.get('has_prize_slips', False))


@app.route("/prize_slips")
@nocache
def get_prize_slips():
    path = os.path.join('tmp', 'prize_slips.pdf')
    if not os.path.exists(path):
        return "Not found", 404
    resp = send_file(path, mimetype='application/pdf')
    resp.headers['Content-Disposition'] = 'inline; filename="prize_slips.pdf"'
    return resp


@app.route("/clue_list")
@nocache
def get_clue_list():
    path = os.path.join('tmp', 'clue_list.pdf')
    if not os.path.exists(path):
        return "Not found", 404
    resp = send_file(path, mimetype='application/pdf')
    resp.headers['Content-Disposition'] = 'inline; filename="clue_list.pdf"'
    return resp


@app.route("/get_puzzle/<string:filename>")
@nocache
def get_puzzle(filename):
    if not re.match(r'^[\w\- ]+\.pdf$', filename):
        return "Invalid filename", 400
    path = os.path.join('tmp', os.path.basename(filename))
    if not os.path.exists(path):
        return "Not found", 404
    resp = send_file(path, mimetype='application/pdf')
    resp.headers['Content-Disposition'] = 'inline; filename="%s"' % filename
    return resp


@app.route("/puzzle_result")
def puzzle_result():
    clue = session.get('last_clue', 'puzzle')
    return render_template('result.html', clue=clue, filename=clue_filename(clue),
                           has_prize_slips=session.get('has_prize_slips', False))


@app.route("/current_puzzle")
@nocache
def current_puzzle():
    clue = session.get('last_clue', 'puzzle')
    filename = clue_filename(clue)
    path = os.path.join('tmp', filename)
    if not os.path.exists(path):
        return "Not found", 404
    resp = send_file(path, mimetype='application/pdf')
    resp.headers['Content-Disposition'] = 'inline; filename="%s"' % filename
    return resp


@app.route("/make_puzzle/<string:puzzle_type>")
def make_puzzle(puzzle_type):
    categories = get_categories()
    clue = request.args.get("clue", "").strip()
    if categories[puzzle_type]['type'] == 'math':
        sheet = puzzlesheet.puzzlesheet("puzzle", "", clue, savetex=True)
        puzz = categories[puzzle_type]['filename'].lower()
        sheet.add_section(puzz, 6, "", puzzlesheet.instructions_map[puzz], rhs=0)
        sheet.write()
    else:
        sheet = crosswordsheet.crossword1d(categories[puzzle_type]['filename'], title=puzzle_type, clue=clue, savetex=True)
        sheet.add_section()
        sheet.write()
    log_puzzle(clue, puzzle_type)
    session['last_clue'] = clue
    return redirect(url_for('puzzle_result'))


@app.route('/log/login', methods=['GET', 'POST'])
def log_login():
    error = None
    if request.method == 'POST':
        if request.form.get('password') == _LOG_PASSWORD:
            session['log_authed'] = True
            return redirect(url_for('log_view'))
        error = 'Incorrect password.'
    return render_template('log_login.html', error=error)


@app.route('/log/logout')
def log_logout():
    session.pop('log_authed', None)
    return redirect(url_for('log_login'))


@app.route('/log')
def log_view():
    if not session.get('log_authed'):
        return redirect(url_for('log_login'))
    page = request.args.get('page', 1, type=int)
    rows, total = get_log(page, _LOG_PER_PAGE)
    total_pages = max(1, (total + _LOG_PER_PAGE - 1) // _LOG_PER_PAGE)
    page = max(1, min(page, total_pages))
    return render_template('log.html', rows=rows, page=page,
                           total_pages=total_pages, total=total)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5006, debug=True)
