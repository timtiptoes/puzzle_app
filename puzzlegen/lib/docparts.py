def doc_parts(title="", author=""):
    start="""
    \\documentclass[10pt]{article}
    \\usepackage{amsfonts}
    \\usepackage{amsmath,multicol,eso-pic}
    \makeatletter
        \newcommand\tinyv{\@setfontsize\tinyv{4pt}{6}}
    \makeatother
    \\begin{document}
    \\usepackage{multicol}
    \def\columnseprulecolor{\color{white}} %Separator ruler colour"""
    if title:
        start = start + "\\title{%s} \n \date{\\vspace{-5ex}} \n \maketitle" % title
 
        end="""
        \end{document}
        """

    return start, end

def puzzle_parts(title="", author=""):
    start="""
    \\documentclass[10pt]{article}
    \\usepackage[a4paper,margin=0.5in,landscape]{geometry}
    \\usepackage{amsmath}
    \\usepackage{graphicx}
    \\usepackage{fancyhdr}
    \\begin{document}
    \\pagenumbering{gobble}
        \\makeatletter
        \\newcommand\\tinyv{\\@setfontsize\\tinyv{4pt}{6}}
    \\makeatother
    """

    end = """\end{document}"""
    return start, end

def puzzle_section_parts(title, instr="", cols = 2):
    section_start="""
        \section*{%s}
        {\\renewcommand{\\arraystretch}{4}}\\vspace{10mm}
        \\begin{tabular}{c c c c c c c c c c}
        """% (instr)
    section_end = """
         \\end{tabular}"""
    return section_start, section_end

def problem(instructions, problem, solution, points=1):
    code = """
    \\question[%s]
        %s
        %s
    \\begin{solution} 
        %s
    \\end{solution}
    """ % (str(points), instructions, problem, solution)
    return code

def puzzle_problem(problem):
    code = """
    $\\begin{aligned}[c]
        %s
    \\end{aligned}$
    """ % (problem)
    return code

def crossword_parts(title="", author=""):
    start="""
    \\documentclass{article}
    \\usepackage[letterpaper, landscape, margin=0.5in]{geometry}
    \\usepackage{cwpuzzle}
    \\begin{document}
    \\pagenumbering{gobble}
    \\textsc{\\LARGE \centering """
    start+=title
    start+=" }"+"\\"+"\\"+"[1.5cm]"
#    start+="\\"+"\\"+"\\"


    middle="""
    \\end{Puzzle}

    \\begin{PuzzleClues}{\\textbf{Hints}}\\\\"""
    end = """\\end{PuzzleClues}

            \\end{document}
          """
    return start,middle, end

if __name__ == "__main__":
    print problem("test", "fasd", "asdfasd", 10)





