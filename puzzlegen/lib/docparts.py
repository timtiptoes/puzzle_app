_LIBRARY_TEXT = (
    "\\noindent\\includegraphics[height=8cm]{static/code_key.png}\\hfill%\n"
    "{\\setlength{\\fboxsep}{8pt}%\n"
    "\\fbox{\\begin{minipage}[c]{14cm}%\n"
    "\\centering\\textbf{Library Etiquette}\\\\[2pt]%\n"
    "\\raggedright\\small%\n"
    "Use the computer to find this book. Go to page 12. Ask a librarian if you must\\\\\n"
    "Be sure to put the book back in the same place you found it. "
    "Mixing up books effectively loses them\\\\\n"
    "Be quiet and respectful to those in the library%\n"
    "\\end{minipage}}}\\\\[6pt]\n"
)


def puzzle_parts(title="", author="", number=None):
    if number is not None:
        number_overlay = """
    \\begin{tikzpicture}[remember picture, overlay]
    \\node[circle, draw, line width=3pt, inner sep=10pt,
          font=\\bfseries\\fontsize{45}{54}\\selectfont,
          anchor=north east, xshift=-1.5cm, yshift=-1.5cm]
      at (current page.north east) {%d};
    \\end{tikzpicture}""" % number
    else:
        number_overlay = ""
    start = """
    \\documentclass[16pt]{article}
    \\usepackage[a4paper,margin=0.5in,landscape]{geometry}
    \\usepackage{amsmath}
    \\usepackage{graphicx}
    \\usepackage{fancyhdr}
    \\usepackage{tikz}
    \\newsavebox{\\puzzlebox}
    \\begin{document}
    \\pagenumbering{gobble}""" + number_overlay + "\n    " + _LIBRARY_TEXT + """
    """
    end = "\\end{document}"
    return start, end


def puzzle_section_parts(title, instr="", cols=6):
    col_spec = " ".join(["c"] * cols)
    section_start = """
        \\section*{%s}
        {\\renewcommand{\\arraystretch}{4}}\\vspace{10mm}
        \\sbox{\\puzzlebox}{\\begin{tabular}{%s}
        """ % (instr, col_spec)
    section_end = """
         \\end{tabular}}
         \\resizebox{\\ifdim\\wd\\puzzlebox>0.92\\linewidth 0.92\\linewidth\\else\\wd\\puzzlebox\\fi}{!}{\\usebox{\\puzzlebox}}"""
    return section_start, section_end


def puzzle_problem(problem):
    return """
    $\\begin{aligned}[c]
        %s
    \\end{aligned}$
    """ % (problem)


def crossword_parts(title="", author=""):
    start = """
    \\documentclass{article}
    \\usepackage[letterpaper, landscape, margin=0.5in]{geometry}
    \\usepackage{cwpuzzle}
    \\begin{document}
    \\pagenumbering{gobble}
    \\textsc{\\LARGE \\centering """
    start += title
    start += " }" + "\\" + "\\" + "[1.5cm]"

    middle = """
    \\end{Puzzle}

    \\begin{PuzzleClues}{\\textbf{Hints}}\\\\"""
    end = """\\end{PuzzleClues}

            \\end{document}
          """
    return start, middle, end
