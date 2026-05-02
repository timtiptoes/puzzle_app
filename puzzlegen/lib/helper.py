import sympy
import numpy
import random
from string import ascii_lowercase, ascii_uppercase
from copy import copy

alpha = [i for i in ascii_uppercase + ascii_lowercase]
alpha.remove("l")
alpha.remove("o")
alpha.remove("O")
alpha.remove("I")
alpha.remove("i")

# Integers from -26 to 26, with and without zero
digits = range(-26, 26)
digits_nozero = list(range(-26, 26))
digits_nozero.remove(0)

powers = {
    4:   [{'base': 2,  'power': 2}],
    8:   [{'base': 2,  'power': 3}],
    9:   [{'base': 3,  'power': 2}],
    16:  [{'base': 2,  'power': 4}, {'base': 4, 'power': 2}],
    25:  [{'base': 5,  'power': 2}],
    27:  [{'base': 3,  'power': 3}],
    32:  [{'base': 2,  'power': 5}],
    36:  [{'base': 6,  'power': 2}],
    49:  [{'base': 7,  'power': 2}],
    64:  [{'base': 2,  'power': 7}, {'base': 4, 'power': 3}, {'base': 8, 'power': 2}],
    81:  [{'base': 9,  'power': 2}],
    100: [{'base': 10, 'power': 2}],
    121: [{'base': 11, 'power': 2}],
    125: [{'base': 5,  'power': 3}],
    144: [{'base': 12, 'power': 2}],
    169: [{'base': 13, 'power': 2}],
}


def shuffle(x):
    x = list(x)
    random.shuffle(x)
    return x


def get_smaller_coefficients(n, exclude=["x", "X"], first_nonzero=True, var_coeffs=False, reduce=False):
    digits_nozero_smaller = list(range(3, 12))
    if var_coeffs:
        selection = copy(digits_nozero_smaller + alpha)
        for i in exclude:
            selection.remove(i)
    else:
        selection = digits_nozero_smaller
    coeffs = []
    for i in range(n):
        c = random.choice(selection)
        if isinstance(c, str):
            c = sympy.Symbol(c)
        if reduce and random.randint(0, 1):
            c = 0
        coeffs.append(c)
    if first_nonzero and coeffs[0] == 0:
        coeffs[0] = random.choice(selection)
    return coeffs


def layout_lines(clue, linewidth):
    words = clue.split(" ")
    lines = []
    line = ""
    for word in words:
        while len(word) > linewidth:
            if line:
                lines.append(line.ljust(linewidth, " "))
                line = ""
            lines.append(word[:linewidth])
            word = word[linewidth:]
        if not line:
            line = word
        elif len(line) + 1 + len(word) <= linewidth:
            line += " " + word
        else:
            lines.append(line.ljust(linewidth, " "))
            line = word
    if line:
        lines.append(line.ljust(linewidth, " "))
    return lines


def get_coefficients(n, exclude=["x", "X"], first_nonzero=True, var_coeffs=False, reduce=True):
    if var_coeffs:
        selection = copy(digits_nozero + alpha)
        for i in exclude:
            selection.remove(i)
    else:
        selection = digits_nozero
    coeffs = []
    for i in range(n):
        c = random.choice(selection)
        if isinstance(c, str):
            c = sympy.Symbol(c)
        if reduce and random.randint(0, 1):
            c = 0
        coeffs.append(c)
    if first_nonzero and coeffs[0] == 0:
        coeffs[0] = random.choice(selection)
    return coeffs


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def render(expr, lhs=""):
    left = "$$"
    if lhs:
        left = "$$%s =" % lhs
    return sympy.latex(expr)


def make_proper(numer, denom):
    remainder = abs(numer) % denom
    whole = (abs(numer) - remainder) / denom
    return whole, cmp_to_zero(numer) * remainder


def cmp_to_zero(numer):
    if numer > 0:
        return 1
    elif numer < 0:
        return -1
    else:
        return 0


def isPrime(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def stack_em(x, y, operator='-'):
    a = str(x)
    b = str(y)
    length = len(a)
    first_line = '9' * (5 - length)
    second_line = '9' * (3 - length)
    out_str = (
        '\\overline{\\begin{array}{c}'
        '\\phantom{\\times' + first_line + '}' + a + '\\phantom{\\times9}\\\\'
        '\\phantom{\\times' + second_line + '}\\underline{' + operator + b + '}\\phantom{\\times9}'
        '\\end{array}}'
    )
    return out_str


def stack_lines(x, y):
    a = str(x) if isinstance(x, int) else x
    b = str(y) if isinstance(y, int) else y
    length = len(a)
    first_line = '9' * (5 - length)
    second_line = '9' * (3 - length)
    out_str = (
        '\\overline{\\begin{array}{c}'
        '\\phantom{\\times' + first_line + '}' + a + '\\phantom{\\times9}\\\\'
        '\\phantom{\\times' + second_line + '}' + b + '\\phantom{\\times9}'
        '\\end{array}}'
    )
    return out_str


def get_power_choices():
    num_powers = random.randint(1, 3)
    pick = random.choice(list(powers.keys()))
    picks = []
    while pick not in picks and len(picks) < num_powers:
        picks.append(pick)
        pick = random.choice(list(powers.keys()))
    return picks


def get_power_choice(perfect_power):
    return random.choice(powers[perfect_power])


def right_sign(x):
    if x > 0:
        return "+{}".format(x)
    elif x < 0:
        return str(x)
    else:
        return ""


def find_shortest(target, conversion_factor):
    mantissa_target = "{:.12E}".format((target) / conversion_factor).split('E')[0]
    mantissa_lower = "{:.12E}".format((target - 0.49) / conversion_factor).split('E')[0]
    mantissa_upper = "{:.12E}".format((target + 0.49) / conversion_factor).split('E')[0]
    shortest_lower = find_shortest_common_string(mantissa_lower, mantissa_target)
    shortest_upper = find_shortest_common_string(mantissa_upper, mantissa_target)
    shortest = min(shortest_upper, shortest_lower)
    exponent = "{:.12E}".format((target) / conversion_factor).split('E')[1]

    if int(exponent) > -3:
        ret_format_str = "{:0." + str(shortest + 2) + "f}"
        ret_str = ret_format_str.format(float(mantissa_target[0:shortest + 2] + "E" + exponent))
        if int(float(ret_str)) == float(ret_str):
            ret_str = "{:0.0f}".format(float(mantissa_target[0:shortest + 2] + "E" + exponent))
        return ret_str

    return mantissa_target[0:shortest + 2] + "E" + exponent


def find_shortest_common_string(s1, s2):
    first_one, second_one = (s1, s2) if len(s1) <= len(s2) else (s2, s1)
    for i in range(len(first_one)):
        if first_one[i] != second_one[i]:
            return i - 1
    return -1


def choose_someint(rng):
    x = 0
    while x == 0:
        x = random.randint(-rng, rng)
    return x


def simple_line(m, x, b, *args, **kwargs):
    return m * x + b


def list_of_ints(tot, n):
    ints = []
    while len(ints) < n:
        someint = choose_someint(10)
        if someint not in ints:
            ints.append(someint)
    ints.append(tot - sum(ints))
    return ints


def compound(p, r, t, n=12.0):
    return p * (1 + r / n) ** (n * t)
