def doc_parts(title="", author=""):
    start="""
    \\documentclass[12pt]{article}
    \\usepackage{amsfonts}
    \\usepackage{amsmath,multicol,eso-pic}
    \\begin{document}
    \\usepackage{multicol}
    \def\columnseprulecolor{\color{white}} %Separator ruler colour"""
    if title:
        start = start + "\\title{%s} \n \date{\\vspace{-5ex}} \n \maketitle" % title


    if title="Phantom Tollbooth":
        end="""
\begin{multicols}{5}

adept

animosity

apothecary

arbitration

awe

azaz

banished

barren

battered

beret

bouquet

bunting

caldron

cartographers

cascade

cascade

chaotic

chartreuse

chasms

circumference

commendable

conciliatory

connotation

context

conveyance

crags

crest

crestfallen

crevice

dank

debris

dense

desolate

dilemma

din

disconsolate

disdain

disrepute

dissonance

distraught

dodecahedron

doldrums

eerie

effusive

famine

famished

fiends

fissure

flabbergast

flattery

flourished

flourished

fraud

gaunt

gorgons

grandeur

grimace

harrowing

havoc

hindsight

honeycombed

illusions

infuriate

intimidated

juster

laudable

ledger

lull

luminous

macabre

magenta

malice

melancholy

minstrels

mirages

misapprehension

miscellaneous

miserly

monotonous

ovation

palatinate

pandemonium

perilous

plateau

precariously

prey

procastinating

profusion

promontory

prosperous

pungent

quagmire

quest

reconcile

regal

repast

reticence

savory

sonnets

soothing

stalactites

stalked

superfluous

surmise

transfixed

tumult

unabridged

unethical

unkempt

verify

villainous

wormwood

wrath
\end{multicols}
\end{document}"""
    else:    
        end="""
        \end{document}
        """

    return start, end

def puzzle_parts(title="", author=""):
    start="""
    \\documentclass[16pt]{article}
    \\usepackage[a4paper,margin=0.5in,portrait]{geometry}
    \\usepackage{amsmath}
    \\usepackage{graphicx}
    \\usepackage{fancyhdr}
    \\begin{document}
    \\pagenumbering{gobble}
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





