from flask import Flask, render_template, request,send_file, redirect
from model import InputForm
from puzzlegen import puzzlesheet

    
app = Flask(__name__)

@app.route('/hw3', methods=['GET', 'POST'])
def index():
	form = InputForm(request.form)
	if request.method == 'POST' and form.validate():
		clue = form.clue.data
		puzzle_type = form.puzzle_type.data
		mypuzzlesheet = puzzlesheet.puzzlesheet("tmp/tim_puzzle", "Algebra 101 worksheet 1",clue, savetex=True)
		mypuzzlesheet.add_section(puzzle_type, 6, "Linear equations","Use the numerator of the resulting improper fraction to lookup the letter above",rhs=0)
		mypuzzlesheet.write()
		return redirect('/return-files/')

	else:
		clue = None

	return render_template("view.html", form=form, clue='defaulto')

@app.route('/return-files/')
def return_files_tut():
	try:
		return send_file('tmp/tim_puzzle.pdf', attachment_filename='ohhey.pdf')
	except Exception as e:
		return str(e)


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
