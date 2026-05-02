import os


def get_categories():
    crossword_puzzles = {}
    math_puzzle_list = [
        'simple_addition', 'add_negatives', 'multiplication_then_addition',
        'fraction_addition', 'simple_division_problem', 'simplify_ratio',
        'two_digit_subtraction', 'two_digit_multiplication', 'add_coins',
        'exponents_problem', 'divide_exponents', 'simple_algebra', 'single_decimal_addition',
        'quadratic_equations', 'roots_problem', 'determinant', 'unit_conversion',
        'simple_series', 'convert_base', 'linear_system', 'simplify_exponents',
        'find_slope', 'simplify_exponent_division', 'simple_scientific', 'harder_scientific',
        'intermediate_scientific', 'scientific_add_sub', 'percent_increase', 'find_the_power',
    ]

    for p in [x for x in os.listdir('static/') if x.endswith(".csv")]:
        f = p.replace(".csv", "")
        crossword_puzzles[f.replace("_", " ")] = {'filename': f, 'type': 'crossword'}

    math_puzzles = {
        p.replace("_", " "): {'filename': p, 'type': 'math'}
        for p in math_puzzle_list
    }

    #return {**crossword_puzzles, **math_puzzles}
    return {**math_puzzles}

def get_display_categories():
    return [(x, '$$\\texttt{' + x + '}$$') for x in get_categories().keys()]
