from flask import Flask, render_template, request,send_file, redirect
from model import InputForm, ClueForm
from puzzlegen import puzzlesheet
from puzzlegen import crosswordsheet
from utils import *    
app = Flask(__name__)

from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@app.route("/puzzle", methods = ['GET','POST'])
def puzzle():
    categories=get_categories()
    form = ClueForm(request.form)
    return render_template('view.html', form=form, clue='defaulto',my_string="Wheeeee!", my_categories=categories)

@app.route("/clue_ideas",methods=['GET'])
def clue_ideas():
    return render_template('clue_ideas.html')

@app.route("/make_puzzle/,<string:puzzle_type>")
def make_puzzle(puzzle_type):
	global return_puzzle
	categories=get_categories()
	clue = request.args.get("clue")
	if categories[puzzle_type]['type']=='math':
		mypuzzlesheet = puzzlesheet.puzzlesheet("puzzle", "",clue, savetex=True)
		puzz=categories[puzzle_type]['filename'].lower()
		mypuzzlesheet.add_section(puzz, 28, "",puzzlesheet.instructions_map[puzz],rhs=0)
		mypuzzlesheet.write()
		return_puzzle="puzzle.pdf"
	else:
		mypuzzlesheet = crosswordsheet.crossword1d(categories[puzzle_type]['filename'], title=puzzle_type,clue=clue, savetex=True)
		mypuzzlesheet.add_section()
		mypuzzlesheet.write()
		return_puzzle=mypuzzlesheet.fname+".pdf"	
	return redirect('/return-files/')

@app.route('/return-files/')
@nocache
def return_files_tut():
	try:
		return send_file('tmp/'+return_puzzle, attachment_filename='puzzle.pdf')
	except Exception as e:
		return str(e)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5005,debug=True)
