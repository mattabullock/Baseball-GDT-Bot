# does all the post generating and editing

import player

import xml.etree.ElementTree as ET
import urllib2
import simplejson as json
from datetime import datetime, timedelta
import time

class Editor:

    options = {
            "Twins": { "sub": "/r/minnesotatwins", "tag": "[MIN](/r/minnesotatwins)", "notes": "min" },
            "White Sox": { "sub": "/r/WhiteSox", "tag": "[CWS](/r/WhiteSox)", "notes": "cws" },
            "Tigers": { "sub": "/r/MotorCityKitties", "tag": "[DET](/r/MotorCityKitties)", "notes": "det" },
            "Royals": { "sub": "/r/KCRoyals", "tag": "[KCR](/r/KCRoyals)", "notes": "kc" },
            "Indians": { "sub": "/r/WahoosTipi", "tag": "[CLE](/r/WahoosTipi)", "notes": "cle" },
            "Rangers": { "sub": "/r/TexasRangers", "tag": "[TEX](/r/TexasRangers)", "notes": "tex" },
            "Astros": { "sub": "/r/Astros", "tag": "[HOU](/r/Astros)", "notes": "hou" },
            "Athletics": { "sub": "/r/OaklandAthletics", "tag": "[OAK](/r/OaklandAthletics)", "notes": "oak" },
            "Angels": { "sub": "/r/AngelsBaseball", "tag": "[LAA](/r/AngelsBaseball)", "notes": "ana" },
            "Mariners": { "sub": "/r/Mariners", "tag": "[SEA](/r/Mariners)", "notes": "sea" },
            "Red Sox": { "sub": "/r/RedSox", "tag": "[BOS](/r/RedSox)", "notes": "bos" },
            "Yankees": { "sub": "/r/NYYankees", "tag": "[NYY](/r/NYYankees)", "notes": "nyy" },
            "Blue Jays": { "sub": "/r/TorontoBlueJays", "tag": "[TOR](/r/TorontoBlueJays)", "notes": "tor" },
            "Rays": { "sub": "/r/TampaBayRays", "tag": "[TBR](/r/TampaBayRays)", "notes": "tb" },
            "Orioles": { "sub": "/r/Orioles", "tag": "[BAL](/r/Orioles)", "notes": "bal" },
            "Cardinals": { "sub": "/r/Cardinals", "tag": "[STL](/r/Cardinals)", "notes": "stl" },
            "Reds": { "sub": "/r/Reds", "tag": "[CIN](/r/Reds)", "notes": "cin" },
            "Pirates": { "sub": "/r/Buccos", "tag": "[PIT](/r/Buccos)", "notes": "pit" },
            "Cubs": { "sub": "/r/CHICubs", "tag": "[CHC](/r/CHICubs)", "notes": "chc" },
            "Brewers": { "sub": "/r/Brewers", "tag": "[MIL](/r/Brewers)", "notes": "mil" },
            "Giants": { "sub": "/r/SFGiants", "tag": "[SFG](/r/SFGiants)", "notes": "sf" },
            "Diamondbacks": { "sub": "/r/azdiamondbacks", "tag": "[ARI](/r/azdiamondbacks)", "notes": "ari" },
            "D-backs": { "sub": "/r/azdiamondbacks", "tag": "[ARI](/r/azdiamondbacks)", "notes": "ari" },
            "Rockies": { "sub": "/r/ColoradoRockies", "tag": "[COL](/r/ColoradoRockies)", "notes": "col" },
            "Dodgers": { "sub": "/r/Dodgers", "tag": "[LAD](/r/Dodgers)", "notes": "la" },
            "Padres": { "sub": "/r/Padres", "tag": "[SDP](/r/Padres)", "notes": "sd" },
            "Phillies": { "sub": "/r/Phillies", "tag": "[PHI](/r/Phillies)", "notes": "phi" },
            "Mets": { "sub": "/r/NewYorkMets", "tag": "[NYM](/r/NewYorkMets)", "notes": "nym" },
            "Marlins": { "sub": "/r/letsgofish", "tag": "[MIA](/r/letsgofish)", "notes": "mia" },
            "Nationals": { "sub": "/r/Nationals", "tag": "[WSH](/r/Nationals)", "notes": "was" },
            "Braves": { "sub": "/r/Braves", "tag": "[ATL](/r/Braves)", "notes": "atl"}
        }

    def __init__(self, time_info, pre_thread_settings, thread_settings, post_thread_settings):
        (self.time_zone,self.time_change,) = time_info
        (self.pre_thread_tag, self.pre_thread_time,
            (self.pre_probables, self.pre_first_pitch)
        ) = pre_thread_settings
        (self.thread_tag,
            (self.header, self.box_score,
             self.line_score, self.scoring_plays,
             self.highlights, self.footer)
        ) = thread_settings
        (self.post_thread_tag,
            (self.post_header, self.post_box_score,
             self.post_line_score, self.post_scoring_plays,
             self.post_highlights, self.post_footer)
        ) = post_thread_settings

    def generate_title(self, gameURL, thread):
        if thread == "pre": title = self.pre_thread_tag + " "
        elif thread == "game": title = self.thread_tag + " "
        elif thread == "post": title = self.post_thread_tag + " "
        while True:
            try:
                response = urllib2.urlopen(gameURL)
                break
            except:
                print "Couldn't find linescore.json for title, trying again..."
                time.sleep(20)
        game = json.load(response)["gameData"]
        timeData = game["datetime"]
        if "timeDate" in timeData:
            timestring = timeData["timeDate"] + " " + timeData["ampm"]
            date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
        else:
            timestring = timeData["originalDate"] + " " + timeData["time"] + " " + timeData["ampm"]
            date_object = datetime.strptime(timestring, "%Y-%m-%d %I:%M %p")
        awayTeamName = game["teams"]["away"]["name"] if isinstance(game["teams"]["away"]["name"], basestring) else game["teams"]["away"]["name"]["full"]
        homeTeamName = game["teams"]["home"]["name"] if isinstance(game["teams"]["home"]["name"], basestring) else game["teams"]["home"]["name"]["full"]
        title += awayTeamName + " (" + str(game["teams"]["away"]["record"]["wins"]) + "-" + str(game["teams"]["away"]["record"]["losses"]) + ")"
        title += " @ "
        title += homeTeamName + " (" + str(game["teams"]["home"]["record"]["wins"]) + "-" + str(game["teams"]["home"]["record"]["losses"]) + ")"
        title += " - "
        title += date_object.strftime("%B %d, %Y")
        print "Returning title..."
        return title

    def generate_pre_code(self, games):
        code = ""
        for g in games:
            response = urllib2.urlopen(g)
            gameData = json.load(response)
            response = urllib2.urlopen("https://statsapi.mlb.com/api/v1/game/" +
                                        gameData["gameData"]["game"]["pk"]+ "/content")
            mediaData = json.load(response)
            if self.pre_probables: code += self.generate_pre_probables(gameData, mediaData)
            if self.pre_first_pitch: code += self.generate_pre_first_pitch(gameData)
            code += "\n\n"
        print "Returning all code..."
        return code

    def generate_pre_probables(self, gameData, mediaData):
        probables = ""
        try:
            homeTeamName = gameData["gameData"]["teams"]["home"]["teamName"]
            awayTeamName = gameData["gameData"]["teams"]["away"]["teamName"]
            homeSub = self.options[homeTeamName]["sub"]
            awaySub = self.options[awayTeamName]["sub"]

            videoBroadcast = mediaData["media"]["epg"][0]
            audioBroadcast = mediaData["media"]["epg"][2]

            homeVideo = ""
            awayVideo = ""
            for item in videoBroadcast["items"]:
                if item["callLetters"]:
                    if item["type"] is "HOME":
                        homeVideo += item["callLetters"] + ", "
                    if item["type"] is "AWAY":
                        awayVideo += item["callLetters"] + ", "

            homeVideo = homeVideo[:-2] if homeVideo else ""
            awayVideo = awayVideo[:-2] if awayVideo else ""

            homeAudio = ""
            awayAudio = ""
            for item in audioBroadcast["items"]:
                if item["callLetters"]:
                    if item["type"] is "HOME":
                        homeAudio += item["callLetters"] + ", "
                    if item["type"] is "AWAY":
                        awayAudio += item["callLetters"] + ", "

            homeAudio = homeAudio[:-2] if homeAudio else ""
            awayAudio = awayAudio[:-2] if awayAudio else ""


            homePitcherID = gameData["gameData"]["probablePitchers"]["home"]["id"]
            awayPitcherID = gameData["gameData"]["probablePitchers"]["away"]["id"]
            homePitcherName = gameData["gameData"]["probablePitchers"]["home"]["fullName"]
            awayPitcherName = gameData["gameData"]["probablePitchers"]["away"]["fullName"]
            homePitcherStats = gameData["liveData"]["boxscore"]["teams"]["home"]["players"]["ID" + homePitcherID]["seasonStats"]["pitching"]
            awayPitcherStats = gameData["liveData"]["boxscore"]["teams"]["away"]["players"]["ID" + awayPitcherID]["seasonStats"]["pitching"]

            homePitcher = "[" + homePitcherName + "](" + "http://mlb.mlb.com/team/player.jsp?player_id=" + homePitcherID + ")"
            homePitcher += " (" + homePitcherStats["wins"] + "-" + homePitcherStats["losses"] + ", " + homePitcherStats["era"] + ")"
            awayPitcher = "[" + awayPitcherName + "](" + "http://mlb.mlb.com/team/player.jsp?player_id=" + awayPitcherID + ")"
            awayPitcher += " (" + awayPitcherStats["wins"] + "-" + awayPitcherStats["losses"] + ", " + awayPitcherStats["era"] + ")"

            preview = "[Preview](http://mlb.mlb.com/mlb/gameday/index.jsp?gid=" + gameData["gameData"]["game"]["id"] + ")\n\n"

            probables  = "| |Pitcher|TV|Radio|Preview\n"
            probables += "|-|-|-|-|-\n"
            probables += "[" + awayTeamName + "](" + awaySub + ")|" + awayPitcher + "|" + awayVideo + "|" + awayAudio + "|" + preview + "\n"
            probables += "[" + homeTeamName + "](" + homeSub + ")|" + homePitcher + "|" + homeVideo + "|" + homeAudio + "|" + preview + "\n"

            probables += "\n"

            return probables
        except:
            print "Missing data for probables, returning empty string..."
            return probables

    def generate_pre_first_pitch(self, gameData):
        first_pitch = ""
        try:
            # Get time data
            timeData = gameData["datetime"]
            if "timeDate" in timeData:
                timestring = timeData["timeDate"] + " " + timeData["ampm"]
                date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
            else:
                timestring = timeData["originalDate"] + " " + timeData["time"] + " " + timeData["ampm"]
                date_object = datetime.strptime(timestring, "%Y-%m-%d %I:%M %p")
            t = timedelta(hours=self.time_change)
            timezone = self.time_zone
            date_object = date_object - t
            first_pitch = "**First Pitch:** " + date_object.strftime("%I:%M %p ") + timezone + "\n\n"

            return first_pitch
        except:
            print "Missing data for first_pitch, returning empty string..."
            return first_pitch

    def generate_code(self, gameURL, thread):
        code = ""
        try:
            response = urllib2.urlopen(gameURL)
            gameData = json.load(response)
            response = urllib2.urlopen("https://statsapi.mlb.com/api/v1/game/" +
                                        gameData["gameData"]["game"]["pk"]+ "/content")
            mediaData = json.load(response)
        except Exception as e:
            print e

        if thread == "game":
            if self.header: code += self.generate_header(gameData, mediaData)
            if self.box_score: code += self.generate_boxscore(gameData)
            if self.line_score: code += self.generate_linescore(gameData)
            if self.scoring_plays: code += self.generate_scoring_plays(gameData)
            if self.highlights: code += self.generate_highlights(mediaData)
            if self.footer: code += self.footer + "\n\n"
        elif thread == "post":
            if self.post_header: code += self.generate_header(gameData, mediaData)
            if self.post_box_score: code += self.generate_boxscore(gameData)
            if self.post_line_score: code += self.generate_linescore(gameData)
            if self.post_scoring_plays: code += self.generate_scoring_plays(gameData)
            if self.post_highlights: code += self.generate_highlights(mediaData)
            if self.post_footer: code += self.post_footer + "\n\n"
        code += self.generate_status(gameData)
        print "Returning all code..."
        return code

    def generate_header(self, data, mediaData):
        header = ""
        # try:
        gameData = data["gameData"]
        game = gameData["game"]
        timeData = gameData["datetime"]
        weather = gameData["weather"]
        teams = gameData["teams"]
        videoBroadcast = mediaData["media"]["epg"][0]
        audioBroadcast = mediaData["media"]["epg"][2]

        # Get time data
        if "timeDate" in timeData:
            timestring = timeData["timeDate"] + " " + timeData["ampm"]
            date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
        else:
            timestring = timeData["originalDate"] + " " + timeData["time"] + " " + timeData["ampm"]
            date_object = datetime.strptime(timestring, "%Y-%m-%d %I:%M %p")
        t = timedelta(hours=self.time_change)
        timezone = self.time_zone
        date_object = date_object - t

        # Build out header
        header = "**First Pitch:** " + date_object.strftime("%I:%M %p ") + timezone + "\n\n"
        header += "[Preview](http://mlb.mlb.com/mlb/gameday/index.jsp?gid=" + game["id"] + ")\n\n"
        header += "|Game Info|Links|\n"
        header += "|:--|:--|\n"
        header += "|**First Pitch:** " + date_object.strftime("%I:%M %p ") + timezone + " @ " + gameData["venue"]["name"] + "|[Gameday](http://mlb.mlb.com/mlb/gameday/index.jsp?gid=" + game["id"] + ")|\n"
        header += "|**Weather:** " + weather["condition"] + ", " + weather["temp"] + " F, " + "Wind " + weather["wind"]
        if "Y" in game["doubleHeader"] or "S" in game["doubleHeader"]:
            header += "|[Game Graph](http://www.fangraphs.com/livewins.aspx?date=" + date_object.strftime("%Y-%m-%d") + "&team=" + teams["home"]["name"]["brief"] + "&dh=" + game["gameNumber"] + "&season=" + date_object.strftime("%Y") + ")|\n"
        else:
            header += "|[Game Graph](http://www.fangraphs.com/livewins.aspx?date=" + date_object.strftime("%Y-%m-%d") + "&team=" + teams["home"]["name"]["brief"] + "&dh=0&season=" + date_object.strftime("%Y") + ")|\n"
        header += "|**TV:** "

        video = False
        for item in videoBroadcast["items"]:
            if item["callLetters"]:
                header += item["callLetters"] + ", "
                video = True
        if video:
            header = header[:-2]
        header += "|[Strikezone Map](http://www.brooksbaseball.net/pfxVB/zoneTrack.php?month=" + date_object.strftime("%m") + "&day=" + date_object.strftime("%d") + "&year=" + date_object.strftime("%Y") + "&game=gid_" + game["id"] + "%2F)|\n"
        header += "|**Radio:** "

        audio = False
        for item in audioBroadcast["items"]:
            if item["callLetters"]:
                header += item["callLetters"] + ", "
                audio = True
        if audio:
            header = header[:-2]
        header += "|**Notes:** [Away](http://mlb.mlb.com/mlb/presspass/gamenotes.jsp?c_id=" + Editor.options[teams["away"]["name"]["brief"]]["notes"] + "), [Home](http://mlb.mlb.com/mlb/presspass/gamenotes.jsp?c_id=" + Editor.options[teams["home"]["name"]["brief"]]["notes"] + ")|\n"
        header += "\n\n"
        print "Returning header..."
        return header
        # except Exception e:
            # print "Missing data for header, returning empty string..."
            # return header

    def generate_boxscore(self,data):
        boxscore = ""
        # try:
        unorderedAwayBatters = {}
        unorderedHomeBatters = {}
        awayBatters = []
        homeBatters = []
        awayPitchers = []
        homePitchers = []

        awayTeam = data["liveData"]["boxscore"]["teams"]["away"]
        homeTeam = data["liveData"]["boxscore"]["teams"]["home"]
        awayTeamInfo = data["gameData"]["teams"]["away"]
        homeTeamInfo = data["gameData"]["teams"]["home"]

        # Get unordered batters
        for batterID in awayTeam["players"]:
            batter = awayTeam["players"][batterID]
            gameStats = batter["gameStats"]["batting"]
            seasonStats = batter["seasonStats"]["batting"]
            if gameStats["battingOrder"] is not None:
                batterName = batter["name"]["boxname"].encode('utf-8').strip()
                unorderedAwayBatters[gameStats["battingOrder"]] = \
                    player.batter(batterName, batter["position"], gameStats["atBats"],
                            gameStats["runs"], gameStats["hits"], gameStats["rbi"], gameStats["baseOnBalls"],
                            gameStats["strikeOuts"], seasonStats["avg"],
                            seasonStats["obp"], seasonStats["ops"], batter["id"])

        for batterID in homeTeam["players"]:
            batter = homeTeam["players"][batterID]
            gameStats = batter["gameStats"]["batting"]
            seasonStats = batter["seasonStats"]["batting"]
            if gameStats["battingOrder"] is not None:
                batterName = batter["name"]["boxname"].encode('utf-8').strip()
                unorderedHomeBatters[gameStats["battingOrder"]] = \
                    player.batter(batterName, batter["position"], gameStats["atBats"],
                            gameStats["runs"], gameStats["hits"], gameStats["rbi"], gameStats["baseOnBalls"],
                            gameStats["strikeOuts"], seasonStats["avg"],
                            seasonStats["obp"], seasonStats["ops"], batter["id"])

        # Order batters in correct order
        for battingOrder in sorted(unorderedAwayBatters):
            awayBatters.append(unorderedAwayBatters[battingOrder])
        for battingOrder in sorted(unorderedHomeBatters):
            homeBatters.append(unorderedHomeBatters[battingOrder])

        # Get ordered pitchers
        for pitcherID in awayTeam["pitchers"]:
            pitcher = awayTeam["players"]["ID" + pitcherID]
            gameStats = pitcher["gameStats"]["pitching"]
            seasonStats = pitcher["seasonStats"]["pitching"]
            pitcherName = pitcher["name"]["boxname"].encode('utf-8').strip()
            awayPitchers.append(
                    player.pitcher(pitcherName, gameStats["inningsPitched"], gameStats["hits"],
                        gameStats["runs"], gameStats["earnedRuns"], gameStats["baseOnBalls"],
                        gameStats["strikeOuts"], gameStats["pitchesThrown"], gameStats["strikes"],
                        seasonStats["era"], pitcher["id"])
                    )

        for pitcherID in homeTeam["pitchers"]:
            pitcher = homeTeam["players"]["ID" + pitcherID]
            gameStats = pitcher["gameStats"]["pitching"]
            seasonStats = pitcher["seasonStats"]["pitching"]
            pitcherName = pitcher["name"]["boxname"].encode('utf-8').strip()
            homePitchers.append(
                    player.pitcher(pitcherName, gameStats["inningsPitched"], gameStats["hits"],
                        gameStats["runs"], gameStats["earnedRuns"], gameStats["baseOnBalls"],
                        gameStats["strikeOuts"], gameStats["pitchesThrown"], gameStats["strikes"],
                        seasonStats["era"], pitcher["id"])
                    )

        # Make home and away same size for the chart
        while len(homeBatters) < len(awayBatters):
            homeBatters.append(player.batter())
        while len(awayBatters) < len(homeBatters):
            awayBatters.append(player.batter())
        while len(homePitchers) < len(awayPitchers):
            homePitchers.append(player.pitcher())
        while len(awayPitchers) < len(homePitchers):
            awayPitchers.append(player.pitcher())

        boxscore += awayTeamInfo["name"]["brief"] + "|Pos|AB|R|H|RBI|BB|SO||"
        boxscore += homeTeamInfo["name"]["brief"] + "|Pos|AB|R|H|RBI|BB|SO||"
        boxscore += "\n"
        boxscore += ":--|:--|:--|:--|:--|:--|:--|:--|:--|"
        boxscore += ":--|:--|:--|:--|:--|:--|:--|:--|:--|"
        boxscore += "\n"
        for i in range(0, len(homeBatters)):
            boxscore += str(awayBatters[i]) + "|" + str(homeBatters[i]) + "\n"
        boxscore += "\n"
        boxscore += awayTeamInfo["name"]["brief"] + "|IP|H|R|ER|BB|SO|P-S|ERA|"
        boxscore += homeTeamInfo["name"]["brief"] + "|IP|H|R|ER|BB|SO|P-S|ERA|"
        boxscore += "\n"
        boxscore += ":--|:--|:--|:--|:--|:--|:--|:--|:--|"
        boxscore += ":--|:--|:--|:--|:--|:--|:--|:--|:--|"
        boxscore += "\n"
        for i in range(0, len(homePitchers)):
            boxscore += str(awayPitchers[i]) + "|" + str(homePitchers[i]) + "\n"
        boxscore += "\n\n"

        print "Returning boxscore..."
        return boxscore
        # except:
            # print "Missing data for boxscore, returning blank text..."
            # return boxscore

    def generate_linescore(self, data):
        linescore = ""
        # try:
        game = data["gameData"]
        awayTeamName = game["teams"]["away"]["name"]["brief"]
        homeTeamName = game["teams"]["home"]["name"]["brief"]

        lineInfo = data["liveData"]["linescore"]
        inningsInfo = data["liveData"]["linescore"]["innings"]
        numInnings = lineInfo["currentInning"] if lineInfo["currentInning"] > 9 else 9

        # Table headers
        linescore += "Linescore|"
        for i in range(1, numInnings + 1):
            linescore += str(i) + "|"
        linescore += "R|H|E\n"
        for i in range(0, numInnings + 4):
            linescore += ":--|"

        # Away team linescore
        linescore += "\n" + "[" + awayTeamName + "](" + Editor.options[awayTeamName]["sub"] + ")" + "|"
        for i in range(0, numInnings):
            linescore += inningsInfo[i]["away"].encode('utf-8').strip() + "|" if i < len(inningsInfo) and "away" in inningsInfo[i] else "|"
        linescore += lineInfo["away"]["runs"] + "|" + lineInfo["away"]["hits"] + "|" + lineInfo["away"]["errors"]

        # Home team linescore
        linescore += "\n" + "[" + homeTeamName + "](" + Editor.options[homeTeamName]["sub"] + ")" "|"
        for i in range(0, numInnings):
            linescore += inningsInfo[i]["home"].encode('utf-8').strip() + "|" if i < len(inningsInfo) and "home" in inningsInfo[i] else "|"
        linescore += lineInfo["home"]["runs"] + "|" + lineInfo["home"]["hits"] + "|" + lineInfo["home"]["errors"]
        linescore += "\n\n"
        print "Returning linescore..."
        return linescore
        # except:
            # print "Missing data for linescore, returning blank text..."
            # return linescore

    def generate_scoring_plays(self, data):
        scoringPlays = ""
        try:
            allPlays = data["liveData"]["plays"]["allPlays"]
            teams = data["gameData"]["teams"]

            scoringPlays += "Inning|Scoring Play Description|Score\n"
            scoringPlays += ":--|:--|:--\n"

            for play in allPlays:
                if play["about"]["isScoringPlay"]:
                    scoringPlays += play["about"]["halfInning"].title() + " " + play["about"]["inning"] + "|"
                    scoringPlays += play["result"]["description"] + "|"

                    # Put winning team's score first
                    if int(play["result"]["homeScore"]) > int(play["result"]["awayScore"]):
                        scoringPlays += play["result"]["homeScore"] + "-" + play["result"]["awayScore"] + " " + teams["home"]["name"]["abbrev"]
                    elif int(play["result"]["homeScore"]) < int(play["result"]["awayScore"]):
                        scoringPlays += play["result"]["awayScore"] + "-" + play["result"]["homeScore"] + " " + teams["away"]["name"]["abbrev"]
                    else:
                        scoringPlays += play["result"]["awayScore"] + "-" + play["result"]["homeScore"]
                    scoringPlays += "\n"

            scoringPlays += "\n\n"
            print "Returning scoringPlays..."
            return scoringPlays
        except:
            print "Missing data for scoringPlays, returning blank text..."
            return scoringPlays

    def generate_highlights(self, data):
        highlightCode = ""
        try:
            highlights = data["highlights"]["live"]["items"]
            highlightCode += "|Team|Highlight|SD|HD|\n"
            highlightCode += "|:--|:--|:--|:--|\n"
            for highlight in highlights:
                try:
                    highlightCode += "|" + Editor.options[highlight["kicker"].replace("Highlights ", "").replace("Top Play ", "")]["tag"]
                except:
                    highlightCode += "|[](/MLB)"
                SDHighlightURL = ""
                HDHighlightURL = ""
                for playback in highlight["playbacks"]:
                    if playback["name"] == "FLASH_1200K_640X360":
                        SDHighlightURL = playback["url"]
                    elif playback["name"] == "FLASH_2500K_1280X720":
                        HDHighlightURL = playback["url"]
                highlightCode += "|" + highlight["headline"] + "|[SD](" + SDHighlightURL + ")|[HD](" + HDHighlightURL + ")|\n"

            highlightCode += "\n\n"
            print "Returning highlight..."
            return highlightCode
        except:
            print "Missing data for highlight, returning blank text..."
            return highlightCode

    def generate_decisions(self, data):
        decisions = ""
        # try:
        homepitchers = []
        awaypitchers = []
        decisionsData = data["liveData"]["linescore"]["pitchers"]
        liveDataTeams = data["liveData"]["boxscore"]["teams"]
        gameDataTeams = data["gameData"]["teams"]
        winningPitcherID = decisionsData["win"]
        losingPitcherID = decisionsData["loss"]
        savePitcherID = decisionsData["save"]
        if "ID" + decisionsData["win"] in liveDataTeams["home"]["players"]:
            winningPitcher = liveDataTeams["home"]["players"]["ID" + winningPitcherID]
            losingPitcher = liveDataTeams["away"]["players"]["ID" + losingPitcherID]
            if decisionsData["save"] is not None:
                savePitcher = liveDataTeams["home"]["players"]["ID" + savePitcherID]
            else:
                savePitcher = None
            winningTeam = gameDataTeams["home"]["name"]["brief"]
            losingTeam = gameDataTeams["away"]["name"]["brief"]
        else:
            winningPitcher = liveDataTeams["away"]["players"]["ID" + winningPitcherID]
            losingPitcher = liveDataTeams["home"]["players"]["ID" + losingPitcherID]
            if decisionsData["save"] is not None:
                savePitcher = liveDataTeams["away"]["players"]["ID" + savePitcherID]
            else:
                savePitcher = None
            winningTeam = gameDataTeams["away"]["name"]["brief"]
            losingTeam = gameDataTeams["home"]["name"]["brief"]

        decisions += "|Decisions||" + "\n"
        decisions += "|:--|:--|" + "\n"
        decisions += "|" + "[" + winningTeam + "](" + Editor.options[winningTeam]["sub"] + ")|"
        decisions += "[" + winningPitcher["name"]["boxname"] + "](http://mlb.mlb.com/team/player.jsp?player_id=" + winningPitcher["id"] + ")"
        decisions += " " + winningPitcher["gameStats"]["pitching"]["note"]
        decisions += "\n"

        decisions += "|" + "[" + losingTeam + "](" + Editor.options[losingTeam]["sub"] + ")|"
        decisions += "[" + losingPitcher["name"]["boxname"] + "](http://mlb.mlb.com/team/player.jsp?player_id=" + losingPitcher["id"] + ")"
        decisions += " " + losingPitcher["gameStats"]["pitching"]["note"]
        decisions += "\n\n"
        print "Returning decisions..."
        return decisions
        # except:
            # print "Missing data for decisions, returning blank text..."
            # return decisions

    def generate_status(self, data):
        status = ""
        # try:
        gameStatus = data["gameData"]["status"]["abstractGameState"]
        linescore = data["liveData"]["linescore"]
        homeTeamRuns = linescore["home"]["runs"]
        awayTeamRuns = linescore["away"]["runs"]
        homeTeamName = data["gameData"]["teams"]["home"]["name"]["brief"]
        awayTeamName = data["gameData"]["teams"]["away"]["name"]["brief"]

        if gameStatus == "Game Over" or gameStatus == "Final":
            status += "## FINAL: "
            if int(homeTeamRuns) < int(awayTeamRuns):
                status += awayTeamRuns + "-" + homeTeamRuns + " " + awayTeamName + "\n\n"
                status += self.generate_decisions(data)
                print "Returning status..."
                return status
            elif int(homeTeamRuns) > int(awayTeamRuns):
                status += homeTeamRuns + "-" + awayTeamRuns + " " + homeTeamName + "\n\n"
                status += self.generate_decisions(data)
                print "Returning status..."
                return status
            elif int(homeTeamRuns) == int(awayTeamRuns):
                status += "TIE"
                print "Returning status..."
                return status
        elif gameStatus == "Completed Early":
            status += "## COMPLETED EARLY: "
            if int(homeTeamRuns) < int(awayTeamRuns):
                status += awayTeamRuns + "-" + homeTeamRuns + " " + awayTeamName + "\n\n"
                status += self.generate_decisions(files)
                print "Returning status..."
                return status
            elif int(homeTeamRuns) > int(awayTeamRuns):
                status += homeTeamRuns + "-" + awayTeamRuns + " " + homeTeamName + "\n\n"
                status += self.generate_decisions(files)
                print "Returning status..."
                return status
            elif int(homeTeamRuns) == int(awayTeamRuns):
                status += "TIE"
                print "Returning status..."
                return status
        elif gameStatus == "Postponed":
            status += "## POSTPONED\n\n"
            print "Returning status..."
            return status
        elif gameStatus == "Suspended":
            status += "## SUSPENDED\n\n"
            print "Returning status..."
            return status
        elif gameStatus == "Cancelled":
            status += "## CANCELLED\n\n"
            print "Returning status..."
            return status
        else:
            print "Status not final or postponed, returning blank text..."
            return status
        # except:
            # print "Missing data for status, returning blank text..."
            # return status
