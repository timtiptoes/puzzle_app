def puzzle_parts(title="", author="", number=None):
    tikz_preamble = "\n    \\usepackage{tikz}" if number is not None else ""
    if number is not None:
        tikz_overlay = """
    \\begin{tikzpicture}[overlay]
    \\node[circle, draw, line width=3pt, inner sep=10pt,
          font=\\bfseries\\fontsize{45}{54}\\selectfont,
          anchor=north east, xshift=-1.5cm, yshift=-1.5cm]
      at (current page.north east) {%d};
    \\end{tikzpicture}""" % number
    else:
        tikz_overlay = ""
    start = """
    \\documentclass[16pt]{article}
    \\usepackage[a4paper,margin=0.5in,landscape]{geometry}
    \\usepackage{amsmath}
    \\usepackage{graphicx}
    \\usepackage{fancyhdr}""" + tikz_preamble + """
    \\begin{document}
    \\pagenumbering{gobble}""" + tikz_overlay + """
    \\includegraphics[height=8cm]{static/code_key.png}
    """
    end = "\\end{document}"
    return start, end


def puzzle_section_parts(title, instr="", cols=2):
    section_start = """
        \\section*{%s}
        {\\renewcommand{\\arraystretch}{4}}\\vspace{10mm}
        \\begin{tabular}{c c c c c c c c c c}
        """ % (instr)
    section_end = """
         \\end{tabular}"""
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
