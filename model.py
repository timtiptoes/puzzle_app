from wtforms import Form, FloatField, TextField, RadioField, validators

class InputForm(Form):
    clue = TextField(validators=[validators.InputRequired()],default="I hold legos")
    puzzle_type=RadioField('Label', choices=[
    	('simple_addition','$$\\texttt{Simple addition: }3+5$$'),
      ('simple_division_problem','$$\\texttt{Simple division: }36\\div3$$'),
    	('multiplication_then_addition','$$\\texttt{multiplication and addition: } 3\\times5 + 3$$'),
      ('simplify_ratio','$$\\texttt{use numerator of reduced fraction: }\\frac{11}{65} + \\frac{1}{5}$$'),
    	('fraction_addition','$$\\texttt{use numerator of sum: }\\frac{2}{7}-\\frac{3}{14}$$'),
      ('quadratic_equations','$$\\texttt{add roots :}x^2-14x+45$$'),
      ('two_digit_subtraction','84-63')])

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