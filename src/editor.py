# does all the post generating and editing

import player

import xml.etree.ElementTree as ET
import urllib2
import simplejson as json
from datetime import datetime, timedelta
import time

class Editor:

    def __init__(self,time_info,post_settings):
        (self.time_zone,self.time_change,) = time_info
        (self.header, self.box_score,
         self.line_score, self.scoring_plays,
         self.highlights, self.footer) = post_settings

    def generatetitle(self,dir):
        title = "GAME THREAD: "
        while True:
            try:
                response = urllib2.urlopen(dir + "linescore.json")
                break
            except:
                print "Couldn't find linescore.json for title, trying again..."
                time.sleep(20)
        filething = json.load(response)
        game = filething.get('data').get('game')
        timestring = game.get('time_date') + " " + game.get('ampm')
        date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
        title = title + game.get('away_team_name') + " (" + game.get('away_win') + "-" + game.get('away_loss') + ")"
        title = title + " @ "
        title = title + game.get('home_team_name') + " (" + game.get('home_win') + "-" + game.get('home_loss') + ")"
        title = title + " - "
        title = title + date_object.strftime("%B %d, %Y")
        print "Returning title..."
        return title


    def generateposttitle(self,dir):
        title = "POST GAME THREAD: "
        while True:
            try:
                response = urllib2.urlopen(dir + "linescore.json")
                break
            except:
                print "Couldn't find linescore.json for title, trying again..."
                time.sleep(20)
        filething = json.load(response)
        game = filething.get('data').get('game')
        timestring = game.get('time_date') + " " + game.get('ampm')
        date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
        title = title + game.get('away_team_name') + " (" + game.get('away_win') + "-" + game.get('away_loss') + ")"
        title = title + " @ "
        title = title + game.get('home_team_name') + " (" + game.get('home_win') + "-" + game.get('home_loss') + ")"
        title = title + " - "
        title = title + date_object.strftime("%B %d, %Y")
        print "Returning title..."
        return title


    def generatecode(self,dir):
        code = ""
        dirs = []
        dirs.append(dir + "linescore.json")
        dirs.append(dir + "boxscore.json")
        dirs.append(dir + "gamecenter.xml")
        dirs.append(dir + "plays.json")
        dirs.append(dir + "/inning/inning_Scores.xml")
        dirs.append(dir + "/media/highlights.xml")
        files = self.downloadfiles(dirs)
        if self.header: code = code + self.generateheader(files)
        if self.box_score: code = code + self.generateboxscore(files)
        if self.line_score: code = code + self.generatelinescore(files)
        if self.scoring_plays: code = code + self.generatescoringplays(files)
        if self.highlights: code = code + self.generatehighlights(files)
        if self.footer: code = code + self.generatefooter()
        code = code + self.generatestatus(files)
        print "Returning all code..."
        return code


    def downloadfiles(self,dirs):
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
                response = urllib2.urlopen(dirs[5])
                files["highlights"] = ET.parse(response)
                break
            except:
                break
        return files


    def generateheader(self,files):
        game = files["linescore"].get('data').get('game')
        timestring = game.get('time_date') + " " + game.get('ampm')
        date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
        t = timedelta(hours=self.time_change)
        timezone = self.time_zone
        date_object = date_object - t
        header = "**First Pitch:** " + date_object.strftime("%I:%M %p ") + timezone + "\n\n"
        header = header + "[Preview](http://mlb.mlb.com/mlb/gameday/index.jsp?gid=" + game.get('gameday_link') + ")\n"
        while True:
            try:
                weather = files["plays"].get('data').get('game').get('weather')
                root = files["gamecenter"].getroot()
                broadcast = root.find('broadcast')
                notes = self.getnotes(game.get('home_team_name'), game.get('away_team_name'))
                header = "|Game Info|Links|\n"
                header = header + "|:--|:--|\n"
                header = header + "|**First Pitch:** " + date_object.strftime("%I:%M %p ") + timezone + "@ " + game.get(
                    'venue') + "|[Gameday](http://mlb.mlb.com/mlb/gameday/index.jsp?gid=" + game.get(
                    'gameday_link') + ")|\n"
                header = header + "|**Weather:** " + weather.get('condition') + ", " + weather.get(
                    'temp') + " F, " + "Wind " + weather.get('wind')
                if "Y" in game.get('double_header_sw') or "S" in game.get('double_header_sw'):
                    header = header + "|[Game Graph](http://www.fangraphs.com/livewins.aspx?date=" + date_object.strftime(
                        "%Y-%m-%d") + "&team=" + game.get('home_team_name') + "&dh=" + game.get(
                        'game_nbr') + "&season=" + date_object.strftime("%Y") + ")|\n"
                else:
                    header = header + "|[Game Graph](http://www.fangraphs.com/livewins.aspx?date=" + date_object.strftime(
                        "%Y-%m-%d") + "&team=" + game.get('home_team_name') + "&dh=0&season=" + date_object.strftime(
                        "%Y") + ")|\n"
                header = header + "|**TV:** "
                if not isinstance(broadcast[0][0].text, type(None)):
                    header = header + broadcast[0][0].text
                if not isinstance(broadcast[1][0].text, type(None)):
                    header = header + ", " + broadcast[1][0].text
                header = header + "|[Strikezone Map](http://www.brooksbaseball.net/pfxVB/zoneTrack.php?month=" + date_object.strftime(
                    "%m") + "&day=" + date_object.strftime("%d") + "&year=" + date_object.strftime(
                    "%Y") + "&game=gid_" + game.get('gameday_link') + "%2F)|\n"
                header = header + "|**Radio:** "
                if not isinstance(broadcast[0][1].text, type(None)):
                    header = header + broadcast[0][1].text
                if not isinstance(broadcast[1][1].text, type(None)):
                    header = header + ", " + broadcast[1][1].text
                header = header + "|**Notes:** [Away](http://mlb.mlb.com/mlb/presspass/gamenotes.jsp?c_id=" + notes[
                    1] + "), [Home](http://mlb.mlb.com/mlb/presspass/gamenotes.jsp?c_id=" + notes[0] + ")|\n"
                header = header + "\n\n"
                print "Returning header..."
                return header
                break
            except:
                print "Missing data for header, returning first pitch time..."
                return header
                break


    def generateboxscore(self,files):
        boxscore = ""
        while True:
            try:
                homebatters = []
                awaybatters = []
                homepitchers = []
                awaypitchers = []
                game = files["boxscore"].get('data').get('boxscore')
                team = files["linescore"].get('data').get('game')
                batting = game.get('batting')
                for i in range(0, len(batting)):
                    players = batting[i].get('batter')
                    for b in range(0, len(players)):
                        if players[b].get('bo') != None:
                            if batting[i].get('team_flag') == "home":
                                homebatters.append(
                                    player.batter(players[b].get('name'), players[b].get('pos'), players[b].get('ab'),
                                                  players[b].get('r'), players[b].get('h'), players[b].get('rbi'),
                                                  players[b].get('bb'), players[b].get('so'), players[b].get('avg'),
                                                  players[b].get('id')))
                            else:
                                awaybatters.append(
                                    player.batter(players[b].get('name'), players[b].get('pos'), players[b].get('ab'),
                                                  players[b].get('r'), players[b].get('h'), players[b].get('rbi'),
                                                  players[b].get('bb'), players[b].get('so'), players[b].get('avg'),
                                                  players[b].get('id')))
                pitching = game.get('pitching')
                for i in range(0, len(pitching)):
                    players = pitching[i].get('pitcher')
                    if type(players) is list:
                        for p in range(0, len(players)):
                            if pitching[i].get('team_flag') == "home":
                                homepitchers.append(
                                    player.pitcher(players[p].get('name'), players[p].get('out'), players[p].get('h'),
                                                   players[p].get('r'), players[p].get('er'), players[p].get('bb'),
                                                   players[p].get('so'), players[p].get('np'), players[p].get('s'),
                                                   players[p].get('era'), players[p].get('id')))
                            else:
                                awaypitchers.append(
                                    player.pitcher(players[p].get('name'), players[p].get('out'), players[p].get('h'),
                                                   players[p].get('r'), players[p].get('er'), players[p].get('bb'),
                                                   players[p].get('so'), players[p].get('np'), players[p].get('s'),
                                                   players[p].get('era'), players[p].get('id')))
                    elif type(players) is dict:
                        if pitching[i].get('team_flag') == "home":
                            homepitchers.append(
                                player.pitcher(players.get('name'), players.get('out'), players.get('h'), players.get('r'),
                                               players.get('er'), players.get('bb'), players.get('so'), players.get('np'),
                                               players.get('s'), players.get('era'), players.get('id')))
                        else:
                            awaypitchers.append(
                                player.pitcher(players.get('name'), players.get('out'), players.get('h'), players.get('r'),
                                               players.get('er'), players.get('bb'), players.get('so'), players.get('np'),
                                               players.get('s'), players.get('era'), players.get('id')))
                while len(homebatters) < len(awaybatters):
                    homebatters.append(player.batter())
                while len(awaybatters) < len(homebatters):
                    awaybatters.append(player.batter())
                while len(homepitchers) < len(awaypitchers):
                    homepitchers.append(player.pitcher())
                while len(awaypitchers) < len(homepitchers):
                    awaypitchers.append(player.pitcher())
                boxscore = boxscore + team.get('away_team_name') + "|Pos|AB|R|H|RBI|BB|SO|BA|"
                boxscore = boxscore + team.get('home_team_name') + "|Pos|AB|R|H|RBI|BB|SO|BA|"
                boxscore = boxscore + "\n"
                boxscore = boxscore + ":--|:--|:--|:--|:--|:--|:--|:--|:--|"
                boxscore = boxscore + ":--|:--|:--|:--|:--|:--|:--|:--|:--|"
                boxscore = boxscore + "\n"
                for i in range(0, len(homebatters)):
                    boxscore = boxscore + str(awaybatters[i]) + "|" + str(homebatters[i]) + "\n"
                boxscore = boxscore + "\n"
                boxscore = boxscore + team.get('away_team_name') + "|IP|H|R|ER|BB|SO|P-S|ERA|"
                boxscore = boxscore + team.get('home_team_name') + "|IP|H|R|ER|BB|SO|P-S|ERA|"
                boxscore = boxscore + "\n"
                boxscore = boxscore + ":--|:--|:--|:--|:--|:--|:--|:--|:--|"
                boxscore = boxscore + ":--|:--|:--|:--|:--|:--|:--|:--|:--|"
                boxscore = boxscore + "\n"
                for i in range(0, len(homepitchers)):
                    boxscore = boxscore + str(awaypitchers[i]) + "|" + str(homepitchers[i]) + "\n"
                boxscore = boxscore + "\n\n"
                print "Returning boxscore..."
                return boxscore
                break
            except:
                print "Missing data for boxscore, returning blank text..."
                return boxscore
                break


    def generatelinescore(self,files):
        linescore = ""
        while True:
            try:
                game = files["linescore"].get('data').get('game')
                subreddits = self.getsubreddits(game.get('home_team_name'), game.get('away_team_name'))
                lineinfo = game.get('linescore')
                innings = len(lineinfo) if len(lineinfo) > 9 else 9
                linescore = linescore + "Linescore|"
                for i in range(1, innings + 1):
                    linescore = linescore + str(i) + "|"
                linescore = linescore + "R|H|E\n"
                for i in range(0, innings + 4):
                    linescore = linescore + ":--|"
                linescore = linescore + "\n" + "[" + game.get('away_team_name') + "](" + subreddits[1] + ")" + "|"
                x = 1
                if type(lineinfo) is list:
                    for v in lineinfo:
                        linescore = linescore + v.get('away_inning_runs') + "|"
                        x = x + 1
                elif type(lineinfo) is dict:
                    linescore = linescore + lineinfo.get('away_inning_runs') + "|"
                    x = x + 1
                for i in range(x, innings + 1):
                    linescore = linescore + "|"
                linescore = linescore + game.get('away_team_runs') + "|" + game.get('away_team_hits') + "|" + game.get(
                    'away_team_errors')
                linescore = linescore + "\n" + "[" + game.get('home_team_name') + "](" + subreddits[0] + ")" "|"
                x = 1
                if type(lineinfo) is list:
                    for v in lineinfo:
                        linescore = linescore + v.get('home_inning_runs') + "|"
                        x = x + 1
                elif type(lineinfo) is dict:
                    linescore = linescore + lineinfo.get('home_inning_runs') + "|"
                    x = x + 1
                for j in range(x, innings + 1):
                    linescore = linescore + "|"
                linescore = linescore + game.get('home_team_runs') + "|" + game.get('home_team_hits') + "|" + game.get(
                    'home_team_errors')
                linescore = linescore + "\n\n"
                print "Returning linescore..."
                return linescore
                break
            except:
                print "Missing data for linescore, returning blank text..."
                return linescore
                break


    def generatescoringplays(self,files):
        scoringplays = ""
        while True:
            try:
                root = files["scores"].getroot()
                scores = root.findall("score")
                currinning = ""
                scoringplays = scoringplays + "Inning|Scoring Play Description|Score\n"
                scoringplays = scoringplays + ":--|:--|:--\n"
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

                    actions = s.findall("action")
                    try:
                        if s.find('atbat').get('score') == "T":
                            scoringplays = scoringplays + s.find('atbat').get('des')
                        elif s.find('action').get("score") == "T":
                            scoringplays = scoringplays + s.find('action').get('des')
                        else:
                            scoringplays = scoringplays + s.get('pbp')
                    except:
                        scoringplays = scoringplays + "Scoring play description currently unavailable."

                    scoringplays = scoringplays + "|"
                    if int(s.get("home")) < int(s.get("away")):
                        scoringplays = scoringplays + s.get("away") + "-" + s.get("home")
                    elif int(s.get("home")) > int(s.get("away")):
                        scoringplays = scoringplays + s.get("home") + "-" + s.get("away")
                    else:
                        scoringplays = scoringplays + s.get("home") + "-" + s.get("away")
                    scoringplays = scoringplays + "\n"
                scoringplays = scoringplays + "\n\n"
                print "Returning scoringplays..."
                return scoringplays
                break
            except:
                print "Missing data for scoringplays, returning blank text..."
                return scoringplays
                break


    def generatehighlights(self,files):
        highlight = ""
        while True:
            try:
                root = files["highlights"].getroot()
                video = root.findall("media")
                highlight = highlight + "|Highlight|Description\n"
                highlight = highlight + "|:-|:-|\n"
                for v in video:
                    if v.get('type') == "video":
                        highlight = highlight + "|[" + v.find("duration").text + "](" + v.find("url").text + ")|" + v.find(
                            "headline").text + "|\n"
                print "Returning highlight..."
                return highlight
                break
            except:
                print "Missing data for highlight, returning blank text..."
                return highlight
                break


    def generatedecisions(self,files):
        decisions = ""
        while True:
            try:
                homepitchers = [];
                awaypitchers = []
                game = files["boxscore"].get('data').get('boxscore')
                team = files["linescore"].get('data').get('game')
                subreddits = self.getsubreddits(team.get('home_team_name'), team.get('away_team_name'))
                pitching = game.get('pitching')
                for i in range(0, len(pitching)):
                    players = pitching[i].get('pitcher')
                    if type(players) is list:
                        for p in range(0, len(players)):
                            if pitching[i].get('team_flag') == "home":
                                homepitchers.append(
                                    player.decision(players[p].get('name'), players[p].get('note'), players[p].get('id')))
                            else:
                                awaypitchers.append(
                                    player.decision(players[p].get('name'), players[p].get('note'), players[p].get('id')))
                    elif type(players) is dict:
                        if pitching[i].get('team_flag') == "home":
                            homepitchers.append(
                                player.decision(players.get('name'), players.get('note'), players.get('id')))
                        else:
                            awaypitchers.append(
                                player.decision(players.get('name'), players.get('note'), players.get('id')))
                decisions = decisions + "|Decisions||" + "\n"
                decisions = decisions + "|:--|:--|" + "\n"
                decisions = decisions + "|" + "[" + team.get('away_team_name') + "](" + subreddits[1] + ")|"
                for i in range(0, len(awaypitchers)):
                    decisions = decisions + str(awaypitchers[i]) + " "
                decisions = decisions + "\n" + "|" + "[" + team.get('home_team_name') + "](" + subreddits[0] + ")|"
                for i in range(0, len(homepitchers)):
                    decisions = decisions + str(homepitchers[i])
                decisions = decisions + "\n\n"
                print "Returning decisions..."
                return decisions
                break
            except:
                print "Missing data for decisions, returning blank text..."
                return decisions
                break


    def generatestatus(self,files):
        status = ""
        while True:
            try:
                game = files["linescore"].get('data').get('game')
                if game.get('status') == "Final":
                    s = files["linescore"].get('data').get('game')
                    status = status + "##FINAL: "
                    if int(s.get("home_team_runs")) < int(s.get("away_team_runs")):
                        status = status + s.get("away_team_runs") + "-" + s.get("home_team_runs") + " " + s.get(
                            "away_team_name") + "\n"
                        status = status + self.generatedecisions(files)
                        print "Returning status..."
                        return status
                        break
                    elif int(s.get("home_team_runs")) > int(s.get("away_team_runs")):
                        status = status + s.get("home_team_runs") + "-" + s.get("away_team_runs") + " " + s.get(
                            "home_team_name") + "\n"
                        status = status + self.generatedecisions(files)
                        print "Returning status..."
                        return status
                        break
                    elif int(s.get("home_team_runs")) == int(s.get("away_team_runs")):
                        status = status + "TIE"
                        print "Returning status..."
                        return status
                        break
                elif game.get('status') == "Completed Early":
                    status = status + "##COMPLETED EARLY: "
                    if int(s.get("home_team_runs")) < int(s.get("away_team_runs")):
                        status = status + s.get("away_team_runs") + "-" + s.get("home_team_runs") + " " + s.get(
                            "away_team_name") + "\n"
                        status = status + self.generatedecisions(files)
                        print "Returning status..."
                        return status
                        break
                    elif int(s.get("home_team_runs")) > int(s.get("away_team_runs")):
                        status = status + s.get("home_team_runs") + "-" + s.get("away_team_runs") + " " + s.get(
                            "home_team_name") + "\n"
                        status = status + self.generatedecisions(files)
                        print "Returning status..."
                        return status
                        break
                    elif int(s.get("home_team_runs")) == int(s.get("away_team_runs")):
                        status = status + "TIE"
                        print "Returning status..."
                        return status
                        break 
                elif game.get('status') == "Postponed":
                    status = status + "##POSTPONED\n\n"
                    print "Returning status..."
                    return status
                    break
                elif game.get('status') == "Suspended":
                    status = status + "##SUSPENDED\n\n"
                    print "Returning status..."
                    return status
                    break
                elif game.get('status') == "Cancelled":
                    status = status + "##CANCELLED\n\n"
                    print "Returning status..."
                    return status
                    break            
                else:
                    print "Status not final or postponed, returning blank text..."
                    return status
                    break
            except:
                print "Missing data for status, returning blank text..."
                return status
                break

    def generatefooter(self):
        footer = ""
        footer += "**Remember to sort by new to keep up!**"
        return footer


    def getsubreddits(self, homename, awayname):
        subreddits = []
        options = {
            "Twins": "/r/minnesotatwins",
            "White Sox": "/r/WhiteSox",
            "Tigers": "/r/MotorCityKitties",
            "Royals": "/r/KCRoyals",
            "Indians": "/r/WahoosTipi",
            "Rangers": "/r/TexasRangers",
            "Astros": "/r/Astros",
            "Athletics": "/r/OaklandAthletics",
            "Angels": "/r/AngelsBaseball",
            "Mariners": "/r/Mariners",
            "Red Sox": "/r/RedSox",
            "Yankees": "/r/NYYankees",
            "Blue Jays": "/r/TorontoBlueJays",
            "Rays": "/r/TampaBayRays",
            "Orioles": "/r/Orioles",
            "Cardinals": "/r/Cardinals",
            "Reds": "/r/Reds",
            "Pirates": "/r/Buccos",
            "Cubs": "/r/CHICubs",
            "Brewers": "/r/Brewers",
            "Giants": "/r/SFGiants",
            "Diamondbacks": "/r/azdiamondbacks",
            "D-backs": "/r/azdiamondbacks",
            "Rockies": "/r/ColoradoRockies",
            "Dodgers": "/r/Dodgers",
            "Padres": "/r/Padres",
            "Phillies": "/r/Phillies",
            "Mets": "/r/NewYorkMets",
            "Marlins": "/r/letsgofish",
            "Nationals": "/r/Nationals",
            "Braves": "/r/Braves"
        }
        subreddits.append(options[homename])
        subreddits.append(options[awayname])
        return subreddits


    def getnotes(self, homename, awayname):
        notes = []
        options = {
            "Twins": "min",
            "White Sox": "cws",
            "Tigers": "det",
            "Royals": "kc",
            "Indians": "cle",
            "Rangers": "tex",
            "Astros": "hou",
            "Athletics": "oak",
            "Angels": "ana",
            "Mariners": "sea",
            "Red Sox": "bos",
            "Yankees": "nyy",
            "Blue Jays": "tor",
            "Rays": "tb",
            "Orioles": "bal",
            "Cardinals": "stl",
            "Reds": "cin",
            "Pirates": "pit",
            "Cubs": "chc",
            "Brewers": "mil",
            "Giants": "sf",
            "Diamondbacks": "ari",
            "D-backs": "ari",
            "Rockies": "col",
            "Dodgers": "la",
            "Padres": "sd",
            "Phillies": "phi",
            "Mets": "nym",
            "Marlins": "mia",
            "Nationals": "was",
            "Braves": "atl"
        }
        notes.append(options[homename])
        notes.append(options[awayname])
        return notes
