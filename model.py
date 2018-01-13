from wtforms import Form, FloatField, TextField, RadioField, validators

class InputForm(Form):
    clue = TextField(validators=[validators.InputRequired()])
    puzzle_type=RadioField('Label', choices=[('Simple_addition','3+5'),('Decode','4 x 3')])

'''
_problems_map = {"Quadratic equations" : make_quadratic_eq,
                 "Linear equations" : make_linear_eq,
                 "Limit of polynomial ratio" : make_poly_ratio_limit,
                 "Decode": make_simple_multiplication_problem,
                 "Fraction_addition": make_fraction_addition_problem,
                 "Simple_addition": make_simple_addition_problem,
                 "Simplify quadratic ratio" : make_rational_poly_simplify}
'''