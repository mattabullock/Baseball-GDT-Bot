#!/usr/bin/env python

'''

BASEBALL GAME THREAD BOT

Written by:
/u/DetectiveWoofles
/u/avery_crudeman

Please contact us on Reddit or Github if you have any questions.

'''

import editor
from datetime import datetime
import timecheck
import time
import simplejson as json
import praw
import urllib2

class Bot:

    def __init__(self):
        return

    def read_settings(self):
        import os
        cwd = os.path.dirname(os.path.realpath(__file__))
        with open(cwd + '/settings.json') as data:
            settings = json.load(data)

            self.CLIENT_ID = settings.get('CLIENT_ID')
            if self.CLIENT_ID == None: return "Missing CLIENT_ID"

            self.CLIENT_SECRET = settings.get('CLIENT_SECRET')
            if self.CLIENT_SECRET == None: return "Missing CLIENT_SECRET"

            self.USER_AGENT = settings.get('USER_AGENT')
            if self.USER_AGENT == None: return "Missing USER_AGENT"

            self.REDIRECT_URI = settings.get('REDIRECT_URI')
            if self.REDIRECT_URI == None: return "Missing REDIRECT_URI"

            self.REFRESH_TOKEN = settings.get('REFRESH_TOKEN')
            if self.REFRESH_TOKEN == None: return "Missing REFRESH_TOKEN"

            self.BOT_TIME_ZONE = settings.get('BOT_TIME_ZONE')
            if self.BOT_TIME_ZONE == None: return "Missing BOT_TIME_ZONE"

            self.TEAM_TIME_ZONE = settings.get('TEAM_TIME_ZONE')
            if self.TEAM_TIME_ZONE == None: return "Missing TEAM_TIME_ZONE"

            self.POST_TIME = settings.get('POST_TIME')
            if self.POST_TIME == None: return "Missing POST_TIME"

            self.SUBREDDIT = settings.get('SUBREDDIT')
            if self.SUBREDDIT == None: return "Missing SUBREDDIT"

            self.TEAM_CODE = settings.get('TEAM_CODE')
            if self.TEAM_CODE == None: return "Missing TEAM_CODE"

            self.OFFDAY_THREAD = settings.get('OFFDAY_THREAD')
            if self.OFFDAY_THREAD == None: return "Missing OFFDAY_THREAD"

            self.PREGAME_THREAD = settings.get('PREGAME_THREAD')
            if self.PREGAME_THREAD == None: return "Missing PREGAME_THREAD"

            self.POST_GAME_THREAD = settings.get('POST_GAME_THREAD')
            if self.POST_GAME_THREAD == None: return "Missing POST_GAME_THREAD"

            self.STICKY = settings.get('STICKY')
            if self.STICKY == None: return "Missing STICKY"

            self.SUGGESTED_SORT = settings.get('SUGGESTED_SORT')
            if self.SUGGESTED_SORT == None: return "Missing SUGGESTED_SORT"

            self.MESSAGE = settings.get('MESSAGE')
            if self.MESSAGE == None: return "Missing MESSAGE"

            self.INBOXREPLIES = settings.get('INBOXREPLIES')
            if self.INBOXREPLIES == None: return "Missing INBOXREPLIES"

            temp_settings = settings.get('OFFDAY_THREAD_SETTINGS')
            self.OFFDAY_THREAD_SETTINGS = (temp_settings.get('OFFDAY_THREAD_TAG'),temp_settings.get('OFFDAY_THREAD_TIME'))

            temp_settings = settings.get('PRE_THREAD_SETTINGS')
            content_settings = temp_settings.get('CONTENT')
            self.PRE_THREAD_SETTINGS = (temp_settings.get('PRE_THREAD_TAG'),temp_settings.get('PRE_THREAD_TIME'),
                                            (content_settings.get('PROBABLES'),content_settings.get('FIRST_PITCH'))
                                       )
            if self.PRE_THREAD_SETTINGS == None: return "Missing PRE_THREAD_SETTINGS"

            temp_settings = settings.get('THREAD_SETTINGS')
            content_settings = temp_settings.get('CONTENT')
            self.THREAD_SETTINGS = (temp_settings.get('THREAD_TAG'),
                                    (content_settings.get('HEADER'), content_settings.get('BOX_SCORE'),
                                     content_settings.get('LINE_SCORE'), content_settings.get('SCORING_PLAYS'),
                                     content_settings.get('HIGHLIGHTS'), content_settings.get('FOOTER'))
                                 )
            if self.THREAD_SETTINGS == None: return "Missing THREAD_SETTINGS"

            temp_settings = settings.get('POST_THREAD_SETTINGS')
            content_settings = temp_settings.get('CONTENT')
            self.POST_THREAD_SETTINGS = (temp_settings.get('POST_THREAD_TAG'),
                                    (content_settings.get('HEADER'), content_settings.get('BOX_SCORE'),
                                     content_settings.get('LINE_SCORE'), content_settings.get('SCORING_PLAYS'),
                                     content_settings.get('HIGHLIGHTS'), content_settings.get('FOOTER'))
                                 )
            if self.POST_THREAD_SETTINGS == None: return "Missing POST_THREAD_SETTINGS"

        return 0

    def run(self):

        error_msg = self.read_settings()

        if error_msg != 0:
            print error_msg
            return

        r = praw.Reddit(client_id=self.CLIENT_ID,
                            client_secret=self.CLIENT_SECRET,
                            refresh_token=self.REFRESH_TOKEN,
                            user_agent=self.USER_AGENT)

        if self.TEAM_TIME_ZONE == 'ET':
            time_info = (self.TEAM_TIME_ZONE,0)
        elif self.TEAM_TIME_ZONE == 'CT':
            time_info = (self.TEAM_TIME_ZONE,1)
        elif self.TEAM_TIME_ZONE == 'MT':
            time_info = (self.TEAM_TIME_ZONE,2)
        elif self.TEAM_TIME_ZONE == 'PT':
            time_info = (self.TEAM_TIME_ZONE,3)
        else:
            print "Invalid time zone settings."
            return

        edit = editor.Editor(time_info, self.PRE_THREAD_SETTINGS,
                self.THREAD_SETTINGS, self.POST_THREAD_SETTINGS)

        if self.BOT_TIME_ZONE == 'ET':
            time_before = self.POST_TIME * 60 * 60
        elif self.BOT_TIME_ZONE == 'CT':
            time_before = (1 + self.POST_TIME) * 60 * 60
        elif self.BOT_TIME_ZONE == 'MT':
            time_before = (2 + self.POST_TIME) * 60 * 60
        elif self.BOT_TIME_ZONE == 'PT':
            time_before = (3 + self.POST_TIME) * 60 * 60
        else:
            print "Invalid bot time zone settings."
            return

        timechecker = timecheck.TimeCheck(time_before)

        while True:
            today = datetime.today()

            # url = "http://gd2.mlb.com/components/game/mlb/"
            baseURL = "https://statsapi.mlb.com"
            url = baseURL + "/api/v1/schedule?language=en&sportId=1&date="
            url += today.strftime("%m/%d/%Y")

            response = ""
            while not response:
                try:
                    response = urllib2.urlopen(url)
                except:
                    print "Couldn't find URL, trying again..."
                    time.sleep(20)

            schedule = json.load(response)
            todayGames = schedule["dates"][0]["games"]

            teamGames = []
            for game in todayGames:
                if game["teams"]["away"]["team"]["id"] == int(self.TEAM_CODE) or game["teams"]["home"]["team"]["id"] == int(self.TEAM_CODE):
                    teamGames.append(baseURL + game["link"])

            if self.OFFDAY_THREAD and not teamGames:
                timechecker.pregamecheck(self.OFFDAY_THREAD_SETTINGS[1])
                title = self.OFFDAY_THREAD_SETTINGS[0] + datetime.today().strftime("%B %m, %Y")
                while True:
                    try:
                        posted = False
                        subreddit = r.subreddit(self.SUBREDDIT)
                        for submission in subreddit.new():
                            if submission.title == title:
                                print "Offday thread already posted, getting submission..."
                                posted = True
                                break
                        if not posted:
                            print "Submitting off day thread..."
                            if self.STICKY and 'sub' in locals():
                                try:
                                    sub.mod.sticky(state=False)
                                except Exception, err:
                                    print "Unsticky failed, continuing."
                            sub = subreddit.submit(title, selftext="", send_replies=self.INBOXREPLIES)
                            print "off day thread submitted..."
                            if self.STICKY:
                                print "Stickying submission..."
                                sub.mod.sticky()
                                print "Submission stickied..."
                            print "Sleeping for two minutes..."
                            print datetime.strftime(datetime.today(), "%d %I:%M %p")
                            time.sleep(5)
                        break
                    except Exception, err:
                        print err
                        time.sleep(300)

            if self.PREGAME_THREAD and len(teamGames) > 0:
                timechecker.pregamecheck(self.PRE_THREAD_SETTINGS[1])
                title = edit.generate_title(teamGames[0],"pre")
                while True:
                    try:
                        posted = False
                        subreddit = r.subreddit(self.SUBREDDIT)
                        for submission in subreddit.new():
                            if submission.title == title:
                                print "Pregame thread already posted, getting submission..."
                                submission.edit(edit.generate_pre_code(teamGames))
                                posted = True
                                break
                        if not posted:
                            print "Submitting pregame thread..."
                            if self.STICKY and 'sub' in locals():
                                try:
                                    sub.mod.sticky(state=False)
                                except Exception, err:
                                    print "Unsticky failed, continuing."
                            sub = subreddit.submit(title, selftext=edit.generate_pre_code(directories), send_replies=self.INBOXREPLIES)
                            print "Pregame thread submitted..."
                            if self.STICKY:
                                print "Stickying submission..."
                                sub.mod.sticky()
                                print "Submission stickied..."
                            print "Sleeping for two minutes..."
                            print datetime.strftime(datetime.today(), "%d %I:%M %p")
                            time.sleep(5)
                        break
                    except Exception, err:
                        print err
                        time.sleep(300)

            for game in teamGames:
                timechecker.gamecheck(game)
                title = edit.generate_title(game,"game")
                if not timechecker.ppcheck(game):
                    while True:
                        check = datetime.today()
                        try:
                            posted = False
                            subreddit = r.subreddit(self.SUBREDDIT)
                            for submission in subreddit.new():
                                if submission.title == title:
                                    print "Thread already posted, getting submission..."
                                    sub = submission
                                    posted = True
                                    break
                            if not posted:
                                if self.STICKY and 'sub' in locals():
                                    try:
                                        sub.mod.sticky(state=False)
                                    except Exception, err:
                                        print "Unsticky failed, continuing."

                                print "Submitting game thread..."
                                sub = subreddit.submit(title, selftext=edit.generate_code(game, "game"), send_replies=self.INBOXREPLIES)
                                print "Game thread submitted..."

                                if self.STICKY:
                                    print "Stickying submission..."
                                    sub.mod.sticky()
                                    print "Submission stickied..."

                                if self.SUGGESTED_SORT != "":
                                    print "Setting suggested sort to " + self.SUGGESTED_SORT + "..."
                                    sub.mod.suggested_sort(self.SUGGESTED_SORT)
                                    print "Suggested sort set..."

                                if self.MESSAGE:
                                    print "Messaging Baseballbot..."
                                    r.redditor('baseballbot').message('Gamethread posted', sub.shortlink)
                                    print "Baseballbot messaged..."

                            print "Sleeping for two minutes..."
                            print datetime.strftime(check, "%d %I:%M %p")
                            time.sleep(5)
                            break
                        except Exception, err:
                            print err
                            time.sleep(300)

                    pgt_submit = False

                    while True:
                        check = datetime.today()
                        str = edit.generate_code(game, "game")
                        while True:
                            try:
                                sub.edit(str)
                                print "Edits submitted..."
                                break
                            except Exception, err:
                                print "Couldn't submit edits, trying again..."
                                print datetime.strftime(check, "%d %I:%M %p")
                                time.sleep(10)

                        if "|Decisions|" in str:
                            check = datetime.today()
                            print datetime.strftime(check, "%d %I:%M %p")
                            print "Game final..."
                            pgt_submit = True
                        elif "## COMPLETED EARLY" in str:
                            check = datetime.today()
                            print datetime.strftime(check, "%d %I:%M %p")
                            print "Completed Early..."
                            pgt_submit = True
                        elif "## FINAL: TIE" in str:
                            check = datetime.today()
                            print datetime.strftime(check, "%d %I:%M %p")
                            print "Game final (tie)..."
                            pgt_submit = True
                        elif "## POSTPONED" in str:
                            check = datetime.today()
                            print datetime.strftime(check, "%d %I:%M %p")
                            print "Game postponed..."
                            pgt_submit = True
                        elif "## SUSPENDED" in str:
                            check = datetime.today()
                            print datetime.strftime(check, "%d %I:%M %p")
                            print "Game suspended..."
                            pgt_submit = True
                        elif "## CANCELLED" in str:
                            check = datetime.today()
                            print datetime.strftime(check, "%d %I:%M %p")
                            print "Game cancelled..."
                            pgt_submit = True
                        if pgt_submit:
                            if self.STICKY and 'sub' in locals():
                                try:
                                    sub.mod.sticky(state=False)
                                except Exception, err:
                                    print "Unsticky failed, continuing."

                            if self.POST_GAME_THREAD:
                                print "Submitting postgame thread..."
                                posttitle = edit.generate_title(game, "post")
                                sub = subreddit.submit(posttitle, selftext=edit.generate_code(game, "post"), send_replies=self.INBOXREPLIES)
                                print "Postgame thread submitted..."

                                if self.STICKY:
                                    print "Stickying submission..."
                                    sub.mod.sticky()
                                    print "Submission stickied..."
                            time.sleep(10)
                            break
                        else:
                            print "Sleeping for one minute..."
                            print datetime.strftime(check, "%d %I:%M %p")
                            time.sleep(60)
            if datetime.today().day == today.day:
                timechecker.endofdaycheck()

if __name__ == '__main__':
    program = Bot()
    program.run()
