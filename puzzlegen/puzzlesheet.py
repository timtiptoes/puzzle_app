import os
import random
import datetime
from .lib import *

_problems_map = {
    "simple_addition":           make_simple_addition_problem,
    "add_negatives":             add_negatives,
    "multiplication_then_addition": make_simple_multiplication_problem,
    "fraction_addition":         make_fraction_addition_problem,
    "simple_division_problem":   make_simple_division_problem,
    "simplify_ratio":            make_simplify_ratio_problem,
    "two_digit_subtraction":     two_digit_subtraction,
    "two_digit_multiplication":  two_digit_multiplication,
    "add_coins":                 add_coins,
    "exponents_problem":         exponents_problem,
    "divide_exponents":          divide_exponents,
    "simple_algebra":            simple_algebra,
    "single_decimal_addition":   single_decimal_addition,
    "quadratic_equations":       make_quadratic_eq,
    "roots_problem":             roots_problem,
    "determinant":               determinant,
    "unit_conversion":           unit_conversion,
    "simple_series":             simple_series,
    "convert_base":              convert_base,
    "linear_system":             linear_system,
    "find_slope":                find_slope,
    "simplify_exponents":        simplify_exponents,
    "simplify_exponent_division": simplify_exponent_division,
    "percent_increase":          percent_increase,
    "compound_interest":         compound_interest,
    "simple_scientific":         simple_scientific,
    "intermediate_scientific":   intermediate_scientific,
    "harder_scientific":         harder_scientific,
}

# Types whose LaTeX expressions evaluate directly to the numeric target — safe to combine additively.
# Types like simple_algebra (equations), simplify_exponents (variable expressions), or
# fraction_addition (answer = numerator, not expression value) are excluded.
_ADDABLE_TYPES = {
    "simple_addition", "add_negatives", "multiplication_then_addition",
    "simple_division_problem", "two_digit_subtraction", "add_coins",
    "exponents_problem", "divide_exponents", "single_decimal_addition",
    "roots_problem",
}


def _strip_overline(s):
    if s.startswith("\\overline{") and s.endswith("}"):
        return s[len("\\overline{"):-1]
    return s


instructions_map = {
    "simple_addition":            "Add the two numbers to find the letter above",
    "add_negatives":              "Add the numbers",
    "multiplication_then_addition": "Solve for the letter above",
    "fraction_addition":          "Use the numerator of the improper fraction to find the letter above",
    "simple_division_problem":    "Solve for the letter above",
    "simplify_ratio":             "Use the numerator of the simplified ratio to find the letter above",
    "two_digit_subtraction":      "Use the difference to find the letter above",
    "two_digit_multiplication":   "Use the inner two digits of the product to find letter above",
    "add_coins":                  "Find the total value of the coins to find letter above",
    "exponents_problem":          "Solve each to find the letter above",
    "divide_exponents":           "Subtract exponents with the same base, then find the letter above",
    "roots_problem":              "Solve each to find letter above",
    "simple_algebra":             "Solve for x to find the letter above",
    "single_decimal_addition":    "Add to find the letter above",
    "quadratic_equations":        "Add the roots to find the letter above",
    "determinant":                "Find the determinant of each matrix",
    "unit_conversion":            "Round each conversion to the nearest integer to find the letter above",
    "simple_series":              "Find the next number in the series",
    "convert_base":               "Convert each to base 10",
    "linear_system":              "Add x+y and find letter above",
    "simplify_exponents":          "Simplify exponents and look up result above.",
    "simplify_exponent_division":  "Simplify exponents and look up result above.",
    "find_slope":                 "Use the slope of the line through two points to find letter above",
    "percent_increase":           "Find the closest integer to match the letter above",
    "compound_interest":          "Use the closest amount in thousands below to find letter above",
    "simple_scientific":          "Convert each number to standard notation and find the letter above",
    "intermediate_scientific":    "Convert each number to standard notation and find the letter above",
    "harder_scientific":          "Convert each number to standard notation and find the letter above",
}


class document(object):
    def __init__(self, fname, title="", savetex=True, doc_generator=puzzle_parts):
        self.savetex = savetex
        self.start, self.end = doc_generator(title)
        self.main = []
        self.fname = fname

    def add(self, code):
        self.main.append(code)

    def write_compile(self):
        main = '\n'.join(self.main)
        doc = '\n'.join([self.start, main, self.end])
        with open("tmp/%s.tex" % self.fname, "wb") as f:
            f.write(doc.encode('utf-8'))
        os.system("pdflatex --output-directory tmp tmp/%s.tex" % self.fname)
        now = datetime.datetime.now().isoformat()
        os.system("cp tmp/{}.pdf log/{}_{}.pdf".format(self.fname, self.fname, now))


class puzzlesheet(object):
    def __init__(self, fname, title="", clue="gimme", savetex=False):
        self.lookup_table = {
            "J": 0,  "E": 1,  "N": 2,  "I": 3,  "U": 4,  "X": 5,
            "A": 6,  "G": 7,  "W": 8,  "C": 9,  "Y": 10, "'": 11,
            "T": 12, "L": 13, "B": 14, "Z": 15, "P": 16, "Q": 17,
            "M": 18, "V": 19, "R": 20, "H": 21, "F": 22, "D": 23,
            "O": 24, "S": 25, "K": 26,
        }
        self.fname = fname
        self.clue = clue.upper()
        self.puzzlesheet = document(fname, title, savetex)

    def add_section(self, problem_type, cols, title, instructions, *args, **kwargs):
        if isinstance(problem_type, list):
            all_gens = [_problems_map[pt] for pt in problem_type]
            addable_gens = [_problems_map[pt] for pt in problem_type if pt in _ADDABLE_TYPES]
            if len(addable_gens) >= 2:
                def prob_generator(target, *a, **kw):
                    g1, g2 = random.sample(addable_gens, 2)
                    if target >= 2:
                        part1 = random.randint(1, target - 1)
                    else:
                        return random.choice(addable_gens)(target)
                    part2 = target - part1
                    p1, _ = g1(part1)
                    p2, _ = g2(part2)
                    expr1 = _strip_overline(p1)
                    expr2 = _strip_overline(p2)
                    combined = "\\overline{" + expr1 + "}\\\\" + "+\\overline{" + expr2 + "}"
                    return combined, str(target)
            else:
                prob_generator = lambda target, *a, **kw: random.choice(all_gens)(target, *a, **kw)
        else:
            prob_generator = problem_type if hasattr(problem_type, '__call__') else _problems_map[problem_type]
        start, end = puzzle_section_parts(title, instructions, cols=1)

        s_probs = []
        lines = layout_lines(self.clue, cols)
        for line in lines:
            for i in range(len(line)):
                terminator = "&" if i < len(line) - 1 else '\\vspace{15mm}' + '\\' + '\\'
                ch = line[i]
                if ch != " ":
                    p, sols = prob_generator(self.lookup_table[ch], *args, **kwargs)
                    prob = puzzle_problem(p) + terminator
                else:
                    prob = terminator
                s_probs.append(prob)

        prob_code = ''.join([start, '\n'.join(s_probs), end])
        self.puzzlesheet.add(prob_code)

    def write(self):
        self.puzzlesheet.write_compile()
