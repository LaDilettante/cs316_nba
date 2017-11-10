from flask import Flask, render_template, request, json
from wtforms import Form, SelectField

app = Flask(__name__)

class PlayerForm(Form):
	#standin for DB integration with all player choices
	c = [('HG', 'Harry Giles'), ('GA', 'Grayson Allen')]
	choosePlay = SelectField(u'Player Choice', choices=c)

@app.route("/")
def main():
	#another standin to be implemented
	nbaCount = 300
	form = PlayerForm(request.form)
	return render_template('index.html', playerCount=nbaCount, form=form)

@app.route('/getPrediction', methods=['POST'])
def getPrediction():
	_points = request.form['inputPoints']
	if _points:
		return json.dumps({'html':'<span>All fields good !!</span>'})
    	else:
        	return json.dumps({'html':'<span>Enter the required fields</span>'})

if __name__ == "__main__":
	app.run()
