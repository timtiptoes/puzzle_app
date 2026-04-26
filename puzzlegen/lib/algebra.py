import math
import random
import re
import sympy
from functools import reduce
from sympy import symbols, expand, factor, Poly
from sympy.parsing.sympy_parser import parse_expr
from sympy.polys.polytools import degree

from .helper import *


def make_simple_addition_problem(target, *args, **kwargs):
    digits = range(0, 25)
    while True:
        r1 = random.choice(digits)
        if r1 < target:
            break
    r2 = target - r1
    sols = "$$" + sympy.latex(target) + "$$"
    outstr = "\\overline{" + str(r1) + "+" + str(r2) + "}"
    return outstr, sols


def make_simple_multiplication_problem(target, *args, **kwargs):
    r1, r2 = get_smaller_coefficients(2)
    r3 = target - r1 * r2
    sols = "$$" + sympy.latex(target) + "$$"
    sign = "+" if r3 >= 0 else ""
    outstr = "\\overline{" + str(r1) + "\\times" + str(r2) + sign + str(r3) + "}"
    return outstr, sols


def make_simple_division_problem(target, *args, **kwargs):
    c = random.choice(range(2, 14))
    outstr = "\\frac{" + str(c * target) + "}{" + str(c) + "}"
    return "\\overline{" + outstr + "}", []


def make_fraction_addition_problem(target, *args, **kwargs):
    primes = [2, 3, 5, 7, 11, 13]
    ints = range(2, 14)
    these_primes = prime_factors(target)

    while True:
        while True:
            c = random.choice(primes)
            if c not in these_primes:
                break
        while True:
            f = random.choice(primes)
            if f not in these_primes and f != c:
                break
        while True:
            b = random.choice(ints)
            if b not in [c, f]:
                break
        e = target - b
        f1 = sympy.fraction(sympy.S(b) / sympy.S(c * f))
        f2 = sympy.fraction(sympy.S(e) / sympy.S(c * f))
        ap, bp = make_proper(f1[0], f1[1])
        dp, ep = make_proper(f2[0], f2[1])
        if bp != 0 and ep != 0 and f1[1] != f2[1]:
            break

    sign = "+" if ep >= 0 else "-"
    outstr = "\\frac{" + str(bp) + "}{" + str(f1[1]) + "}"
    second_int = str(dp) if dp != 0 else ""
    outstr += sign + second_int + "\\frac{" + str(abs(ep)) + "}{" + str(f2[1]) + "}"
    return "\\overline{" + outstr + "}", []


def make_simplify_ratio_problem(target, *args, **kwargs):
    c = random.choice(range(2, 14))
    while True:
        b = random.choice(range(2, 14))
        if b != c:
            break
    outstr = "\\frac{" + str(c * target) + "}{" + str(c * b) + "}"
    return "\\overline{" + outstr + "}", []


def make_quadratic_eq(target, rhs=None, integer=[0, 1]):
    var = random.choice("pqrstuvwxyz")
    x = sympy.Symbol("x")
    f = random.randint(2, 5) * random.choice([-1, 1])
    r1 = target
    while r1 == target:
        r1 = random.randint(1, 13)
    r2 = target - r1
    expr = (f * x - r1 * f) * (x - r2)
    ex = Poly(expand(expr), x)
    a, b, c = tuple(ex.coeffs())
    out_str = "{}{}^2{}{}{}".format(a, var, right_sign(b), var, right_sign(c))
    sols = "$$" + sympy.latex(target) + "$$"
    return "\\overline{" + out_str + "}", sols


def two_digit_subtraction(target, *args, **kwargs):
    r1 = random.choice(range(50, 99))
    r2 = r1 - target
    sols = "$$" + sympy.latex(target) + "$$"
    outstr = stack_em(r1, r2, "-")
    return outstr, sols


def two_digit_multiplication(target, *args, **kwargs):
    single_digits = range(1, 10)
    trier = 2
    while isPrime(trier):
        a = random.choice(single_digits)
        b = random.choice(single_digits)
        trier = 1000 * a + 10 * target + b
    p = prime_factors(trier)
    mx = max(p)
    p.remove(mx)
    rest = reduce(lambda x, y: x * y, p)
    sols = "$$" + sympy.latex(target) + "$$"
    outstr = stack_em(mx, rest, operator="\\times")
    return outstr, sols


def add_coins(target, *args, **kwargs):
    number_words = (
        "one,two,three,four,five,six,seven,eight,nine,ten,eleven,"
        "twelve,thirteen,fourteen,fifteen,sixteen,seventeen,"
        "eighteen,nineteen,twenty,twenty-one,twenty-two,"
        "twenty-three,twenty-four,twenty-five,twenty-six,twenty-seven"
    ).split(",")

    coins = {
        'quarters': {'value': 25, 'singular': 'quarter'},
        'dimes':    {'value': 10, 'singular': 'dime'},
        'nickels':  {'value': 5,  'singular': 'nickel'},
        'pennies':  {'value': 1,  'singular': 'penny'},
    }

    total = target
    keys = list(coins.keys())
    purse = {}
    while total > 0:
        coin = random.choice(keys)
        value = coins[coin]['value']
        if total - value >= 0:
            purse[coin] = purse.get(coin, 0) + 1
            total -= value

    out_str = "\\overline{"
    purse_keys = list(purse.keys())
    for i, coin in enumerate(purse_keys):
        coin_name = coin if purse[coin] > 1 else coins[coin]['singular']
        out_str += "\\textrm{" + number_words[purse[coin] - 1] + " " + coin_name + "}"
        if i == 0:
            out_str += "}"
        if i != len(purse_keys) - 1:
            out_str += "\\\\"
    return out_str, "$$ $$"


def exponents_problem(target, *args, **kwargs):
    list_of_perfect_powers = get_power_choices()
    out_str = ""
    signed_values = []
    for pp in list_of_perfect_powers:
        pp_pick = get_power_choice(pp)
        base, power = pp_pick['base'], pp_pick['power']
        # Odd powers allow a negative base: (-2)^3 = -8
        if power % 2 == 1 and random.random() < 0.5:
            out_str += "(-{})^{}".format(base, power)
            signed_values.append(-pp)
        else:
            out_str += "{}^{}".format(base, power)
            signed_values.append(pp)
        if pp != list_of_perfect_powers[-1]:
            out_str += "+"
    constant = target - sum(signed_values)
    if constant > 0:
        out_str += "+{}".format(constant)
    elif constant < 0:
        out_str += "{}".format(constant)
    sols = "$$" + sympy.latex(target) + "$$"
    return "\\overline{" + out_str + "}", sols


def divide_exponents(target, *args, **kwargs):
    # Each term is base^(power+k) / base^k, which simplifies to base^power (a perfect power).
    # Sum 1-3 such terms plus a constant offset to reach the target.
    list_of_perfect_powers = get_power_choices()
    constant = target - sum(list_of_perfect_powers)
    out_str = ""
    for i, pp in enumerate(list_of_perfect_powers):
        pp_pick = get_power_choice(pp)
        base = pp_pick['base']
        power = pp_pick['power']
        k = random.randint(1, 4)
        out_str += "\\frac{{{}^{{{}}}}}{{{}^{{{}}}}}".format(base, power + k, base, k)
        if i < len(list_of_perfect_powers) - 1:
            out_str += "+"
    if constant > 0:
        out_str += "+{}".format(constant)
    elif constant < 0:
        out_str += "{}".format(constant)
    sols = "$$" + sympy.latex(target) + "$$"
    return "\\overline{" + out_str + "}", sols


def roots_problem(target, *args, **kwargs):
    list_of_perfect_powers = get_power_choices()
    out_str = ""
    base_sum = 0
    for pp in list_of_perfect_powers:
        pp_pick = get_power_choice(pp)
        base_sum += pp_pick['base']
        out_str += "\\sqrt[{}]".format(pp_pick['power']) + "{" + str(pp) + "}"
        if pp != list_of_perfect_powers[-1]:
            out_str += "+"
    constant = target - base_sum
    if constant > 0:
        out_str += "+{}".format(constant)
    elif constant < 0:
        out_str += "{}".format(constant)
    sols = "$$" + sympy.latex(target) + "$$"
    return "\\overline{" + out_str + "}", sols


def simple_algebra(target, *args, **kwargs):
    coefficient = random.randint(1, 13)
    rhs = random.randint(1, 30)
    constant = rhs - coefficient * target
    out_coefficient = str(coefficient) if coefficient > 1 else ""
    out_constant = "+{}".format(constant) if constant > 0 else "{}".format(constant)
    sols = sympy.latex(target)
    out_str = "{}x{}={}".format(out_coefficient, out_constant, rhs)
    return "\\overline{" + out_str + "}", sols


def decimal_addition(target, num_places, *args, **kwargs):
    f = random.uniform(.1, .9)
    a = float(int(target * f * 10**num_places)) / 10**num_places
    b = float(round((target - a) * 10**num_places)) / 10**num_places
    sols = "$$" + sympy.latex(target) + "$$"
    out_str = stack_em(a, b, '+')
    return out_str, sols


def single_decimal_addition(target, *args, **kwargs):
    return decimal_addition(target, 2)


def determinant(target, *args, **kwargs):
    single_digits = range(1, 10)
    trier = 2
    while isPrime(abs(trier)):
        a = random.choice(single_digits)
        d = random.choice(single_digits)
        trier = a * d - target
    p = prime_factors(abs(trier))
    idx = random.randint(0, len(p) - 1)
    p[idx] = p[idx] * numpy.sign(trier)
    b = random.choice(p)
    c = trier / b
    out_str = "\\overline{\\begin{vmatrix}" + "{} & {} \\\ {} & {} ".format(a, b, c, d) + " \\end{vmatrix}}"
    sols = "$$" + sympy.latex(target) + "$$"
    return out_str, sols


def unit_conversion(target, allow_scientific=False, *args, **kwargs):
    systems = {
        "Imperial": {
            "length":  {"in": 1.0, "ft": 12.0, "yd": 36.0, "miles": 63360.0},
            "volume":  {"tsp": 0.333333, "Tb": 0.5, "oz": 1, "pints": 16.0, "quarts": 32.0, "gallons": 128.0},
            "mass":    {"oz": 1.0, "lbs": 16.0, "tons": 32000.0},
        },
        "Metric": {
            "length":  {"mm": .03937, "m": 39.37, "cm": 0.3937, "kilometers": 39370.0},
            "volume":  {"ml": 0.033814, "cc": 0.033814, "liters": 33.814},
            "mass":    {"mg": 3.5274e-5, "g": 3.5274e-2, "kg": 35.274},
        },
    }
    conversion_factor = 0.0
    computed_target = 0.0

    while round(float(computed_target) * conversion_factor) != target or ('E' in computed_target and not allow_scientific):
        source_system = random.choice(list(systems.keys()))
        source_type = random.choice(list(systems[source_system].keys()))
        source_unit = random.choice(list(systems[source_system][source_type].keys()))
        dest_unit = source_unit
        while dest_unit == source_unit:
            dest_system = random.choice(list(systems.keys()))
            dest_unit = random.choice(list(systems[dest_system][source_type].keys()))

        f1 = systems[source_system][source_type][source_unit]
        f2 = systems[dest_system][source_type][dest_unit]
        conversion_factor = f1 / f2
        sols = sympy.latex(target)
        computed_target = find_shortest(target, conversion_factor)

    computed_target = computed_target.rstrip("0") if "." in computed_target else computed_target
    out_str = computed_target + "\\ \\textrm{" + source_unit + "}\\ =\\ ?\\ \\textrm{" + dest_unit + "}"
    return "\\overline{" + out_str + "}", sols


def add_negatives(target, *args, **kwargs):
    digits = range(-25, 25)
    chosen_digits = []
    chosen_operators = []
    while len(chosen_digits) < 1:
        r1 = random.choice(digits)
        r2 = random.choice([-1, 1])
        if r1 not in chosen_digits and -r1 not in chosen_digits:
            chosen_digits.append(r1)
            chosen_operators.append(r2)

    sols = "$$" + sympy.latex(target) + "$$"
    outstr = str(chosen_digits[0])
    running_total = chosen_digits[0]
    for i in range(1, len(chosen_digits)):
        if chosen_operators[i] == -1:
            op = "-"
            running_total -= chosen_digits[i]
        else:
            op = "+"
            running_total += chosen_digits[i]
        outstr += op + str(chosen_digits[i])
    final = target - running_total
    if final > 0:
        outstr += "+"
    outstr += str(final)
    return "\\overline{" + outstr + "}", sols


def common_difference(target):
    decrement = random.randint(3, 9)
    sign = random.choice([-1, 1])
    ret_list = []
    next_num = target - sign * decrement
    while len(ret_list) < 5:
        ret_list.append(next_num)
        next_num -= sign * decrement
    ret_list_str = [str(i) for i in sorted(ret_list, reverse=(sign < 1))]
    ret_list_str.append('x')
    return "\\overline{" + ",".join(ret_list_str) + "}", []


def common_ratio(target):
    starting_num = random.randint(3, 4)
    ratio = random.choice([0.25, 0.5, 2, 3, 4, 5])
    next_num = starting_num * (1 / ratio)**4 if ratio < 1 else starting_num
    ret_list = []
    while len(ret_list) < 4:
        ret_list.append(int(next_num))
        next_num *= ratio
    pre_ret_list = sorted(ret_list, reverse=ratio < 1)
    correction = target - pre_ret_list[-1]
    if correction < 0:
        correction_text = " then subtract " + str(abs(int(correction)))
    elif correction > 0:
        correction_text = " then add " + str(abs(int(correction)))
    else:
        correction_text = ""
    pre_ret_list.pop()
    pre_ret_list.append('x')
    outstr = ",".join([str(i) for i in pre_ret_list]) + "\\text{" + correction_text + "}"
    return "\\overline{" + outstr + "}", []


def simple_series(target, *args, **kwargs):
    if random.choice(['heads', 'tails']) == 'heads':
        return common_difference(target)
    else:
        return common_ratio(target)


def basetoStr(n, base):
    convertString = "0123456789ABCDEF"
    if n < base:
        return convertString[n]
    else:
        return basetoStr(n // base, base) + convertString[n % base]


def convert_base(target, *args, **kwargs):
    base = random.choice(range(2, 9))
    outstr = "{}_{}".format(basetoStr(target, base), base) + " = ?_{10}"
    sols = "$$" + sympy.latex(target) + "$$"
    return "\\overline{" + outstr + "}", sols


def linear_system(target, *args, **kwargs):
    x = choose_someint(5)
    y = target - x
    coeff11 = choose_someint(6)
    coeff12 = choose_someint(6)
    sign1 = "+" if coeff12 > 0 else ''
    constant1 = coeff11 * x + coeff12 * y
    coeff21 = coeff11
    while coeff21 == coeff11:
        coeff21 = choose_someint(9)
    coeff22 = choose_someint(9)
    constant2 = coeff21 * x + coeff22 * y
    sign2 = "+" if coeff22 > 0 else ''
    out_str = stack_lines(
        "{}x {} {}y = {}".format(coeff11, sign1, coeff12, constant1),
        "{}x {} {}y = {}".format(coeff21, sign2, coeff22, constant2),
    )
    sols = sympy.latex(target)
    return out_str, sols


def find_slope(target, *args, **kwargs):
    b = choose_someint(9)
    x1 = choose_someint(10)
    y1 = simple_line(target, x1, b)
    x2 = x1
    while x1 == x2:
        x2 = choose_someint(10)
    y2 = simple_line(target, x2, b)
    sols = sympy.latex(target)
    out_str = "({},{})".format(x1, y1) + "\\text{ and }" + "({},{})".format(x2, y2)
    return "\\overline{" + out_str + "}", sols


_CONSONANTS = list("bcdfghjkmnpqrstvwz")


def simplify_exponents(target, *args, **kwargs):
    sols = sympy.latex(target)
    n = random.choice([2, 3, 4])
    while True:
        ints = list_of_ints(target, n)
        if 0 not in ints:
            break
    # Guarantee at least one negative exponent: negate a non-last element
    # and add 2× its value to the last so the sum stays at target.
    if all(v > 0 for v in ints):
        idx = random.randint(0, len(ints) - 2)
        ints[-1] += 2 * ints[idx]
        ints[idx] = -ints[idx]
    random.shuffle(ints)
    out_str = ""
    for i in ints:
        power_string = "^{" + str(i) + "}" if i != 1 else ""
        out_str += "x{}".format(power_string)
    return "\\overline{" + out_str + "}", sols


def simplify_exponent_division(target, *args, **kwargs):
    var = random.choice(_CONSONANTS)
    sols = sympy.latex(target)

    # Denominator: 1-3 small positive exponents
    n_den = random.choice([1, 2, 3])
    den_exps = [random.randint(1, 4) for _ in range(n_den)]
    total_den = sum(den_exps)

    # Numerator exponents sum to target + total_den so that num - den = target
    total_num = target + total_den
    n_num = random.choice([2, 3])
    if total_num < n_num:
        num_exps = [1] * total_num if total_num > 0 else [1]
    else:
        cuts = sorted(random.sample(range(1, total_num), n_num - 1))
        cuts = [0] + cuts + [total_num]
        num_exps = [cuts[i + 1] - cuts[i] for i in range(len(cuts) - 1)]

    # Guarantee at least one negative exponent in the numerator: negate a
    # non-last element and add 2× its value to the last to keep the sum.
    if len(num_exps) >= 2 and all(e > 0 for e in num_exps):
        idx = random.randint(0, len(num_exps) - 2)
        num_exps[-1] += 2 * num_exps[idx]
        num_exps[idx] = -num_exps[idx]

    random.shuffle(num_exps)
    random.shuffle(den_exps)

    def term(exp):
        return var if exp == 1 else "{}^{{{}}}".format(var, exp)

    num_str = "".join(term(e) for e in num_exps)
    den_str = "".join(term(e) for e in den_exps)
    return "\\overline{\\frac{" + num_str + "}{" + den_str + "}}", sols


def percent_increase(target, *args, **kwargs):
    sols = sympy.latex(target)
    p = random.randint(10, 95)
    chooser = random.randint(1, 4)
    if chooser == 1:
        output = target / (1 + float(p) / 100)
        out_str = "{}\\%".format(p) + "\\text{ increase of }" + "{:.2f}".format(output)
    elif chooser == 2:
        output = target / (1 - float(p) / 100)
        out_str = "{}\\%".format(p) + "\\text{ decrease of }" + "{:.2f}".format(output)
    elif chooser == 3:
        output = target / (1 + float(p) / 100)
        out_str = "\\text{Add }" + "{}\\%".format(p) + "\\text{ to }" + "{:.2f}".format(output)
    elif chooser == 4:
        output = target / (1 - float(p) / 100)
        out_str = "\\text{Subtract }" + "{}\\%".format(p) + "\\text{ from }" + "{:.2f}".format(output)
    return "\\overline{" + out_str + "}", sols


def compound_interest(target, *args, **kwargs):
    r = random.randint(1, 12)
    t = random.randint(5, 50)
    amount = compound(1, r / 100.0, t)
    principle = target * 1000 / amount
    sols = sympy.latex(target)
    out_str = "${:0.2f}".format(principle) + "\\text{ for }" + "{}".format(t) + "\\text{ years at }" + "{}".format(r) + "\\text{% APR }"
    return "\\overline{" + out_str + "}", sols


def simple_scientific(target, *args, **kwargs):
    power = int(math.log10(target))
    coef = float(target) / float(10**power)
    sols = "$$" + sympy.latex(target) + "$$"
    outstr = "{}\\times10^{}".format(coef, power)
    return "\\overline{" + outstr + "}", sols


def intermediate_scientific(target, *args, **kwargs):
    power = int(math.log10(target))
    coef = float(target) / float(10**power)
    divisor = random.randint(0, 7)
    sols = "$$" + sympy.latex(target) + "$$"
    outstr = "\\frac{" + str(coef) + "\\times10^" + str(power + divisor) + "}{10^" + str(divisor) + "}"
    return "\\overline{" + outstr + "}", sols


def harder_scientific(target, *args, **kwargs):
    power = int(math.log10(target))
    coef = float(target) / float(10**power)
    divisor = random.randint(0, 7)
    sols = "$$" + sympy.latex(target) + "$$"
    outstr = "\\frac{" + str(coef) + "\\times10^" + str(power + divisor) + "}{" + str(10**divisor) + "}"
    return "\\overline{" + outstr + "}", sols
