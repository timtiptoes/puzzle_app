import os
from lib import *
#import lib

_problems_map = {"simple_addition": make_simple_addition_problem,
                 "multiplication_then_addition": make_simple_multiplication_problem,
                 "fraction_addition": make_fraction_addition_problem,
                 "simple_division_problem":make_simple_division_problem,
                 "simplify_ratio":make_simplify_ratio_problem,
                 "quadratic_equations" : make_quadratic_eq,
                 "two_digit_subtraction":two_digit_subtraction}

instructions_map={"simple_addition": "Add the two numbers to find the letter above",
                 "multiplication_then_addition": "Solve for the letter above",
                 "fraction_addition": "Use the numerator to find the letter above",
                 "simple_division_problem":"Solve for the letter above",
                 "simplify_ratio":"Use the numerator of the simplified ratio to find the letter above",
                 "quadratic_equations":"Add the roots to find the letter above",
                 "two_digit_subtraction":"Use the difference to find the letter above"}


class document(object):
    """
    Small class for managing the documents and compiling them
    """
    def __init__(self, fname, title="", savetex=False, doc_generator = puzzle_parts):
        self.savetex = savetex
        self.start, self.end = doc_generator(title)
        self.main = []
        self.fname = fname

    def add(self, code):
        """
        Adds new sections to the document
        """
        self.main.append(code)

    def write_compile(self, remove_aux=True):
        """
        Writes and compiles into a pdf
        """
        print "I think fname is >>>"+self.fname+"<<<<\n"
        main = '\n'.join(self.main)
        doc = '\n'.join([self.start, main, self.end])
        f = open("%s.tex" % self.fname, "wb")
        f.write(doc)
        f.close()
        os.system("pdflatex --output-directory tmp %s.tex" % self.fname)
        os.remove("%s.log" % self.fname)
        if remove_aux:
            os.remove("%s.aux" % self.fname)
        if not self.savetex:
            os.remove("%s.tex" % self.fname)

class puzzlesheet(object):
    """
    Class for managing a puzzlesheet.
    """
    def __init__(self, fname, title="",clue="gimme", savetex=False):
        """
        fname : file name for the worksheet
        title : title to be placed in the worksheet
        savetex : flag to either save or delete the .tex files after compiling
        """
        self.lookup_table={"J":0,"E":1,"N":2,"I":3,"U":4,"X":5,"A":6,"G":7,"W":8,"C":9,"Y":10,"'":11,"T":12,"L":13,"B":14,"Z":15,"P":16,"Q":17,"M":18,"V":19,"R":20,"H":21,"F":22,"D":23,"O":24,"S":25,"K":26}

        self.fname = fname
        self.clue = clue.upper()
        self.puzzlesheet = document(fname, title, savetex)


    def add_section(self, problem_type,cols,title,instructions,*args, **kwargs):
        """
        Method for adding a section of problems to an worksheet & solutions.
        problem_type : name of the type of problem, which is mapped to a
                       problem generating function shown at the top of this file

                                                OR
                       
                       A problem generating function directly. This function
                       must take no arguments, and return a tuple of two strings.
                       The first string gives the problem, the second string it's
                       solution.
        n : the number of problems to generate for this section.
        title : title text for the section
        instructions : text instructions for the section
        """
        if hasattr(problem_type, '__call__'):
            prob_generator = problem_type
        else:
            prob_generator = _problems_map[problem_type]

        start, end = puzzle_section_parts(title, instructions, cols=1)

        s_probs = []
        lines=layout_lines(self.clue,cols)
        for line in lines:
            for i in range(len(line)):
                terminator = "&" if i<len(line)-1 else '\\vspace{15mm}'+'\\'+'\\'
                ch = line[i]
                if ch !=" ":
                    p, sols = prob_generator(self.lookup_table[ch],*args, **kwargs)
                    prob =puzzle_problem(p) + terminator
                else:
                    prob = terminator
                s_probs.append(prob)

        s_probs = '\n'.join(s_probs)
        prob_code = ''.join([start, s_probs, end])

        print" YOUCH"
        print s_probs
        self.puzzlesheet.add(prob_code)

    def write(self):
        self.puzzlesheet.write_compile()




