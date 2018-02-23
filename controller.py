from flask import Flask, render_template, request,send_file, redirect
from model import InputForm
from puzzlegen import puzzlesheet
from puzzlegen import crosswordsheet
    
app = Flask(__name__)

@app.route('/puzzle', methods=['GET', 'POST'])
def index():
	global return_puzzle
	form = InputForm(request.form)
	if request.method == 'POST' and form.validate():
		clue = form.clue.data
		puzzle_type = form.puzzle_type.data
		print puzzle_type
		if puzzle_type not in ['Harry Potter','Star Wars','American History','Mythology','Shakespeare','The Bible','Science','Animals']:
			mypuzzlesheet = puzzlesheet.puzzlesheet("puzzle", "",clue, savetex=True)
			mypuzzlesheet.add_section(puzzle_type, 6, "",puzzlesheet.instructions_map[puzzle_type],rhs=0)
			mypuzzlesheet.write()
			return_puzzle="puzzle.pdf"
		else:
			mypuzzlesheet = crosswordsheet.crossword1d(puzzle_type, title=puzzle_type,clue=clue, savetex=True)
			mypuzzlesheet.add_section()
			mypuzzlesheet.write()
			return_puzzle=mypuzzlesheet.fname+".pdf"	
		return redirect('/return-files/')

	else:
		clue = None

	return render_template("view.html", form=form, clue='defaulto')

@app.route('/return-files/')
def return_files_tut():
	try:
		return send_file('tmp/'+return_puzzle, attachment_filename='puzzle.pdf')
	except Exception as e:
		return str(e)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=6555,debug=True)
