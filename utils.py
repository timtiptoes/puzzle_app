import os

def get_categories():
  math_puzzles={}
  crossword_puzzles={}
  all_puzzles={}

  crossword_puzzle_list = [x for x in os.listdir('static/') if x.endswith(".csv")]

  for p in crossword_puzzle_list:
    f=p.replace(".csv","")
    key=f.replace("_"," ")
    crossword_puzzles[key]={'filename':f,'type':'crossword'}

  math_puzzle_list=['simple_addition','multiplication_then_addition','fraction_addition','simple_division_problem','simplify_ratio','two_digit_subtraction','two_digit_multiplication','add_coins','exponents_problem','simple_algebra','single_decimal_addition','quadratic_equations' ,'roots_problem' ,'determinant']

  for p in math_puzzle_list:
    key=p.replace("_"," ")
    math_puzzles[key]={'filename':p,'type':'math'}


  all_puzzles=merge_two_dicts(crossword_puzzles,math_puzzles)

  return all_puzzles

def get_display_categories():
	categories=get_categories()
	tups=[(x,'$$\\texttt{'+x+'}$$') for x in categories.keys()]
	return tups

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

if __name__ == "__main__":
       print get_display_categories()