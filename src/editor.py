# does all the post generating and editing

import player

import xml.etree.ElementTree as ET
import urllib2
import simplejson as json
from datetime import datetime, timedelta
import time

def generatetitle(dir):
	title = "GAME THREAD: "
	while True:
		try:
			response = urllib2.urlopen(dir + "linescore.json")
			oresponse = urllib2.urlopen(dir + "boxscore.json")
			break
		except :
			print "Couldn't find file, trying again..."
			time.sleep(20)
	filething = json.load(response)
	ofilething = json.load(oresponse)
	game = filething.get('data').get('game')
	ogame = ofilething.get('data').get('boxscore')
	timestring = game.get('time_date') + " " + game.get('ampm')
	date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
	title = title + ogame.get('away_fname') + " (" + game.get('away_win') + "-" + game.get('away_loss') + ")"
	title = title + " @ "
	title = title + ogame.get('home_fname') + " (" + game.get('home_win') + "-" + game.get('home_loss') + ")"
	title = title + " - "
	title = title + date_object.strftime("%B %d, %Y")
	return title

def generatecode(dir):
	code = ""
	# files needed to download
	files = dict()
	dirs = []
	dirs.append(dir + "linescore.json")
	dirs.append(dir + "boxscore.json")
	dirs.append(dir + "gamecenter.xml")
	dirs.append(dir + "plays.json")
	dirs.append(dir + "/inning/inning_Scores.xml")
	files = downloadfiles(dirs)
	
	#generate post
	code = code + generateheader(files)
	code = code + generatelinescore(files)
	code = code + generateboxscore(files)
	code = code + generatescoringplays(files)
	if files["linescore"].get('data').get('game').get('status') == "Final":
		s = files["linescore"].get('data').get('game')
		code = code + "###FINAL "
		if int(s.get("home_team_runs")) < int(s.get("away_team_runs")):
			code = code + s.get("away_team_runs") + "-" + s.get("home_team_runs") + " " + s.get("away_team_name")
		elif int(s.get("home_team_runs")) > int(s.get("away_team_runs")):
			code = code + s.get("home_team_runs") + "-" + s.get("away_team_runs") + " " + s.get("home_team_name")
		else:
			code = code + "SOMETHING WENT HORRIBLY WRONG"
	if files["linescore"].get('data').get('game').get('status') == "Postponed":
		code = code + "###POSTPONED"
	return code

def downloadfiles(dirs):
	files = dict()
	while True:
		try:
			response = urllib2.urlopen(dirs[0])
			files["linescore"] = json.load(response)
			response = urllib2.urlopen(dirs[1])
			files["boxscore"] = json.load(response)
			response = urllib2.urlopen(dirs[2])
			files["gamecenter"] = ET.parse(response)
			response = urllib2.urlopen(dirs[3])
			files["plays"] = json.load(response)
			response = urllib2.urlopen(dirs[4])
			files["scores"] = ET.parse(response)
			break
		except:
			print "Couldn't open file, retrying..."
			time.sleep(10)
	return files

	
def generateheader(files):
	header = ""
	game = files["linescore"].get('data').get('game')
	ogame = files["boxscore"].get('data').get('boxscore')
	timestring = game.get('time_date') + " " + game.get('ampm')
	date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
	t = timedelta(hours=1) #change depending on team, 0 for east, 1 for central, 2 for mountain, 3 for west coast
	timezone = "CST" #change this based on team too
	date_object = date_object - t
	weather = files["plays"].get('data').get('game').get('weather')
	subreddits = getsubreddits(game.get('home_team_name'),game.get('away_team_name'))
	header = header + "###" + ogame.get('away_fname')
	header = header + " @ " + ogame.get('home_fname') + "\n"
	header = header + "First Pitch|Media||Feed|Channel|Subreddits\n"
	header = header + ":--|:--|:--:|:--|:--|:--\n"
	root = files["gamecenter"].getroot()
	broadcast = root.find('broadcast')
	header = header + date_object.strftime("%I:%M %p") + " " + timezone + "|**Audio**||" + game.get('home_name_abbrev') + "|" 
	if not isinstance(broadcast[0][0].text, type(None)):
		header = header + broadcast[0][0].text
	header = header + "|" + subreddits[0] + "\n"
	header = header + "**Weather**| ||" + game.get('away_name_abbrev') + "|"
	if not isinstance(broadcast[1][0].text, type(None)):
		header = header + broadcast[1][0].text
	header = header + "|" + subreddits[1] + "\n"
	header = header + weather.get('condition') + " " + weather.get('temp') + " F|**Video**||" + game.get('home_name_abbrev') + "|" 
	if not isinstance(broadcast[0][1].text, type(None)):
		header = header + broadcast[0][1].text 
	header = header + "| **Location**\n"
	header = header + weather.get('wind') + " |||" + game.get('away_name_abbrev') + "|" 
	if not isinstance(broadcast[1][1].text, type(None)):
		header = header + broadcast[1][1].text 
	header = header + "|" + game.get('venue') + "\n"
	header = header + "\n---\n"
	return header
	
def generatelinescore(files):
	linescore = "###Line Score\n"
	game = files["linescore"].get('data').get('game')
	lineinfo = game.get('linescore')
	innings = len(lineinfo) if len(lineinfo) > 9 else 9
	curinning = len(lineinfo)
	linescore = linescore + " |"
	for i in range(1, innings+1):
		linescore = linescore + "**" + str(i) + "**|"
	linescore = linescore + "**R**|**H**|**E**\n"
	for i in range(0, innings+4):
		linescore = linescore + ":--:|"
	linescore = linescore + "\n" + game.get('away_name_abbrev') + "|"
	x = 1
	if type(lineinfo) is list:
		for v in lineinfo:
			linescore = linescore + v.get('away_inning_runs') + "|"
			x = x + 1
	elif type(lineinfo) is dict:
		linescore = linescore + lineinfo.get('away_inning_runs') + "|"
		x = x + 1
	for i in range(x, innings+1):
		linescore = linescore + "|"
	linescore = linescore + game.get('away_team_runs') + "|" + game.get('away_team_hits') + "|" + game.get('away_team_errors')
	linescore = linescore + "\n" + game.get('home_name_abbrev') + "|"
	x = 1
	if type(lineinfo) is list:
		for v in lineinfo:
			linescore = linescore + v.get('home_inning_runs') + "|"
			x = x + 1
	elif type(lineinfo) is dict:
		linescore = linescore + lineinfo.get('home_inning_runs') + "|"
		x = x + 1
	for j in range(x, innings+1):
		linescore = linescore + "|"
	linescore = linescore + game.get('home_team_runs') + "|" + game.get('home_team_hits') + "|" + game.get('home_team_errors')
	return linescore
	
def generateboxscore(files):
	boxscore = "\n###Live Box Score\n"
	homebatters = []; awaybatters = []
	homepitchers = []; awaypitchers = []
	game = files["boxscore"].get('data').get('boxscore')
	batting = game.get('batting')
	for i in range(0,len(batting)):
		players = batting[i].get('batter')
		for b in range(0,len(players)):
			if players[b].get('bo') != None:
				if batting[i].get('team_flag') == "home":
					homebatters.append(player.batter(players[b].get('name'), players[b].get('pos'), players[b].get('ab'), players[b].get('r'), players[b].get('h'), players[b].get('rbi'), players[b].get('bb'), players[b].get('so'), players[b].get('avg'), players[b].get('id')))
				else:	
					awaybatters.append(player.batter(players[b].get('name'), players[b].get('pos'), players[b].get('ab'), players[b].get('r'), players[b].get('h'), players[b].get('rbi'), players[b].get('bb'), players[b].get('so'), players[b].get('avg'), players[b].get('id')))
	pitching = game.get('pitching')
	for i in range(0,len(pitching)):
		players = pitching[i].get('pitcher')
		if type(players) is list:
			for p in range(0,len(players)):
				if pitching[i].get('team_flag') == "home":
					homepitchers.append(player.pitcher(players[p].get('name'), players[p].get('pos'), players[p].get('out'), players[p].get('h'), players[p].get('r'), players[p].get('er'), players[p].get('bb'), players[p].get('so'), players[p].get('np'), players[p].get('s'), players[p].get('era'), players[p].get('id')))
				else:
					awaypitchers.append(player.pitcher(players[p].get('name'), players[p].get('pos'), players[p].get('out'), players[p].get('h'), players[p].get('r'), players[p].get('er'), players[p].get('bb'), players[p].get('so'), players[p].get('np'), players[p].get('s'), players[p].get('era'), players[p].get('id')))
		elif type(players) is dict:
			if pitching[i].get('team_flag') == "home":
				homepitchers.append(player.pitcher(players.get('name'), players.get('pos'), players.get('out'), players.get('h'), players.get('r'), players.get('er'), players.get('bb'), players.get('so'), players.get('np'), players.get('s'), players.get('era'), players.get('id')))
			else:
				awaypitchers.append(player.pitcher(players.get('name'), players.get('pos'), players.get('out'), players.get('h'), players.get('r'), players.get('er'), players.get('bb'), players.get('so'), players.get('np'), players.get('s'), players.get('era'), players.get('id')))
	while len(homebatters) < len(awaybatters):
		homebatters.append(player.batter())
	while len(awaybatters) < len(homebatters):
		awaybatters.append(player.batter())
	while len(homepitchers) < len(awaypitchers):
		homepitchers.append(player.pitcher())
	while len(awaypitchers) < len(homepitchers):
		awaypitchers.append(player.pitcher())
		
		
		
	boxscore = boxscore + "**" + files["linescore"].get('data').get('game').get('away_name_abbrev') +"**|Pos|AB|R|H|RBI|BB|SO|BA|"
	boxscore = boxscore + "|"
	boxscore = boxscore + "**" + files["linescore"].get('data').get('game').get('home_name_abbrev') +"**|Pos|AB|R|H|RBI|BB|SO|BA|"
	boxscore = boxscore + "\n"
	boxscore = boxscore + ":--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
	boxscore = boxscore + ":--:|"
	boxscore = boxscore + ":--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
	boxscore = boxscore + "\n"
	for i in range(0,len(homebatters)):
		boxscore = boxscore + str(awaybatters[i]) + "|" + str(homebatters[i]) + "\n"
	boxscore = boxscore + "\n**" + files["linescore"].get('data').get('game').get('away_name_abbrev') +"**|Pos|IP|H|R|ER|BB|SO|P-S|ERA|"
	boxscore = boxscore + "|"
	boxscore = boxscore + "**" + files["linescore"].get('data').get('game').get('home_name_abbrev') +"**|Pos|IP|H|R|ER|BB|SO|P-S|ERA|"
	boxscore = boxscore + "\n"
	boxscore = boxscore + ":--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
	boxscore = boxscore + ":--:|"
	boxscore = boxscore + ":--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"
	boxscore = boxscore + "\n"
	for i in range(0,len(homepitchers)):
		boxscore = boxscore + str(awaypitchers[i]) + "|" + str(homepitchers[i]) + "\n"
	boxscore = boxscore + "---\n\n"
	return boxscore
	
def generatescoringplays(files):
	scoringplays = "###Scoring Plays\nInning|Play|Score\n"
	scoringplays = scoringplays + ":--:|:--|:--:\n"
	root = files["scores"].getroot()
	game = files["linescore"].get('data').get('game')
	scores = root.findall("score")
	currinning = ""
	inningcheck = ""
	for s in scores:
		if s.get("top_inning") == "Y":
			inningcheck = "Top "
		else:
			inningcheck = "Bottom "
		inningcheck = inningcheck + s.get("inn") + "|"
		if inningcheck != currinning:
			currinning = inningcheck
			scoringplays = scoringplays + currinning
		else:
			scoringplays = scoringplays + " |"
		if "scores" not in s.find('atbat').get('des') and s.get("pbp") == "":
			actions = s.findall("action")
			scoringplays = scoringplays + actions[len(actions)-1].get("des")
		elif s.get("pbp") == "" :
			scoringplays = scoringplays + s.find('atbat').get('des')
		elif "scores" not in s.get("pbp") and len(s.findall("action")) > 0:
			actions = s.findall("action")
			scoringplays = scoringplays + actions[len(actions)-1].get("des")
		else:
			scoringplays = scoringplays + s.get("pbp")
		scoringplays = scoringplays + "|"
		if int(s.get("home")) < int(s.get("away")):
			scoringplays = scoringplays + s.get("away") + "-" + s.get("home") + " " + game.get("away_team_name")
		elif int(s.get("home")) > int(s.get("away")):
			scoringplays = scoringplays + s.get("home") + "-" + s.get("away") + " " + game.get("home_team_name")
		else:
			scoringplays = scoringplays + s.get("home") + "-" + s.get("away") + " Tied"
		scoringplays = scoringplays + "\n"
	scoringplays = scoringplays + "\n"
	return scoringplays

def getsubreddits(homename, awayname):
	subreddits = []
	options = {
		"Twins" : "/r/minnesotatwins",
		"White Sox" : "/r/WhiteSox",
		"Tigers" : "/r/MotorCityKitties",
		"Royals" : "/r/KCRoyals",
		"Indians" : "/r/WahoosTipi",
		"Rangers" : "/r/TexasRangers",
		"Astros" : "/r/Astros",
		"Athletics" : "/r/OaklandAthletics",
		"Angels" : "/r/AngelsBaseball",
		"Mariners" : "/r/Mariners",
		"Red Sox" : "/r/RedSox",
		"Yankees" : "/r/Yankees",
		"Blue Jays" : "/r/TorontoBlueJays",
		"Rays" : "/r/TampaBayRays",
		"Orioles" : "/r/Orioles",
		"Cardinals" : "/r/Cardinals",
		"Reds" : "/r/Reds",
		"Pirates" : "/r/Buccos",
		"Cubs" : "/r/Cubs",
		"Brewers" : "/r/Brewers",
		"Giants" : "/r/SFGiants",
		"D-backs" : "/r/azdiamondbacks",
		"Rockies" : "/r/ColoradoRockies",
		"Dodgers" : "/r/Dodgers",
		"Padres" : "/r/Padres",
		"Phillies" : "/r/Phillies",
		"Mets" : "/r/NewYorkMets",
		"Marlins" : "/r/letsgofish",
		"Nationals" : "/r/Nationals",
		"Braves" : "/r/Braves",
		"National" : "/r/baseball",
		"American" : "/r/baseball"
	}
	subreddits.append(options[homename])
	subreddits.append(options[awayname])
	return subreddits
