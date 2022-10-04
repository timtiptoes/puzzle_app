import os
import re
import sympy
from sympy.parsing.sympy_parser import parse_expr
from sympy.polys.polytools import degree
from sympy import symbols,expand,factor,Poly


import random
from helper import *

def make_simple_addition_problem(target,*args,**kwargs):
    """
    """
    digits = range(0,25)

    while True:
        r1=random.choice(digits)
        if (r1<target):
            break
    r2 = target-r1
    c1=sympy.Symbol(str(r1))
    c2=sympy.Symbol(str(r2))
    lhs = c1 + c2
    
    sols = sympy.latex(target) 
    sols = "$$" + sols + "$$"
    outstr="\\overline{"+str(r1)+"+"+str(r2)+"}"
    print "about to return "+outstr
    print r1,r2
    return outstr, sols

def make_simple_multiplication_problem(target,*args,**kwargs):
    """
    """
    r1,r2 = get_smaller_coefficients(2)
    r3=target-r1*r2
    c1=sympy.Symbol(str(r1))
    c2=sympy.Symbol(str(r2))
    c3=sympy.Symbol(str(r3))
    lhs = c1 * c2 + c3
    
    sols = sympy.latex(target) 
    sols = "$$" + sols + "$$"
    if len(sols) == 0:
        return make_quadratic_eq()
    print "lhs:"
    print lhs

    #outstr=render(lhs).replace('\\cdot','\\times').replace("$$","")
    sign="+" if r3>=0 else ""
    outstr="\\overline{"+str(r1)+"\\times"+str(r2)+ sign +str(r3)+"}"
    print "about to return "+outstr
    print r1,r2,r3
    return outstr, sols

def make_simple_division_problem(target,*args,**kwargs):
    ints = range(2,14)
    c=random.choice(ints)
    outstr="\\frac{"+str(c*target)+"}{"+str(c)+"}"
    return "\overline{"+outstr+"}",[]

def make_fraction_addition_problem(target,*args,**kwargs):
    primes = [2,3,5,7,11,13]
    ints = range(2,14)
    these_primes=prime_factors(target)
    
    while True:

        while True:
            c=random.choice(primes)
            if c not in these_primes:
                break
        while True:
            f=random.choice(primes)
            if f not in these_primes and f != c:
                break
        while True:
            b=random.choice(ints)
            if b not in [c,f]:
                break
        e=target-b
        f1 = sympy.fraction(sympy.S(b)/sympy.S(c*f))
        f2 = sympy.fraction(sympy.S(e)/sympy.S(c*f))

    
        ap,bp=make_proper(f1[0],f1[1])
        dp,ep=make_proper(f2[0],f2[1])
        if bp!=0 and ep!=0 and f1[1] != f2[1]:
                break
    print "-------------"
    print "Below is trying to get "+str(target)
    print ":".join([str(i) for i in [target,c,f,b,e,ap,bp,dp,ep]])
    print str(bp)+"/"+str(c*f) +"+"+str(ep)+"/"+str(f*c)
    sign="+" if ep>=0 else "-"
    outstr=str(ap) if ap !=0 else ""
    outstr="\\frac{"+str(bp)+"}{"+str(f1[1])+"}"
    second_int = str(dp) if dp !=0 else ""
    outstr+=sign+second_int+"\\frac{"+str(abs(ep))+"}{"+str(f2[1])+"}"
    return "\\overline{"+outstr+"}",[]

def make_simplify_ratio_problem(target,*args,**kwargs):
    ints = range(2,14)
    c=random.choice(ints)
    while True:
            b=random.choice(ints)
            if b != c:
                break
    outstr="\\frac{"+str(c*target)+"}{"+str(c*b)+"}"
    return "\overline{"+outstr+"}",[]

def make_quadratic_eq(target, rhs = None, integer=[0, 1]):
    var=random.choice("pqrstuvwxyz")
    x = sympy.Symbol("x")
    f=random.randint(2,5)*random.choice([-1,1])
    f2=random.choice([-1,1])
    r1=target
    while r1==target:
        r1=random.randint(1,13)
    r2=target-r1
    expr = (f*x-r1*f)*(x-r2)
    expanded_expr = expand(expr)
    print "I chose {}, {}, and {}".format(f,r1,r2)
    ex = Poly(expanded_expr, x)
    a,b,c=tuple(ex.coeffs())
    print "I got {},{} and {}".format(a,b,c)
    out_str="{}{}^2{}{}{}".format(a,var,right_sign(b),var,right_sign(c))
    sols = sympy.latex(target) 
    sols = "$$" + sols + "$$"
    out_str="\\overline{"+out_str+"}"
    return out_str,sols

def two_digit_subtraction(target,*args,**kwargs):

    digits = range(50,99)

    
    r1=random.choice(digits)
    r2 = r1 - target
    c1=sympy.Symbol(str(r1))
    c2=sympy.Symbol(str(r2))
    lhs = r1 - r2
    
    sols = sympy.latex(target) 
    sols = "$$" + sols + "$$"
    outstr=stack_em(r1,r2,"-")
    print "about to return "+outstr
    print r1,r2

    outstr="\\begin{tabular}{ c c c } \
 cell1 & cell2 & cell3 \\\ \
 cell4 & cell5 & cell6 \\\ \
 cell7 & cell8 & cell9 \
    \\end{tabular}"
    return outstr, sols


def two_digit_subtraction(target,*args,**kwargs):

    digits = range(50,99)

    
    r1=random.choice(digits)
    r2 = r1 - target
    c1=sympy.Symbol(str(r1))
    c2=sympy.Symbol(str(r2))
    lhs = r1 - r2
    
    sols = sympy.latex(target) 
    sols = "$$" + sols + "$$"
    outstr=stack_em(r1,r2,"-")
    print "about to return "+outstr
    print r1,r2
    return outstr, sols

def two_digit_multiplication(target,*args,**kwargs):
 
    single_digits=range(1,10)
    trier=2
    while isPrime(trier):
        a=random.choice(single_digits)
        b=random.choice(single_digits)
        trier=1000*a+10*target+b
        
    p=prime_factors(trier)
    mx=max(p)
    p.remove(mx)
    rest=reduce(lambda x, y: x*y, p)

    sols = sympy.latex(target) 
    sols = "$$" + sols + "$$"
    outstr=stack_em(mx,rest,operator="\\times")
    print "about to return "+outstr
    return outstr, sols

def add_coins(target,*args,**kwargs):
    quarters=int(target/25)
    dimes=int(target/10)
    nickels=int(target/5)
    pennies=target
    
    number_words="one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twenty-one,twenty-two,twenty-three,twenty-four,twenty-five,twenty-six,twenty-seven".split(",")
    
    choices={}
    coins={'quarters':{'value':25,'singular':'quarter'},
           'dimes':   {'value':10,'singular':'dime'},
            'nickels':{'value':5,'singular':'nickel'},
            'pennies':{'value':1,'singular':'penny'}}

    
    total=target
    keys=coins.keys()
    indicies=range(4)
    purse={}
    while total>0:
        idx=random.choice(indicies)
        coin=keys[idx]
        value=coins[coin]['value']
        if total-value>=0:
            if coin in purse:
                purse[coin]+=1
            else:
                purse[coin]=1
            total-=value

    out_str="\\overline{"
    for coin in purse.keys():
        coin_name=coin if purse[coin]>1 else coins[coin]['singular']

        out_str+="\\textrm{"+number_words[purse[coin]-1]+" "+coin_name+"}"
        if coin==purse.keys()[0]:
            out_str+="}"

        if coin !=purse.keys()[-1]:
            out_str+="\\\\"

    print out_str
    return out_str,"$$ $$"

def exponents_problem(target,*args,**kwargs):
    list_of_perfect_powers=get_power_choices()
    constant=target-sum(list_of_perfect_powers)
    out_str=""
    for pp in list_of_perfect_powers:
        pp_pick=get_power_choice(pp)
        out_str+="{}^{}".format(pp_pick['base'],pp_pick['power'])
        if pp!=list_of_perfect_powers[-1]:
            out_str+="+"
    if constant>0:
        out_str+="+{}".format(constant)
    elif constant<0:
        out_str+="{}".format(constant)
    sols = sympy.latex(target) 
    sols = "$$" + sols + "$$"
    out_str="\\overline{"+out_str+"}"
    return out_str,sols

def roots_problem(target,*args,**kwargs):
    list_of_perfect_powers=get_power_choices()
    out_str=""
    base_sum=0
    for pp in list_of_perfect_powers:
        pp_pick=get_power_choice(pp)
        base_sum+=pp_pick['base']
        out_str+="\sqrt[{}]".format(pp_pick['power'])+"{"
        out_str+=str(pp)+"}"
        if pp!=list_of_perfect_powers[-1]:
            out_str+="+"
    constant=target-base_sum
    if constant>0:
        out_str+="+{}".format(constant)
    elif constant<0:
        out_str+="{}".format(constant)
    sols = sympy.latex(target) 
    sols = "$$" + sols + "$$"
    out_str="\\overline{"+out_str+"}"
    return out_str,sols

def simple_algebra(target,*args,**kwargs):
    coefficient=random.randint(1,13)
    rhs=random.randint(1,30)
    constant=rhs-coefficient*target
    out_coefficient=str(coefficient) if coefficient>1 else ""
    if constant>0:
        out_constant="+{}".format(constant)
    elif constant<0:
        out_constant="{}".format(constant)
        
    sols = sympy.latex(target) 
    out_str="{}x{}={}".format(out_coefficient,out_constant,rhs)
    out_str="\\overline{"+out_str+"}"
    return out_str,sols

def decimal_addition(target,num_places,*args,**kwargs):
    f=random.uniform(.1,.9)
    a=float(int(target*f*10**num_places))/10**num_places
    b=float(round((target-a)*10**num_places))/10**num_places
    sols = sympy.latex(target) 
    sols = "$$" + sols + "$$"
    #out_str="\\overline{"+"{}+{}".format(a,b)+"}"
    out_str=stack_em(a,b,'+')
    return out_str,sols

def single_decimal_addition(target,*args,**kwargs):
    return decimal_addition(target,2)

def determinant(target,*args,**kwargs):
 
    single_digits=range(1,10)
    trier=2
    while isPrime(abs(trier)):
        a=random.choice(single_digits)
        d=random.choice(single_digits)
        trier=a*d-target
        
    p=prime_factors(abs(trier))
    idx=random.randint(0,len(p)-1)
    p[idx]=p[idx]*numpy.sign(trier)
    b=random.choice(p)
    c=trier/b
    out_str="\\overline{\\begin{vmatrix}"+"{} & {} \\\ {} & {} ".format(a,b,c,d)+" \\end{vmatrix}}"
    sols = sympy.latex(target) 
    sols = "$$" + sols + "$$"
    return out_str,sols

def unit_conversion(target,allow_scientific=False,*args,**kwargs):
    systems={"Imperial":{"length":{"in":1.0,"ft":12.0,"yd":36.0,"miles":63360.0}, \
                         "volume":{"tsp":0.333333,"Tb":0.5,"oz":1,"pints":16.0,"quarts":32.0,"gallons":128.0}, \
                         "mass": {"oz":1.0,"lbs":16.0,"tons":32000.0}}, \
             "Metric":  {"length":{"mm":.03937,"m":39.37,"cm":0.3937,"kilometers":39370.0}, \
                     "volume":{"ml":0.033814,"cc":0.033814,"liters":33.814}, \
                     "mass":{"mg":3.5274e-5,"g":3.5274e-2,"kg":35.274}}} 
    counter=0
    conversion_factor=0.0
    computed_target=0.0
    
    while round(float(computed_target)*conversion_factor)!=target or ('E' in computed_target and not allow_scientific):

        source_system = random.choice(systems.keys())
        source_type = random.choice(systems[source_system].keys())
        source_unit = random.choice(systems[source_system][source_type].keys())
        dest_unit = source_unit
        while dest_unit==source_unit:
            dest_system = random.choice(systems.keys())
            dest_unit = random.choice(systems[dest_system][source_type].keys())    

        print "I want to convert {} to {} ".format(source_unit,dest_unit)

        factor_to_convert_source_unit_to_base=systems[source_system][source_type][source_unit]

        factor_to_convert_dest_unit_to_base=systems[dest_system][source_type][dest_unit]

        conversion_factor=factor_to_convert_source_unit_to_base / \
                          factor_to_convert_dest_unit_to_base 

        print "f1:{} f2:{} and of course conv:{}".format(factor_to_convert_source_unit_to_base,factor_to_convert_dest_unit_to_base,conversion_factor)
        source_figure=target/conversion_factor
        sols = sympy.latex(target) 
    #    out_str="{:.3f}".format(source_figure)
        computed_target=find_shortest(target,conversion_factor)
    computed_target=computed_target.rstrip("0") if "." in computed_target else computed_target
    out_str=computed_target + "\\ \\textrm{"+source_unit+"}\\ =\\ ?\\ \\textrm{"+dest_unit+"}"

    out_str="\\overline{"+out_str+"}"
    #    $\overline{25.153\ \textrm{yd}\ =\ ?\ \textrm{m}}$
    return out_str,sols
    
def add_negatives(target,*args,**kwargs):

    digits = range(-25,25)
    chosen_digits=[]
    chosen_operators=[]
    chosen_signed_alphas=[]
    while len(chosen_digits)<1:
        r1=random.choice(digits)
        r2=random.choice([-1,1])
        if r1 not in chosen_digits and -r1 not in chosen_digits:
            chosen_digits.append(r1)
            chosen_operators.append(r2)

#    print chosen_signs
        
    sols = sympy.latex(target) 
    sols = "$$" + sols + "$$"
    outstr=str(chosen_digits[0])
    running_total=chosen_digits[0]
    for i in range(1,len(chosen_digits)):
        if chosen_operators[i]==-1:
            op="-"
            running_total-=chosen_digits[i]
        else:
            op="+"
            running_total+=chosen_digits[i]
        outstr+=op+str(chosen_digits[i])
    final=target-running_total
    if final>0:
        outstr+="+"
    outstr+=str(final)

    outstr="\\overline{"+outstr+"}"
    return outstr, sols

def common_difference(target):
    #decrement=max(1,int(0.5+float(target)/5))
    decrement=random.randint(3,9)
    sign=random.choice([-1,1])
    ret_list=[]
    next_num=target-sign*decrement
    while len(ret_list)<5:
        ret_list.append(next_num)
        next_num-=sign*decrement
    ret_list_str=[str(i) for i in sorted(ret_list,reverse=(sign<1))]
    ret_list_str.append('x')
    outstr=",".join(ret_list_str)
    return "\\overline{"+outstr+"}",[]

def common_ratio(target):
    starting_num=random.randint(3,4)
    ratio=random.choice([0.25,0.5,2,3,4,5])
    if (ratio<1):
        next_num=starting_num*(1/ratio)**4
    else:
        next_num=starting_num
    ret_list=[]
    while len(ret_list)<4:
        ret_list.append(int(next_num))
        next_num*=ratio
    pre_ret_list=sorted(ret_list,reverse=ratio<1)
    correction=target-pre_ret_list[-1]
    if correction<0:
        correction_text=" then subtract "+str(abs(int(correction)))
    elif correction>0:
        correction_text = " then add "+str(abs(int(correction)))
    else:
        correction_text=""
    pre_ret_list.pop()
    pre_ret_list.append('x')
    ret_list_str=[str(i) for i in pre_ret_list]
    
    outstr=",".join(ret_list_str)+"\\text{"+correction_text+"}"
    return "\\overline{"+outstr+"}",[] 

def simple_series(target,*args,**kwargs):
    choice=random.choice(['heads','tails'])
    if choice=='heads':
        return common_difference(target)
    else:
        return common_ratio(target)




def basetoStr(n,base):
   convertString = "0123456789ABCDEF"
   if n < base:
      return convertString[n]
   else:
      return basetoStr(n//base,base) + convertString[n%base]

def convert_base(target,*args,**kwargs):

    digits = range(2,9)
    base=random.choice(range(2,9))
    outstr = "{}_{}".format(basetoStr(target,base),base)
    outstr = outstr + " = ?_{10}"
    sols = sympy.latex(target) 
    sols = "$$" + sols + "$$"
    outstr="\\overline{"+outstr+"}"
    return outstr, sols

def linear_system(target,*args,**kwargs):
    x=choose_someint(5)
    y=target - x
    coeff11=choose_someint(6)
    coeff12=choose_someint(6)
    sign1="+" if coeff12>0 else ''
    constant1=coeff11*x+coeff12*y
    print("{},{}".format(x,y))
    coeff21=coeff11
    while coeff21==coeff11:
        coeff21=choose_someint(9)
    coeff22=choose_someint(9)
    constant2=coeff21*x+coeff22*y
    sign2="+" if coeff22>0 else ''
    print("{}x {} {}y = {}".format(coeff11,sign1,coeff12,constant1))
    print("{}x {} {}y = {}".format(coeff21,sign2,coeff22,constant2))
    
    out_str=stack_lines("{}x {} {}y = {}".format(coeff11,sign1,coeff12,constant1),"{}x {} {}y = {}".format(coeff21,sign2,coeff22,constant2))
    #out_str="\\begin{array}{c}"+"{}x +{}y".format(coeff11,coeff12)+" & = & "+"{}".format(constant1)+"\\"
    #out_str+="{}x +{}y".format(coeff21,coeff22)+" & = & "+"{}".format(constant2)

#    out_str+="\\end{array}"
    sols = sympy.latex(target)
#    out_str="\\overline{"+out_str+"}"

    return out_str,sols

def find_slope(target,*args,**kwargs):
    b=choose_someint(9)
    x1=choose_someint(10)
    y1=simple_line(target,x1,b)
    
    x2=x1
    while x1==x2:
        x2=choose_someint(10)
    y2=simple_line(target,x2,b)
    #print("({},{}) and ({},{})".format(x1,y1,x2,y2))
    sols = sympy.latex(target) 
    out_str="({},{})".format(x1,y1)+"\\text{ and }"+"({},{})".format(x2,y2)
    out_str="\\overline{"+out_str+"}"
    return out_str,sols

def simplify_exponents(target,*args,**kwargs):
    sols = sympy.latex(target) 
    out_str=""
    ints=list_of_ints(target,random.choice([2,3,4]))
    random.shuffle(ints)
    print(ints)
    power_strings=[]
    for i in ints:
        power_string="^{"+str(i)+"}" if i!=1 else ""
        print("given {} I compute {}".format(i,power_string))
        #power_strings.append(power_string)
        out_str+="x{}".format(power_string)
    out_str="\\overline{"+out_str+"}"
    return out_str,sols  

def compound_interest(target,*args,**kwargs):
    r=random.randint(1,12)
    t=random.randint(5,50)
    amount=compound(1,r/100.0,t)
    principle=target*1000/amount
    sols = sympy.latex(target) 
    #$111.71 for 3 years at 5% APR
    out_str="${:0.2f}".format(principle)+"\text{ for }"+ "{}".format(t)+"\text{ years at }"+"{}".format(r)+"\text{% APR }"
    out_str="\\overline{"+out_str+"}"
    return out_str,sols


if __name__ == "__main__":
    print compound_interest(14)



