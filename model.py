from wtforms import Form, FloatField, TextField, RadioField, validators

class InputForm(Form):
    clue = TextField(validators=[validators.InputRequired()])
    puzzle_type=RadioField('Label', choices=[
    	('simple_addition','Simple addition e.g. 3+5'),
        ('simple_division_problem','Fraction simplification'),
    	('multiplication_then_addition','Simple multiplication and then addition e.g. 4x3+2'),
        ('simplify_ratio','Simplify ratio'),
    	('fraction_addition','Fraction addition e.g. 2/3 + 3/8'),
        ('quadratic_equations','Quadratic equations')])

'''
To add a new problem type:
  1) add function to lib/algebra.py
        given a target it only has to return a latex string something like 
           \overline{\frac{2}{77}+\frac{1}{7}}
  2) add to above list

  3) add it to _problems_map at top of puzzlesheet.py
'''