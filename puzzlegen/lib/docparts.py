def doc_parts(title="", author=""):
    start="""
    \\documentclass[12pt]{article}
    \\usepackage{amsfonts}
    \\usepackage{amsmath,multicol,eso-pic}
    \\begin{document}
    """

    if title:
        start = start + "\\title{%s} \n \date{\\vspace{-5ex}} \n \maketitle" % title

    end="""
    \end{document}
    """
    return start, end

def puzzle_parts(title="", author=""):
    start="""
    \\documentclass[16pt]{article}
    \\usepackage[a4paper,margin=0.5in,landscape]{geometry}
    \\usepackage{amsmath}
    \\usepackage{graphicx}
    \\usepackage{fancyhdr}
    \\begin{document}
    \\includegraphics[height=8cm]{static/code_key.png}
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

if __name__ == "__main__":
    print problem("test", "fasd", "asdfasd", 10)





