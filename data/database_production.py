import sqlite3
import os
import csv

if os.path.exists('/Users/vidurmalhotra/Desktop/COMPSCI316/Project/db/data.sqlite'):
    os.remove('/Users/vidurmalhotra/Desktop/COMPSCI316/Project/db/data.sqlite')
conn = sqlite3.connect('/Users/vidurmalhotra/Desktop/COMPSCI316/Project/db/data.sqlite')
c = conn.cursor()

#rookiedata
c.execute("CREATE TABLE rookiedata (Rk,Player,Age,Tm,Lg,Season,G,GS,MP,FG,FGA,TwoP,TwoPA,ThreeP,ThreePA,FT,FTA,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,FGpercent,TwoPpercent,ThreePpercent,eFGpercent,FTpercent,TSpercent)")

with open('/Users/vidurmalhotra/Desktop/COMPSCI316/Project/db/nbarookiedata.csv','rt') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['Rk'], i['Player'], i['Age'], i['Tm'], i['Lg'], i['Season'], i['G'], i['GS'], i['MP'], i['FG'], i['FGA'], i['2P'], i['2PA'], i['3P'], i['3PA'], i['FT'], i['FTA'], i['ORB'], i['DRB'], i['TRB'], i['AST'], i['STL'], i['BLK'], i['TOV'], i['PF'], i['PTS'], i['FG%'], i['2P%'], i['3P%'], i['eFG%'], i['FT%'], i['TS%']) for i in dr]

c.executemany("INSERT INTO rookiedata (Rk,Player,Age,Tm,Lg,Season,G,GS,MP,FG,FGA,TwoP,TwoPA,ThreeP,ThreePA,FT,FTA,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,FGpercent,TwoPpercent,ThreePpercent,eFGpercent,FTpercent,TSpercent) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", to_db)

#draft
c.execute("CREATE TABLE draft (Rk,Year,Lg,Rd,Pk,Tm,Player,Age,Pos,Born,College)")

with open('/Users/vidurmalhotra/Desktop/COMPSCI316/Project/db/draft.csv','rt') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['Rk'], i['Year'], i['Lg'], i['Rd'], i['Pk'], i['Tm'], i['Player'], i['Age'], i['Pos'], i['Born'], i['College']) for i in dr]

c.executemany("INSERT INTO draft (Rk,Year,Lg,Rd,Pk,Tm,Player,Age,Pos,Born,College) VALUES (?,?,?,?,?,?,?,?,?,?,?);", to_db)

#ncaa
c.execute("CREATE TABLE ncaa (Player,Team,G,MP,PTS,FG,FGA,FGpercent,TwoP,TwoPA,TwoPpercent,ThreeP,ThreePA,ThreePpercent,FT,FTA,FTpercent,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,Year,PTSperGame,FGAperGame,PTSperPlay,TSpercent,eFGpercent,FTAperFPA,ThrePAperFGA,ASTperGame,ASTperFGA,ASTperTOV,PPR,BLKperGame,STLperGame,PFperGame)")

with open('/Users/vidurmalhotra/Desktop/COMPSCI316/Project/db/ncaa2.csv','rt') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['Name'], i['Team'], i['GP'], i['Min'], i['Pts'], i['FG'], i['FGA'], i['FG%'], i['2Pt'], i['2PtA'], i['2P%'], i['3Pt'], i['3PtA'], i['3P%'], i['FTM'], i['FTA'], i['FT%'], i['Off'], i['Def'], i['TOT'], i['Asts'], i['Stls'], i['Blks'], i['TOs'], i['PFs'], i['year'], i['PTs/g'], i['FGA/g'], i['Pts/Play'], i['TS%'], i['eFG%'], i['FTA/FGA'], i['3PA/FGA'], i['Ast/g'], i['Ast/FGA'], i['A/TO'], i['PPR'], i['BK/g'], i['STL/g'], i['PF/g']) for i in dr]

c.executemany("INSERT INTO ncaa (Player,Team,G,MP,PTS,FG,FGA,FGpercent,TwoP,TwoPA,TwoPpercent,ThreeP,ThreePA,ThreePpercent,FT,FTA,FTpercent,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,Year,PTSperGame,FGAperGame,PTSperPlay,TSpercent,eFGpercent,FTAperFPA,ThrePAperFGA,ASTperGame,ASTperFGA,ASTperTOV,PPR,BLKperGame,STLperGame,PFperGame) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",to_db)

#teamdata
c.execute("CREATE TABLE teamdata (Rk,School,Season,G,W,L,WLpercent,SRS,SOS,ConfW,ConfL,HomeW,HomeL,AwayW,AwayL,TmPoints,OppPoints,MP,FG,FGA,FGpercent,ThreeP,ThreePA,ThreePpercent,FT,FTA,FTpercent,ORB,TRB,AST,STL,BLK,TOV,PF)")

with open('/Users/vidurmalhotra/Desktop/COMPSCI316/Project/db/team_data.csv','rt') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['Rk'], i['School'], i['Season'], i['G'], i['W'], i['L'], i['W-L%'], i['SRS'], i['SOS'], i['ConfW'], i['ConfL'], i['HomeW'], i['HomeL'], i['AwayW'], i['AwayL'], i['Tm.'], i['Opp.'], i['MP'], i['FG'], i['FGA'], i['FG%'], i['3P'], i['3PA'], i['3P%'], i['FT'], i['FTA'], i['FT%'], i['ORB'], i['TRB'], i['AST'], i['STL'], i['BLK'], i['TOV'], i['PF']) for i in dr]

c.executemany("INSERT INTO teamdata (Rk,School,Season,G,W,L,WLpercent,SRS,SOS,ConfW,ConfL,HomeW,HomeL,AwayW,AwayL,TmPoints,OppPoints,MP,FG,FGA,FGpercent,ThreeP,ThreePA,ThreePpercent,FT,FTA,FTpercent,ORB,TRB,AST,STL,BLK,TOV,PF) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", to_db)

conn.commit()
conn.close()
