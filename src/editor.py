# does all the post generating and editing

import player

import xml.etree.ElementTree as ET
import urllib2
import simplejson as json
from datetime import datetime, timedelta
import time

class Editor:

    def __init__(self,time_info,pre_thread_settings,thread_settings,
            post_thread_settings):
        (self.time_zone,self.time_change,) = time_info
        (self.pre_thread_tag, self.pre_thread_time, self.pre_thread_flair,
            (self.pre_probables, self.pre_first_pitch)
        ) = pre_thread_settings
        (self.thread_tag, self.thread_flair, 
            (self.header, self.box_score, 
             self.line_score, self.scoring_plays,
             self.highlights, self.footer)
        ) = thread_settings
        (self.post_thread_tag, self.post_thread_flair, 
            (self.post_header, self.post_box_score, 
             self.post_line_score, self.post_scoring_plays,
             self.post_highlights, self.post_footer)
        ) = post_thread_settings


    def generate_title(self,dir,thread):
        if thread == "pre": title = self.pre_thread_tag + " "
        elif thread == "game": title = self.thread_tag + " "
        elif thread == "post": title = self.post_thread_tag + " "
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

    def generate_pre_code(self,dirs):
        code = ""
        for d in dirs:
            temp_dirs = []
            temp_dirs.append(d + "linescore.json")
            temp_dirs.append(d + "gamecenter.xml")
            files = self.download_pre_files(temp_dirs)
            if self.pre_probables: code = code + self.generate_pre_probables(files)
            if self.pre_first_pitch: code = code + self.generate_pre_first_pitch(files)
            code = code + "\n\n"
        print "Returning all code..."
        return code

    def download_pre_files(self,dirs):
        files = dict()
        response = urllib2.urlopen(dirs[0])
        files["linescore"] = json.load(response)
        response = urllib2.urlopen(dirs[1])
        files["gamecenter"] = ET.parse(response)
        return files


    def generate_pre_probables(self,files):
        probables = ""
        try:
            game = files["linescore"].get('data').get('game')
            subs = self.get_subreddits(game.get('home_team_name'), game.get('away_team_name'))

            root = files["gamecenter"].getroot()
            broadcast = root.find('broadcast')

            if not isinstance(broadcast[0][0].text, type(None)):
                home_tv_broadcast = broadcast[0][0].text
            if not isinstance(broadcast[1][0].text, type(None)):
                away_tv_broadcast = broadcast[1][0].text
            if not isinstance(broadcast[0][1].text, type(None)):
                home_radio_broadcast = broadcast[0][1].text
            if not isinstance(broadcast[1][1].text, type(None)):
                away_radio_broadcast = broadcast[1][1].text

            away_pitcher_obj = game.get('away_probable_pitcher')
            home_pitcher_obj = game.get('home_probable_pitcher')

            away_pitcher = away_pitcher_obj.get('first_name') + " " + away_pitcher_obj.get('last_name')
            away_pitcher = "[" + away_pitcher + "](" + "http://mlb.mlb.com/team/player.jsp?player_id=" + away_pitcher_obj.get('id') + ")"
            away_pitcher += " (" + away_pitcher_obj.get('wins') + "-" + away_pitcher_obj.get('losses') + ", " + away_pitcher_obj.get('era') + ")"
            home_pitcher = home_pitcher_obj.get('first_name') + " " + home_pitcher_obj.get('last_name')
            home_pitcher = "[" + home_pitcher + "](" + "http://mlb.mlb.com/team/player.jsp?player_id=" + home_pitcher_obj.get('id') + ")"
            home_pitcher += " (" + home_pitcher_obj.get('wins') + "-" + home_pitcher_obj.get('losses') + ", " + home_pitcher_obj.get('era') + ")"

            away_preview = "[Link](http://mlb.com" + game.get('away_preview_link') + ")"
            home_preview = "[Link](http://mlb.com" + game.get('home_preview_link') + ")"

            probables  = " |Pitcher|TV|Radio|Preview\n"
            probables += "-|-|-|-|-\n"
            probables += "[" + game.get('away_team_name') + "](" + subs[1] + ")|" + away_pitcher + "|" + away_tv_broadcast + "|" + away_radio_broadcast + "|" + away_preview + "\n"
            probables += "[" + game.get('home_team_name') + "](" + subs[0] + ")|" + home_pitcher + "|" + home_tv_broadcast + "|" + home_radio_broadcast + "|" + home_preview + "\n"

            probables += "\n"
            
            return probables
        except:
            print "Missing data for probables, returning empty string..."
            return probables

    def generate_pre_first_pitch(self,files):
        first_pitch = ""
        try:
            game = files["linescore"].get('data').get('game')

            timestring = game.get('time_date') + " " + game.get('ampm')
            date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
            t = timedelta(hours=self.time_change)
            timezone = self.time_zone
            date_object = date_object - t
            first_pitch = "**First Pitch:** " + date_object.strftime("%I:%M %p ") + timezone + "\n\n"

            return first_pitch
        except:
            print "Missing data for first_pitch, returning empty string..."
            return first_pitch


    def generate_code(self,dir,thread):
        code = ""
        dirs = []
        dirs.append(dir + "linescore.json")
        dirs.append(dir + "boxscore.json")
        dirs.append(dir + "gamecenter.xml")
        dirs.append(dir + "plays.json")
        dirs.append(dir + "/inning/inning_Scores.xml")
        dirs.append(dir + "/media/mobile.xml")
        files = self.download_files(dirs)
        if thread == "game":
            if self.header: code = code + self.generate_header(files)
            if self.box_score: code = code + self.generate_boxscore(files)
            if self.line_score: code = code + self.generate_linescore(files)
            if self.scoring_plays: code = code + self.generate_scoring_plays(files)
            if self.highlights: code = code + self.generate_highlights(files)
            if self.footer: code = code + self.footer + "\n\n"
        elif thread == "post":
            if self.post_header: code = code + self.generate_header(files)
            if self.post_box_score: code = code + self.generate_boxscore(files)
            if self.post_line_score: code = code + self.generate_linescore(files)
            if self.post_scoring_plays: code = code + self.generate_scoring_plays(files)
            if self.post_highlights: code = code + self.generate_highlights(files)
            if self.post_footer: code = code + self.post_footer + "\n\n"
        code = code + self.generate_status(files)
        print "Returning all code..."
        return code


    def download_files(self,dirs):
        files = dict()
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
        except Exception as e:
            print e

        return files


    def generate_header(self,files):
        header = ""
        try:
            game = files["linescore"].get('data').get('game')
            timestring = game.get('time_date') + " " + game.get('ampm')
            date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
            t = timedelta(hours=self.time_change)
            timezone = self.time_zone
            date_object = date_object - t
            header = "**First Pitch:** " + date_object.strftime("%I:%M %p ") + timezone + "\n\n"
            header = header + "[Preview](http://mlb.mlb.com/mlb/gameday/index.jsp?gid=" + game.get('gameday_link') + ")\n\n"
            weather = files["plays"].get('data').get('game').get('weather')
            root = files["gamecenter"].getroot()
            broadcast = root.find('broadcast')
            notes = self.get_notes(game.get('home_team_name'), game.get('away_team_name'))
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
        except:
            print "Missing data for header, returning empty string..."
            return header


    def generate_boxscore(self,files):
        boxscore = ""
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
        except:
            print "Missing data for boxscore, returning blank text..."
            return boxscore


    def generate_linescore(self,files):
        linescore = ""
        try:
            game = files["linescore"].get('data').get('game')
            subreddits = self.get_subreddits(game.get('home_team_name'), game.get('away_team_name'))
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
        except:
            print "Missing data for linescore, returning blank text..."
            return linescore


    def generate_scoring_plays(self,files):
        scoringplays = ""
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
                    scoringplays = scoringplays + s.get("away") + "-" + s.get("home") + " " + root.get("away_team").upper()
                elif int(s.get("home")) > int(s.get("away")):
                    scoringplays = scoringplays + s.get("home") + "-" + s.get("away") + " " + root.get("home_team").upper()
                else:
                    scoringplays = scoringplays + s.get("home") + "-" + s.get("away")
                scoringplays = scoringplays + "\n"
            scoringplays = scoringplays + "\n\n"
            print "Returning scoringplays..."
            return scoringplays
        except:
            print "Missing data for scoringplays, returning blank text..."
            return scoringplays


    def generate_highlights(self,files):
        highlight = ""
        try:
            root = files["highlights"].getroot()
            video = root.findall("media")
            highlight = highlight + "|Team|Highlight|\n"
            highlight = highlight + "|:--|:--|\n"
            for v in video:
                if v.get('type') == "video" and v.get('media-type') == "T":              
                    try:
                        team = self.get_team(v.get('team_id'))
                        highlight = highlight + "|" + team[0] + "|[" + v.find("headline").text + "](" + v.find("url").text + ")|\n"                   
                    except:
                        highlight = highlight + "|[](/MLB)|[" + v.find("headline").text + "](" + v.find("url").text + ")|\n"                     
            highlight = highlight + "\n\n"
            print "Returning highlight..."
            return highlight
        except:
            print "Missing data for highlight, returning blank text..."
            return highlight


    def generate_decisions(self,files):
        decisions = ""
        try:
            homepitchers = []
            awaypitchers = []
            game = files["boxscore"].get('data').get('boxscore')
            team = files["linescore"].get('data').get('game')
            subreddits = self.get_subreddits(team.get('home_team_name'), team.get('away_team_name'))
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
        except:
            print "Missing data for decisions, returning blank text..."
            return decisions


    def generate_status(self,files):
        status = ""
        try:
            game = files["linescore"].get('data').get('game')
            if game.get('status') == "Game Over" or game.get('status') == "Final":
                s = files["linescore"].get('data').get('game')
                status = status + "##FINAL: "
                if int(s.get("home_team_runs")) < int(s.get("away_team_runs")):
                    status = status + s.get("away_team_runs") + "-" + s.get("home_team_runs") + " " + s.get(
                        "away_team_name") + "\n"
                    status = status + self.generate_decisions(files)
                    print "Returning status..."
                    return status
                elif int(s.get("home_team_runs")) > int(s.get("away_team_runs")):
                    status = status + s.get("home_team_runs") + "-" + s.get("away_team_runs") + " " + s.get(
                        "home_team_name") + "\n"
                    status = status + self.generate_decisions(files)
                    print "Returning status..."
                    return status
                elif int(s.get("home_team_runs")) == int(s.get("away_team_runs")):
                    status = status + "TIE"
                    print "Returning status..."
                    return status
            elif game.get('status') == "Completed Early":
                status = status + "##COMPLETED EARLY: "
                if int(s.get("home_team_runs")) < int(s.get("away_team_runs")):
                    status = status + s.get("away_team_runs") + "-" + s.get("home_team_runs") + " " + s.get(
                        "away_team_name") + "\n"
                    status = status + self.generate_decisions(files)
                    print "Returning status..."
                    return status
                elif int(s.get("home_team_runs")) > int(s.get("away_team_runs")):
                    status = status + s.get("home_team_runs") + "-" + s.get("away_team_runs") + " " + s.get(
                        "home_team_name") + "\n"
                    status = status + self.generate_decisions(files)
                    print "Returning status..."
                    return status
                elif int(s.get("home_team_runs")) == int(s.get("away_team_runs")):
                    status = status + "TIE"
                    print "Returning status..."
                    return status
            elif game.get('status') == "Postponed":
                status = status + "##POSTPONED\n\n"
                print "Returning status..."
                return status
            elif game.get('status') == "Suspended":
                status = status + "##SUSPENDED\n\n"
                print "Returning status..."
                return status
            elif game.get('status') == "Cancelled":
                status = status + "##CANCELLED\n\n"
                print "Returning status..."
                return status
            else:
                print "Status not final or postponed, returning blank text..."
                return status
        except:
            print "Missing data for status, returning blank text..."
            return status

    def get_subreddits(self, homename, awayname):
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


    def get_notes(self, homename, awayname):
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
        
        
    def get_team(self, team_id):
        team = []
        options = {
            "142": "[MIN](/r/minnesotatwins)",
            "145": "[CWS](/r/WhiteSox)",
            "116": "[DET](/r/MotorCityKitties)",
            "118": "[KCR](/r/KCRoyals)",
            "114": "[CLE](/r/WahoosTipi)",
            "140": "[TEX](/r/TexasRangers)",
            "117": "[HOU](/r/Astros)",
            "133": "[OAK](/r/OaklandAthletics)",
            "108": "[LAA](/r/AngelsBaseball)",
            "136": "[SEA](/r/Mariners)",
            "111": "[BOS](/r/RedSox)",
            "147": "[NYY](/r/NYYankees)",
            "141": "[TOR](/r/TorontoBlueJays)",
            "139": "[TBR](/r/TampaBayRays)",
            "110": "[BAL](/r/Orioles)",
            "138": "[STL](/r/Cardinals)",
            "113": "[CIN](/r/Reds)",
            "134": "[PIT](/r/Buccos)",
            "112": "[CHC](/r/CHICubs)",
            "158": "[MIL](/r/Brewers)",
            "137": "[SFG](/r/SFGiants)",
            "109": "[ARI](/r/azdiamondbacks)",
            "115": "[COL](/r/ColoradoRockies)",
            "119": "[LAD](/r/Dodgers)",
            "135": "[SDP](/r/Padres)",
            "143": "[PHI](/r/Phillies)",
            "121": "[NYM](/r/NewYorkMets)",
            "146": "[MIA](/r/letsgofish)",
            "120": "[WSH](/r/Nationals)",
            "144": "[ATL](/r/Braves)"
        }
        team.append(options[team_id])
        return team        
