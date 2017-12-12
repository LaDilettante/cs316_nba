from flask import Flask, render_template, request, redirect, g
from wtforms import Form, IntegerField, SelectField,  validators, TextField
import pickle
import sqlite3
import numpy
import time

app = Flask(__name__)

unpickled = False

rfModelP = None
rfModelA = None
rfModelR = None
rfModelB = None
rfModelS = None

rfModelTeamP = None
rfModelTeamA = None
rfModelTeamR = None
rfModelTeamB = None
rfModelTeamS = None


nnModelP = None
nnModelA = None
nnModelR = None
nnModelB = None
nnModelS = None

nnModelTeamP = None
nnModelTeamA = None
nnModelTeamR = None
nnModelTeamB = None
nnModelTeamS = None


finalizedStats = [0,0,0,0,0,0,0,0,0,0,0,0]
teamStat = 'None'

DATABASEPATH = './cs316_nba/data/data.sqlite_2'

DATABASE = None

playerDict = {}

teamDict = {}

teamYear = '2017'

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
	global playersYear
	s = "'" + playersYear + "'"
	strng = "SELECT DISTINCT Player FROM ncaa WHERE Year=" + s + " ORDER BY Player"
	#cursor.execute("SELECT DISTINCT Player FROM ncaa WHERE Year='2014' ORDER BY Player")
	cursor.execute(strng)
	rows =(cursor.fetchall())
	players = []
	for p in rows:
		name = p[0]
		tup = (p[0], name)
		global playerDict
		playerDict[name] = p
		players.append(tup)
	players.insert(0, ('Select Player', 'Select Player'))
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
	team = SelectField(u'Existing NCAA Teams', [validators.Optional()], choices=existingTeams, default='Select Team')
	
	playerYears = [(str(i), str(i)) for i in range(2002,2018)]
	playerYears.insert(0, ('Select Year', 'Select Year'))
	playerYear = SelectField(u'Year', [validators.Optional()], choices=playerYears, default='Select Year')

	existingPlayers2 = getExistingCollegePlayers()
	#existingPlayers2.insert(0,('Select Player', 'Select Player'))
	playerChoice= SelectField(u'Existing College Players', default='Select Player')


class UpdateForm(Form):
	name = TextField('Name', [validators.InputRequired()])
	points= IntegerField('Points', [validators.InputRequired()], render_kw={"placeholder":"Points"})
	assists= IntegerField('Assists', [validators.InputRequired()], render_kw={"placeholder":"Assists"})
	rebounds= IntegerField('Rebounds', [validators.InputRequired()], render_kw={"placeholder":"Rebounds"})
	blocks = IntegerField('Blocks', [validators.InputRequired()], render_kw={"placeholder":"Blocks"})
	steals = IntegerField('Steals', [validators.InputRequired()], render_kw={"placeholder":"Steals"})


	existingTeams = getExistingTeams()
	existingTeams.insert(0, ('Select Team', 'Select Team'))
	team = SelectField(u'Existing NCAA Teams', [validators.InputRequired()], choices=existingTeams, default='Select Team')
	
	playerYears = [(str(i), str(i)) for i in range(2002,2018)]
	playerYears.insert(0, ('Select Year', 'Select Year'))
	playerYear = SelectField(u'Year', [validators.Optional()], choices=playerYears, default='Select Year')

@app.route('/update', methods=['POST', 'GET'])
def update():
	form = UpdateForm(request.form)
	if form.validate():
		vals = (request.form["name"],request.form["team"],0,0,request.form["points"],0,0,0,0,0,0,0,0,0,0,0,0,0,0,request.form["rebounds"],request.form["assists"],request.form["steals"],request.form["blocks"],0,0,form.playerYear.data,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
		cursor = DATABASE.cursor()
		cursor.execute("INSERT INTO ncaa (Player,Team,G,MP,PTS,FG,FGA,FGpercent,TwoP,TwoPA,TwoPpercent,ThreeP,ThreePA,ThreePpercent,FT,FTA,FTpercent,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,Year,PTSperGame,FGAperGame,PTSperPlay,TSpercent,eFGpercent,FTAperFPA,ThrePAperFGA,ASTperGame,ASTperFGA,ASTperTOV,PPR,BLKperGame,STLperGame,PFperGame) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", vals)
		cursor.fetchone()
		inPName = vals[0]
		cursor.execute("SELECT * FROM ncaa WHERE Player=?", (inPName,))
		DATABASE.commit()
		DATABASE.close()
		getDatabase()
		return redirect('/updated')
	return render_template('update.html', uForm = form)

shownYet = False

@app.route('/updated', methods=['POST', 'GET'])
def updated():
	time.sleep(2)
	return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def index():
	global teamYear
	statsDict = {}
	statsDict['PTS'] = -1
	statsDict['AST'] = -1
	statsDict['RBD'] = -1
	statsDict['STL'] = -1
	statsDict['BLK'] = -1
	statsDict['POS'] = "C"
	statsDict['TEAM'] = "None"
	teamStat = None
	form=BasketballForm(request.form)
	#form = model_form(BasketballForm(request.form), base_class=Form)
	form.playerChoice.choices = getExistingCollegePlayers()

	if form.validate() and (form.position.data != 'None' or form.playerChoice.data != 'Select Player'):
		#change global var userInput
		#need steals and blocks

		if request.form["points"]:
			statsDict["PTS"] = float(request.form["points"])
		if request.form["assists"]:
			statsDict["AST"] = float(request.form["assists"])
		if request.form["rebounds"]:
			statsDict["RBD"] = float(request.form["rebounds"])
		if form.position != 'None':
			statsDict['POS'] = form.position.data
		if form.team.data != "Select Team":
			statsDict["TEAM"] = form.team.data

		if form.playerYear.data!='Select Year':
			
			teamYear = form.playerYear.data



		
		filledStats = fillInEmptyStats(statsDict)
		if form.playerChoice.data != 'Select Player':
			filledStats = getStatsOfChosenPlayer(form.playerChoice.data, filledStats)
		
		transposeDictToArray(filledStats)

		return redirect('/hello')


	if (form.playerYear.data!='Select Year'):

		global playersYear
		
		teamYear = form.playerYear.data
		playersYear = form.playerYear.data
		newPlayers = getExistingCollegePlayers()
		form.playerChoice.choices = newPlayers

	form = BasketballForm(request.form)
	form.playerChoice.choices = getExistingCollegePlayers()
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
	global teamStat
	teamStat = statsDict["TEAM"]
	return

def getStatsOfChosenPlayer(playerName, stats):
	cursor = DATABASE.cursor()
	playerName = playerDict[playerName][0]
	playerName = (playerName,)

	cursor.execute("SELECT PTS FROM ncaa WHERE Player=?", playerName)
	stats["PTS"] = cursor.fetchone()[0]

	cursor.execute("SELECT AST FROM ncaa WHERE Player=?", playerName)
	stats["AST"] = cursor.fetchone()[0]

	cursor.execute("SELECT TRB FROM ncaa WHERE Player=?", playerName)
	stats["RBD"] = cursor.fetchone()[0]

	cursor.execute("SELECT STL FROM ncaa WHERE Player=?", playerName)
	stats["STL"] = cursor.fetchone()[0]

	cursor.execute("SELECT BLK FROM ncaa WHERE Player=?", playerName)
	stats["BLK"] = cursor.fetchone()[0]

	cursor.execute("SELECT Team FROM ncaa WHERE Player=?", playerName)
	stats["TEAM"] = cursor.fetchone()[0]

	return stats

def averageTaker(columnToAvgFrom):
	global DATABASE
	cursor = DATABASE.cursor()
	st = "SELECT avg(" + columnToAvgFrom + ") FROM ncaa"
	cursor.execute(st)
	fetched = cursor.fetchone()

	return fetched[0]


def fillInEmptyStats(dictOfStats):
	for key, value in dictOfStats.items():
		if value == -1:

			if key == 'RBD':
				orb = averageTaker('TRB')
				
				dictOfStats[key] = orb
			else:
				dictOfStats[key] = averageTaker(key)
	return dictOfStats

@app.route('/hello', methods=['POST', 'GET'])
def hello():
	t = predictPerformance(finalizedStats)

	return render_template('hello.html', pointsPredict=t[0][0], assistsPredict=t[0][1], reboundsPredict=t[0][2], blocksPredict=t[0][3], stealsPredict=t[0][4],one=t[2][0], two=t[2][1], three=t[2][2])


@app.route('/newSubmission', methods=['POST'])
def newSubmission():
	return redirect('/')

def unpickleRFModel():
	modelFile = open('./cs316_nba/model/randomforest_point.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global rfModelP
	rfModelP = model

	modelFile = open('./cs316_nba/model/randomforest_assist.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global rfModelA
	rfModelA = model

	modelFile = open('./cs316_nba/model/randomforest_rebound.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global rfModelR
	rfModelR = model

	modelFile = open('./cs316_nba/model/randomforest_block.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global rfModelB
	rfModelB = model

	modelFile = open('./cs316_nba/model/randomforest_steal.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global rfModelS
	rfModelS = model




	modelFile = open('./cs316_nba/model/randomforest_team_point.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global rfModelTeamP
	rfModelTeamP = model

	modelFile = open('./cs316_nba/model/randomforest_team_assist.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global rfModelTeamA
	rfModelTeamA = model

	modelFile = open('./cs316_nba/model/randomforest_team_rebound.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global rfModelTeamR
	rfModelTeamR = model

	modelFile = open('./cs316_nba/model/randomforest_team_block.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global rfModelTeamB
	rfModelTeamB = model

	modelFile = open('./cs316_nba/model/randomforest_team_steal.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global rfModelTeamS
	rfModelTeamS = model

	return

def unpickleNNModel():
	modelFile = open('./cs316_nba/model/nearestneighbor_point.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global nnModelP
	nnModelP = model

	modelFile = open('./cs316_nba/model/nearestneighbor_assist.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global nnModelA ##TODO
	nnModelA = model

	modelFile = open('./cs316_nba/model/nearestneighbor_rebound.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global nnModelR ##TODO
	nnModelR = model

	modelFile = open('./cs316_nba/model/nearestneighbor_block.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global nnModelB ##TODO
	nnModelB = model

	modelFile = open('./cs316_nba/model/nearestneighbor_steal.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global nnModelS ##TODO
	nnModelS = model




	modelFile = open('./cs316_nba/model/nearestneighbor_team_point.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global nnModelTeamP
	nnModelTeamP = model

	modelFile = open('./cs316_nba/model/nearestneighbor_team_assist.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global nnModelTeamA
	nnModelTeamA = model

	modelFile = open('./cs316_nba/model/nearestneighbor_team_rebound.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global nnModelTeamR
	nnModelTeamR = model

	modelFile = open('./cs316_nba/model/nearestneighbor_team_block.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global nnModelTeamB
	nnModelTeamB = model

	modelFile = open('./cs316_nba/model/nearestneighbor_team_steal.pkl', 'rb')
	model = pickle.load(modelFile)
	modelFile.close()
	global nnModelTeamS
	nnModelTeamS = model

	return

def predictPerformance(inputStats2):
	#[[points, rebounds, assists, steals, blocks, C, C&F, F, F&C, F&G, G, G&F]]
	inputStats = [x for x in inputStats2]
	global unpickled
	if unpickled == False:

		unpickleRFModel()
		unpickleNNModel()
		unpickled = True

	global teamStat
	global teamYear
	global playersYear
	
	if teamStat!='None':
		theTeamStats = getTeamStats(teamStat)

		if theTeamStats is None:
			teamStat = 'None'
			return predictPerformance(inputStats2)
		for x in theTeamStats:
			inputStats.insert(5, x)
		rfTeamPrediction = rfTeamPredict(inputStats)
		nnTeamPrediction = nnTeamPredict(inputStats)

		nearestNeighborsTeam = getTeamNeighborStats(inputStats)

		
		teamYear = '2017'
		teamStat = 'None'
		playersYear = '2014'
		return (rfTeamPrediction, nnTeamPrediction, nearestNeighborsTeam)

	
	else:
		teamYear = '2017'
		teamStat = 'None'
		playersYear = '2014'


		rfPrediction = rfPredict(inputStats)
		nnPrediction = nnPredict(inputStats)

		nearestNeighbors = getNeighborStats(inputStats)

		return (rfPrediction, nnPrediction, nearestNeighbors)


def getTeamNeighborStats(stats):
	c = DATABASE.cursor()
	lis = nnModelTeamP.kneighbors([stats], 3)
	arr = []
	statement = "SELECT * FROM rookiedata WHERE Player LIKE ?"
	pandaFile = open('./cs316_nba/model/training_data_team.pkl', 'rb')
	panda = pickle.load(pandaFile)
	for i in lis[1][0]:

		name = panda.index[i][0]
		name = name + "%"
		name = (name,)
		statement2 = statement
		c.execute(statement2, name)
		pStats = c.fetchone()
		pArr = []
		pName = pStats[1].split("\\")[0]
		pArr.append(pName)
		pArr.append(pStats[25]) #ppg
		pArr.append(pStats[20]) #apg
		pArr.append(pStats[19]) #rpg
		pArr.append(pStats[22]) #bpg
		pArr.append(pStats[21]) #spg
		arr.append(pArr)
	return arr

def getNeighborStats(stats):
	c = DATABASE.cursor()
	lis = nnModelP.kneighbors([stats], 3)
	arr = []
	statement = "SELECT * FROM rookiedata WHERE Player LIKE ?"
	pandaFile = open('./cs316_nba/model/training_data.pkl', 'rb')
	panda = pickle.load(pandaFile)
	for i in lis[1][0]:

		name = panda.index[i]
		name = name + "%"
		name = name
		name = (name,)
		statement2 = statement
		c.execute(statement2, name)
		pStats = c.fetchone()
		pArr = []
		pName = pStats[1].split("\\")[0]
		pArr.append(pName)
		pArr.append(pStats[25]) #ppg
		pArr.append(pStats[20]) #apg
		pArr.append(pStats[19]) #rpg
		pArr.append(pStats[22]) #bpg
		pArr.append(pStats[21]) #spg
		arr.append(pArr)
	return arr







def rfTeamPredict(stats):
	ret = [0,0,0,0,0]
	ret[0] = rfModelTeamP.predict([stats])[0]
	ret[1] = rfModelTeamA.predict([stats])[0]
	ret[2] = rfModelTeamR.predict([stats])[0]
	ret[3] = rfModelTeamB.predict([stats])[0]
	ret[4] = rfModelTeamS.predict([stats])[0]
	return ret

def rfPredict(stats):
	ret = [0,0,0,0,0]
	ret[0] = rfModelP.predict([stats])[0]
	ret[1] = rfModelA.predict([stats])[0]
	ret[2] = rfModelR.predict([stats])[0]
	ret[3] = rfModelB.predict([stats])[0]
	ret[4] = rfModelS.predict([stats])[0]
	return ret

def nnTeamPredict(stats):
	ret = [0,0,0,0,0]
	ret[0] = nnModelTeamP.predict([stats])[0]
	ret[1] = nnModelTeamA.predict([stats])[0]
	ret[2] = nnModelTeamR.predict([stats])[0]
	ret[3] = nnModelTeamB.predict([stats])[0]
	ret[4] = nnModelTeamS.predict([stats])[0]
	return ret

def nnPredict(stats):
	ret = [0,0,0,0,0]
	ret[0] = nnModelP.predict([stats])[0]
	ret[1] = nnModelA.predict([stats])[0]
	ret[2] = nnModelR.predict([stats])[0]
	ret[3] = nnModelB.predict([stats])[0]
	ret[4] = nnModelS.predict([stats])[0]
	return ret

def getTeamStats(teamName):
	teamKey = teamName

	teamYearInt = int(teamYear)
	if teamYearInt == 2017:
		teamYearInt = 2018
	prevYear = teamYearInt-1
	dastring = str(prevYear) + "-" + str(teamYearInt)[2:]
	dastring = "'" + dastring + "'"

	teamString = "'" + teamKey + "'"
	altTeamString = "'" + teamKey + " NCAA" + "'"
	c = DATABASE.cursor()
	ultstring = "SELECT * FROM teamdata WHERE School=" + teamString + " AND Season=" + dastring
	altString = "SELECT * FROM teamdata WHERE School=" + altTeamString + " AND Season=" + dastring
	finalOne = "'" + teamKey.split(" ")[0] + "'"
	finalString = "SELECT * FROM teamdata WHERE School=" + finalOne + " AND Season=" + dastring
	c.execute(ultstring)
	resultsOne = c.fetchone()

	if resultsOne is None:
		c.execute(altString)

		resultsOne = c.fetchone()

	if resultsOne is None:
		c.execute(finalString)
		resultsOne = c.fetchone()

	if resultsOne is None:	
		return None

	locTeamStats = []
	locTeamStats.insert(0,resultsOne[6])
	locTeamStats.insert(0,resultsOne[15])
	locTeamStats.insert(0,resultsOne[16])
	locTeamStats.insert(0,resultsOne[28])
	locTeamStats.insert(0,resultsOne[29])
	locTeamStats.insert(0,resultsOne[30])
	locTeamStats.insert(0,resultsOne[31])
	return locTeamStats


if __name__ == '__main__':
	app.run()
