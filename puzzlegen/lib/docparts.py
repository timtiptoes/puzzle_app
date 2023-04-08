def doc_parts(title="", author=""):
    start=""
    end=""

    return start, end

def puzzle_parts(title="", author=""):
    start=""

    end = ""
    return start, end

def puzzle_section_parts(title, instr="", cols = 2):
    section_start=""
    section_end = ""
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
    {\\tinyv
    $\\begin{aligned}[c]
        %s
    \\end{aligned}$
    }
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





