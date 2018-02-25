from wtforms import Form, FloatField, TextField, RadioField, validators
from utils import *

class InputForm(Form):
    clue = TextField(validators=[validators.InputRequired()],default="I hold legos")
    display_categories=get_display_categories()
    puzzle_type=RadioField('Label', choices=[
    	('simple_addition','$$\\texttt{simple addition: e.g. }3+5$$'),
      ('simple_division_problem','$$\\texttt{simple division: e.g. }36\\div3$$'),
    	('multiplication_then_addition','$$\\texttt{multiplication and addition: e.g. } 3\\times5 + 3$$'),
      ('simplify_ratio','$$\\texttt{use numerator of reduced fraction: e.g. }\\frac{11}{65} + \\frac{1}{5}$$'),
    	('fraction_addition','$$\\texttt{use numerator of sum: e.g. }\\frac{2}{7}-\\frac{3}{14}$$'),
      ('two_digit_subtraction','$$\\texttt{find difference : e.g. }84-63$$'),
      ('two_digit_multiplication','$$\\texttt{take inner two digits of product : e.g. }691 \\times 2$$'),
      ('add_coins','$$\\texttt{add coins: e.g. find total value of 1 dime, 2 nickels, 3 pennies}$$'),
      ('exponents_problem','$$\\texttt{add exponents : e.g. }2^3+4^2-5$$'),
      ('roots_problem','$$\\texttt{add roots : e.g. }\\sqrt{121}+\\sqrt[3]{8}-5$$'),
      ('simple_algebra','$$\\texttt{find x : e.g. } 4x+5=17$$'),
      ('single_decimal_addition','$$\\texttt{add decimals : e.g. } 3.4+2.6$$'),
      ('quadratic_equations','$$\\texttt{add quadratic equation roots : e.g. }x^2-14x+45$$')]+display_categories)
#
'''
,('The Bible','$$\\texttt{The Bible}$$')
      ('determinant_problem','$$\\texttt{find determinant :}\\begin{vmatrix} 5 & 3 \\\ -5 & 1  \\end{vmatrix}$$')
To add a new problem type:
  1) add function to lib/algebra.py
        given a target it only has to return a latex string something like 
           \overline{\frac{2}{77}+\frac{1}{7}}
  2) add to above list

  3) add it to _problems_map at top of puzzlesheet.py
,
      ('two_digit_subtraction','84-63')
'''