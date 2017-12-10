from flask import Flask, render_template, request, redirect, g
from wtforms import Form, IntegerField, SelectField,  validators
import pickle
import sqlite3
import numpy

app = Flask(__name__)

unpickled = False

rfModel = None
rfModelTeam = None

nnModel = None
nnModelTeam = None

userInput = None

finalizedStats = [0,0,0,0,0,0,0,0,0,0,0,0]

DATABASEPATH = './cs316_nba/data/database.sqlite'

DATABASE = None

playerDict = {}

teamDict = {}

playersYear = '2014'

existingPlayersList = []

def getDatabase():
	global DATABASE
	DATABASE =  sqlite3.connect(DATABASEPATH)
	


def getStatsFromPlayerChoice(playerChosen):
	cursor = DATABASE.cursor()
	

def getExistingCollegePlayers():
	global DATABASE
	cursor = DATABASE.cursor()
	#year = (2015,)
	strng = "SELECT DISTINCT Player FROM ncaa WHERE Year='" + year + "' ORDER BY PLAYER"
	print(playersYear)
	#cursor.execute("SELECT DISTINCT Player FROM ncaa WHERE Year='2014' ORDER BY Player")
	cursor.execute(strng)
	rows =(cursor.fetchall())
	players = []
	for p in rows:
		name = p[0]
		tup = (p[0], name)
		#print(tup)
		global playerDict
		playerDict[name] = p
		players.append(tup)
	return players


def getExistingTeams():
	global DATABASE
	cursor = DATABASE.cursor()
	cursor.execute("SELECT DISTINCT Team FROM ncaa ORDER BY Team")
	rows = (cursor.fetchall())
	teams = []
	for r in rows:
		teamName = r[0]
		tup = (r[0], teamName)
		global teamDict
		teamDict[teamName] = r
		teams.append(tup)
	return teams



class BasketballForm(Form):
	#need to have position
	getDatabase()
	positionChoices = [('None', 'Select Position'), ('G', ' Guard'), ('F', 'Forward'), ('C', 'Center')]
	position = SelectField('Player Position', [validators.InputRequired()], choices=positionChoices)
	points= IntegerField('Points', [validators.Optional()], render_kw={"placeholder":"Points"})
	assists= IntegerField('Assists', [validators.Optional()], render_kw={"placeholder":"Assists"})
	rebounds= IntegerField('Rebounds', [validators.Optional()], render_kw={"placeholder":"Rebounds"})
	blocks = IntegerField('Blocks', [validators.Optional()], render_kw={"placeholder":"Blocks"})
	steals = IntegerField('Steals', [validators.Optional()], render_kw={"placeholder":"Steals"})


	existingTeams = getExistingTeams()
	existingTeams.insert(0, ('Select Team', 'Select Team'))
	team = SelectField(u'Existing NCAA Teams', choices=existingTeams, default='Select Team')
	
	playerYears = [(str(i), str(i)) for i in range(2002,2015)]
	playerYears.insert(0, ('Select Year', 'Select Year'))
	playerYear = SelectField(u'College Players for Year', [validators.Optional()], choices=playerYears, default='Select Year')

	existingPlayers2 = getExistingCollegePlayers()
	existingPlayers2.insert(0,('Select Player', 'Select Player'))
	playerChoice= SelectField(u'Existing College Players', choices=existingPlayers2, default='Select Player')

@app.route('/', methods=['POST', 'GET'])
def index():
	statsDict = {}
	statsDict['PTS'] = -1
	statsDict['AST'] = -1
	statsDict['RBD'] = -1
	statsDict['STL'] = -1
	statsDict['BLK'] = -1
	statsDict['POS'] = "C"
	statsDict['TEAM'] = "None"
	form=BasketballForm(request.form, "2014")
	print("-----------------------------")
	print(form.validate())
	print(form.position.data)
	print(form.playerChoice.data)
	if form.validate() and (form.position.data != 'None' or form.playerChoice.data != 'Select Player'):
		#change global var userInput
		#need steals and blocks

		print("enters here?")
		if (form.position == 'Select Position'):
			print("something")
		if request.form["points"]:
			statsDict["PTS"] = float(request.form["points"])
		if request.form["assists"]:
			statsDict["AST"] = float(request.form["assists"])
		if request.form["rebounds"]:
			statsDict["RBD"] = float(request.form["rebounds"])
		if form.position != 'None':
			statsDict['POS'] = form.position.data
		
		filledStats = fillInEmptyStats(statsDict)
		if form.playerChoice.data != 'Select Player':
			filledStats = getStatsOfChosenPlayer(form.playerChoice.data, filledStats)
		transposeDictToArray(filledStats)

		return hello()
	print("else it goes here")
	print(form.playerChoice.data)
	if (form.playerYear.data!='Select Year'):
		playersYear = form.playerYear.data[0]
	form = BasketballForm(request.form)
	return render_template('index.html', ballForm=form)

def transposeDictToArray(statsDict):
	#[[points, rebounds, assists, steals, blocks, C, C&F, F, F&C, F&G, G, G&F]]
	finalizedStats[0] = statsDict["PTS"]
	finalizedStats[1] = statsDict["RBD"]
	finalizedStats[2] = statsDict["AST"]
	finalizedStats[3] = statsDict["STL"]
	finalizedStats[4] = statsDict["BLK"]
	pos = statsDict['POS']
	if pos == 'C':
		finalizedStats[5] = 1
	if pos == 'F':
		finalizedStats[7] = 1
	if pos == 'G':
		finalizedStats[10] = 1
	return

def getStatsOfChosenPlayer(playerName, stats):
	cursor = DATABASE.cursor()
	playerName = playerDict[playerName][0]
	playerName = "'" + playerName + "'"
	cursor.execute("SELECT PTS FROM ncaa WHERE Player=" + playerName)
	stats["PTS"] = cursor.fetchone()[0]

	cursor.execute("SELECT AST FROM ncaa WHERE Player=" + playerName)
	stats["AST"] = cursor.fetchone()[0]

	cursor.execute("SELECT TRB FROM ncaa WHERE Player=" + playerName)
	stats["RBD"] = cursor.fetchone()[0]

	cursor.execute("SELECT STL FROM ncaa WHERE Player=" + playerName)
	stats["STL"] = cursor.fetchone()[0]

	cursor.execute("SELECT BLK FROM ncaa WHERE Player=" + playerName)
	stats["BLK"] = cursor.fetchone()[0]
	return stats

def averageTaker(columnToAvgFrom):
	global DATABASE
	cursor = DATABASE.cursor()
	st = "SELECT avg(" + columnToAvgFrom + ") FROM ncaa"
	cursor.execute(st)
	fetched = cursor.fetchone()
	print("this is average:")
	print(fetched[0])
	return fetched[0]


def fillInEmptyStats(dictOfStats):
	for key, value in dictOfStats.items():
		if value == -1:
			print(key)
			if key == 'RBD':
				orb = averageTaker('ORB')
				drb = averageTaker('DRB')
				dictOfStats[key] = orb+drb
			else:
				dictOfStats[key] = averageTaker(key)
	return dictOfStats

@app.route('/hello', methods=['POST'])
def hello():
	#inPoints = request.form['points']
	#inRebounds = request.form['rebounds']
	#inAssists = request.form['assists']
	#inPlayerChoice = request.form['playerChoice']
	#inPlayerPost = request.form['position']
	predictPerformance(finalizedStats, False)
	return render_template('hello.html', points=12)


@app.route('/newSubmission', methods=['POST'])
def newSubmission():
	return redirect('/')

def unpickleRFModel():
	modelFile = open('./cs316_nba/model/randomforest.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global rfModel
	rfModel = model

	modelFile = open('./cs316_nba/model/randomforest_team.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global rfModelTeam
	rfModelTeam = model

	return

def unpickleNNModel():
	modelFile = open('./cs316_nba/model/nearestneighbor.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global nnModel
	nnModel = model

	modelFile = open('./cs316_nba/model/nearestneighbor_team.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global nnModelTeam
	nnModelTeam = model

	return

def predictPerformance(inputStats, teamInput):
	#[[points, rebounds, assists, steals, blocks, C, C&F, F, F&C, F&G, G, G&F]]
	print("reaches here")
	global unpickled
	if unpickled == False:
		print("should reach here")
		unpickleRFModel()
		unpickleNNModel()
		unpickled = True

	global nnModel
	global rfModel
	nnModelToUse = nnModel
	rfModelToUse = rfModel

	if teamInput:
		global nnModelTeam
		global rfModelTeam
		nnModelToUse = nnModelTeam
		rfModelToUse = rfModelTeam

	print(inputStats)

	#inputStats = [12,0,0,0,0,0,0,0,0,0,0,0]
	rfPrediction = (rfModelToUse.predict([inputStats]))
	print(rfPrediction)
	#print(ar.shape)
	#print (ar[0])
	#print (type(nnModelToUse.n_neighbors()))
	nnPrediction = (nnModelToUse.predict([inputStats]))
	print(nnPrediction)
	print (nnModelToUse.kneighbors([inputStats], 3))
	#print(nnModelToUse.n_neighbors([inputStats]))

if __name__ == '__main__':
	app.run()
