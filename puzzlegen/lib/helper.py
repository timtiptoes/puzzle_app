import sympy
import numpy
import random
from string import ascii_lowercase
from string import ascii_uppercase
from copy import copy

# gather up alphanumeric charectors we might want to use for variable names
alpha = [i for i in ascii_uppercase + ascii_lowercase]
# remove the ones that might be confusing in a problem
alpha.remove("l")
alpha.remove("o")
alpha.remove("O")
alpha.remove("I")
alpha.remove("i")
# gather up numerical digits we might want to use for coefficients
# nothing special about -26 to 26, other than it matches the number of chars
# above
digits = range(-26,26)
# make a list of the nums above, but with zero removed. This way we know we
# can always guarantee selection of a non-zero digit (so the degree of a
# polynomial in an equation is at least a certain value)
digits_nozero = range(-26,26)
digits_nozero.remove(0)

powers={4:[{'base':2,'power':2}],
          8:[{'base':2,'power':3}],
          9:[{'base':3,'power':2}],
          16:[{'base':2,'power':4},
              {'base':4,'power':2}],
          25:[{'base':5,'power':2}],
          27:[{'base':3,'power':3}],
          32:[{'base':2,'power':5}],
          36:[{'base':6,'power':2}],
          49:[{'base':7,'power':2}],
          64:[{'base':2,'power':7},
              {'base':4,'power':3},
              {'base':8,'power':2}],
          81:[{'base':9,'power':2}],
          100:[{'base':10,'power':2}],
          121:[{'base':11,'power':2}],
          125:[{'base':5,'power':3}],
          144:[{'base':12,'power':2}],
          169:[{'base':13,'power':2}]}

def shuffle(x):
    x = list(x)
    random.shuffle(x)
    return x

def get_smaller_coefficients(n, exclude=["x", "X"], first_nonzero=True, var_coeffs=False, 
                        reduce=False):
    """
    Helper function to generate "good" coefficients for problems
    """
    digits_smaller = range(3,12)
    digits_nozero_smaller = range(3,12)
    #digits_nozero_smaller.remove(0)
    if var_coeffs:
        selection = copy(digits_nozero_smaller + alpha)
        for i in exclude:
            selection.remove(i)
    else:
        selection = digits_nozero_smaller
    coeffs = []
    for i in xrange(n):
        c = random.choice(selection)
        if isinstance(c, str):
            c = sympy.Symbol(c)
        if reduce and random.randint(0,1):
            c = 0
        coeffs.append(c)
    if first_nonzero and coeffs[0] == 0:
        coeffs[0] = random.choice(selection)
    return coeffs

def layout_lines(clue,linewidth):
    words=clue.split(" ")    
    lines=[]
    line=""
    for word in words:
        if len(line+" "+word)>linewidth:
            lines.append(line.strip().ljust(linewidth, " "))
            line=word
        else:
            line += " "+ word
    lines.append(line.strip().ljust(linewidth, " "))
    return lines

def get_coefficients(n, exclude=["x", "X"], first_nonzero=True, var_coeffs=False, 
                        reduce=True):
    """
    Helper function to generate "good" coefficients for problems
    """
    if var_coeffs:
        selection = copy(digits_nozero + alpha)
        for i in exclude:
            selection.remove(i)
    else:
        selection = digits_nozero
    coeffs = []
    for i in xrange(n):
        c = random.choice(selection)
        if isinstance(c, str):
            c = sympy.Symbol(c)
        if reduce and random.randint(0,1):
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
    """
    Puts $ at the beginning and end of a latex expression.
    lhs : if we want to render something like: $x = 3 + 5$, set the left hand 
          side here
    """
    left = "$$"
    if lhs:
        left = "$$%s =" % lhs
#    return ''.join([left, sympy.latex(expr), "$$"])
    return sympy.latex(expr)

def make_proper(numer,denom):
    #given numer and denom return proper fraction
    remainder = abs(numer) % denom
    whole=(abs(numer)-remainder)/denom 
    return whole,cmp(numer,0)*remainder

def isPrime(n):
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False

    return True

def stack_em(x,y,operator='-'):
    import math
    a=str(x)
    b=str(y)

    length=len(a)

    first_line='9'*(5-length)
    second_line='9'*(3-length)


    out_str='\\overline{\\begin{array}{c}\\phantom{\\times'+first_line+'}'+a+'\\phantom{\\times9}\\\\\phantom{\\times'+second_line+'}\\underline{'+operator+b+'}\\phantom{\\times9}\\end{array}}'
   
    return out_str

def stack_lines(x,y):
    import math
    a=str(x) if isinstance(x, int) else x
    b=str(y) if isinstance(y, int) else y

    length=len(a)

    first_line='9'*(5-length)
    second_line='9'*(3-length)


    out_str='\\overline{\\begin{array}{c}\\phantom{\\times'+first_line+'}'+a+'\\phantom{\\times9}\\\\\phantom{\\times'+second_line+'}'+b+'\\phantom{\\times9}\\end{array}}'
    print("****************\n"+out_str)
    return out_str

def get_power_choices():
    num_powers=random.randint(1,3)
    pick=random.choice(powers.keys())
    picks=[]
    while pick not in picks and len(picks)<num_powers:
        picks.append(pick)
        pick=random.choice(powers.keys())

    return picks
                         
def get_power_choice(perfect_power):
    #given a perfect power, return one of the choices
    pick=random.choice(powers[perfect_power])
    return pick

def right_sign(x):
    if x>0:
        out="+{}".format(x)
    elif x<0:
        out=str(x)
    else:
        out=""
    return out

def find_shortest(target,conversion_factor):
    mantissa_target="{:.12E}".format((target)/conversion_factor).split('E')[0]
    mantissa_lower="{:.12E}".format((target-0.49)/conversion_factor).split('E')[0]
    mantissa_upper="{:.12E}".format((target+0.49)/conversion_factor).split('E')[0]
    print "{} < {} < {}".format(mantissa_lower,mantissa_target,mantissa_upper)
    shortest_lower=find_shortest_common_string(mantissa_lower,mantissa_target)
    shortest_upper=find_shortest_common_string(mantissa_upper,mantissa_target)
    shortest=min(shortest_upper,shortest_lower)
    print "{} {}".format(shortest_lower,shortest_upper)
    exponent="{:.12E}".format((target)/conversion_factor).split('E')[1]   
    
    if int(exponent)>-3:
        ret_format_str="{:0."+str(shortest+2)+"f}"
        ret_str=ret_format_str.format(float(mantissa_target[0:shortest+2]+"E"+exponent))
        if int(float(ret_str))==float(ret_str):
            ret_format_str="{:0.0f}"
            ret_str=ret_format_str.format(float(mantissa_target[0:shortest+2]+"E"+exponent))
        return ret_str
    
    return mantissa_target[0:shortest+2]+"E"+exponent


def find_shortest_common_string(s1,s2):
    if len(s1)<=len(s2):
        first_one=s1
        second_one=s2
    else:
        first_one=s2
        second_one=s1
    
    for i in range(len(first_one)):
        if first_one[i]!=second_one[i]:
            return i-1
    return -1

def choose_someint(rng):
    #I want to choose some non-zero integer
    x=0
    while x==0:
        x=random.randint(-rng,rng)
    return x

def simple_line(m,x,b,*args,**kwargs):
    return m*x+b

def list_of_ints(tot,n):
    #return a list of n ints that sum to tot
    ints=[]
    someint=0
    while len(ints)<n:
        someint=choose_someint(10)
        if someint not in ints:
            ints.append(someint)
            
    ints.append(tot-sum(ints))
    return ints

def simplify_exponents(target,*args,**kwargs):
    sols = sympy.latex(target) 
    out_str=""
    ints=random.shuffle(list_of_ints(target,random.choice([2,3,4])))
    print(ints)
    power_strings=[]
    for i in ints:
        power_string="^{"+str(i)+"}" if i!=1 else ""
        print("given {} I compute {}".format(i,power_string))
        #power_strings.append(power_string)
        out_str+="x{}".format(power_string)
    out_str="\\overline{"+out_str+"}"
    return out_str,sols  

def compound(p,r,t,n=12.0):
    a=p*(1+r/n)**(n*t)
    return a