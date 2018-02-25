import os

def get_categories():
	arr_txt = [x for x in os.listdir('static/') if x.endswith(".csv")]
	categories={x.replace("_"," ").replace(".csv",""):x for x in arr_txt}
	return categories

'''
     ('Harry Potter','$$\\texttt{Harry Potter}$$'),
      ('Star Wars','$$\\texttt{Star Wars}$$'),
      ('American History','$$\\texttt{American History}$$'),
      ('Mythology','$$\\texttt{Mythology}$$'),
      ('Shakespeare','$$\\texttt{Shakespeare}$$'),
      ('The Bible','$$\\texttt{The Bible}$$'),
      ('Science','$$\\texttt{Science}$$'),
      ('Animals','$$\\texttt{Animals}$$')])
      ('First ', '$$\\texttt{Firstes}$$'), ('Religion', '$$\\texttt{Religion}$$')


'''

def get_display_categories():
	categories=get_categories()
	tups=[(x,'$$\\texttt{'+x+'}$$') for x in categories.keys()]
	return tups

if __name__ == "__main__":
        get_display_categories()