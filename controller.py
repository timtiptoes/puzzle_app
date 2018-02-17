from flask import Flask, render_template, request,send_file, redirect
from model import InputForm
from puzzlegen import puzzlesheet
    
app = Flask(__name__)


@app.route('/puzzle', methods=['GET', 'POST'])
def index():
	form = InputForm(request.form)
	if request.method == 'POST' and form.validate():
		clue = form.clue.data
		puzzle_types = form.puzzle_types.data
		tests = request.form.getlist('tests')

		mypuzzlesheet = puzzlesheet.puzzlesheet("tmp/puzzle", "",clue, savetex=True)
		#problems_list=[puzzlesheet._problems_map[i] for i in puzzle_types]
		mypuzzlesheet.add_section(puzzle_types, 6, "","Solve each to find the letter above",rhs=0)
		mypuzzlesheet.write()
		return redirect('/return-files/')

	else:
		clue = None

	return render_template("view.html", form=form, clue='defaulto')

@app.route('/return-files/')
def return_files_tut():
	try:
		return send_file('tmp/puzzle.pdf', attachment_filename='puzzle.pdf')
	except Exception as e:
		return str(e)


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
