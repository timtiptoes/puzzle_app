from wtforms import Form, FloatField, TextField, RadioField, validators,widgets,SelectMultipleField


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class InputForm(Form):
    clue = TextField(validators=[validators.InputRequired()],default="I hold legos")
    puzzle_types=MultiCheckboxField('Label', choices=[
    	('simple_addition','$$\\texttt{simple addition: }3+5$$'),
      ('simple_division_problem','$$\\texttt{simple division: }36\\div3$$'),
    	('multiplication_then_addition','$$\\texttt{multiplication and addition: } 3\\times5 + 3$$'),
      ('simplify_ratio','$$\\texttt{use numerator of reduced fraction: }\\frac{11}{65} + \\frac{1}{5}$$'),
    	('fraction_addition','$$\\texttt{use numerator of sum: }\\frac{2}{7}-\\frac{3}{14}$$'),
      ('two_digit_subtraction','$$\\texttt{find difference :}84-63$$'),
      ('two_digit_multiplication','$$\\texttt{take inner two digits of product :}691 \\times 2$$'),
      ('add_coins','$$\\texttt{add coins: find total value of 1 dime, 2 nickels, 3 pennies}$$'),
      ('exponents_problem','$$\\texttt{add exponents :}2^3+4^2-5$$'),
      ('simple_algebra','$$\\texttt{find x :} 4x+5=17$$'),
      ('single_decimal_addition','$$\\texttt{add decimals :} 3.4+2.6$$'),
      ('simplify_exponents','$$\\texttt{simplify exponents :}x^3x^2$$'),
      ('scaling_rule',"$$\\texttt{find scaling factor :}5x=25$$")])


#,      ('quadratic_equations','$$\\texttt{add roots :}x^2-14x+45$$')
'''
To add a new problem type:
  1) add function to lib/algebra.py
        given a target it only has to return a latex string something like 
           \overline{\frac{2}{77}+\frac{1}{7}}
  2) add to above list

  3) add it to _problems_map at top of puzzlesheet.py
,
      ('two_digit_subtraction','84-63')
'''