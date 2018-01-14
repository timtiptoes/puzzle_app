from wtforms import Form, FloatField, TextField, RadioField, validators

class InputForm(Form):
    clue = TextField(validators=[validators.InputRequired()])
    puzzle_type=RadioField('Label', choices=[\
    	('Simple_addition','3+5'),\
    	('Decode','Simple multiplication and then addition e.g. 4x3+2'),\
    	('Fraction_addition','Fraction addition e.g. 2/3 + 3/8'),\
    	('Quadratic equations','Quadratic equation'),
        ('make_big_division_problem','Fraction simplification')])

'''
To add a new problem type:
  add function to lib/algebra.py
    given a target it only has to return something like 
         \overline{\frac{2}{77}+\frac{1}{7}}
  add it to lib/init.py
  add it to _problems_map at top of puzzlesheet.py
'''