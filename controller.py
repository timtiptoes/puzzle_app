from flask import Flask, render_template, request, send_file
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime
from model import InputForm
from puzzlegen import puzzlesheet
from puzzlegen import crosswordsheet
from utils import get_categories
from db import init_db, log_puzzle

app = Flask(__name__)
init_db()


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


@app.route("/make_puzzle/<string:puzzle_type>")
@nocache
def make_puzzle(puzzle_type):
    categories = get_categories()
    clue = request.args.get("clue")
    if categories[puzzle_type]['type'] == 'math':
        sheet = puzzlesheet.puzzlesheet("puzzle", "", clue, savetex=True)
        puzz = categories[puzzle_type]['filename'].lower()
        sheet.add_section(puzz, 6, "", puzzlesheet.instructions_map[puzz], rhs=0)
        sheet.write()
        filename = "puzzle.pdf"
    else:
        sheet = crosswordsheet.crossword1d(categories[puzzle_type]['filename'], title=puzzle_type, clue=clue, savetex=True)
        sheet.add_section()
        sheet.write()
        filename = sheet.fname + ".pdf"
    log_puzzle(clue, puzzle_type)
    return send_file('tmp/' + filename, download_name='puzzle.pdf')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5006, debug=True)
