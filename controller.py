from flask import Flask, render_template, request,send_file, redirect
from model import InputForm, ClueForm
from puzzlegen import puzzlesheet
from puzzlegen import crosswordsheet
from utils import *    
app = Flask(__name__)



@app.route("/puzzle")
def puzzle():
    categories=get_categories()
    form = ClueForm(request.form)
    return render_template('view.html', form=form, clue='defaulto',my_string="Wheeeee!", my_categories=categories)

@app.route("/make_puzzle/,<string:puzzle_type>")
def make_puzzle(puzzle_type):
	global return_puzzle
	categories=get_categories()
	clue = request.args.get("clue")
	if categories[puzzle_type]['type']=='math':
		mypuzzlesheet = puzzlesheet.puzzlesheet("puzzle", "",clue, savetex=True)
		puzz=categories[puzzle_type]['filename'].lower()
		print "I want to do {}".format(puzz)
		mypuzzlesheet.add_section(puzz, 6, "",puzzlesheet.instructions_map[puzz],rhs=0)
		mypuzzlesheet.write()
		return_puzzle="puzzle.pdf"
	else:
		mypuzzlesheet = crosswordsheet.crossword1d(categories[puzzle_type]['filename'], title=puzzle_type,clue=clue, savetex=True)
		mypuzzlesheet.add_section()
		mypuzzlesheet.write()
		return_puzzle=mypuzzlesheet.fname+".pdf"	
	return redirect('/return-files/')

@app.route('/return-files/')
def return_files_tut():
	try:
		return send_file('tmp/'+return_puzzle, attachment_filename='puzzle.pdf')
	except Exception as e:
		return str(e)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
