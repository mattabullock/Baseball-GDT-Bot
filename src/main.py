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
        self.BOT_TIME_ZONE = None
        self.TEAM_TIME_ZONE = None
        self.POST_TIME = None
        self.USERNAME = None
        self.PASSWORD = None
        self.SUBREDDIT = None
        self.TEAM_CODE = None
        self.POST_GAME_THREAD = None
        self.STICKY = None
        self.MESSAGE = None
        self.POST_SETTINGS = None

    def read_settings(self):
        with open('settings.json') as data:
            settings = json.load(data)

            self.BOT_TIME_ZONE = settings.get('BOT_TIME_ZONE')
            if self.BOT_TIME_ZONE == None: return "Missing BOT_TIME_ZONE"

            self.TEAM_TIME_ZONE = settings.get('TEAM_TIME_ZONE')
            if self.TEAM_TIME_ZONE == None: return "Missing TEAM_TIME_ZONE"

            self.POST_TIME = settings.get('POST_TIME')
            if self.POST_TIME == None: return "Missing POST_TIME"

            self.USERNAME = settings.get('USERNAME')
            if self.USERNAME == None: return "Missing USERNAME"

            self.PASSWORD = settings.get('PASSWORD')
            if self.PASSWORD == None: return "Missing PASSWORD"

            self.SUBREDDIT = settings.get('SUBREDDIT')
            if self.SUBREDDIT == None: return "Missing SUBREDDIT"

            self.TEAM_CODE = settings.get('TEAM_CODE')
            if self.TEAM_CODE == None: return "Missing TEAM_CODE"

            self.POST_GAME_THREAD = settings.get('POST_GAME_THREAD')
            if self.POST_GAME_THREAD == None: return "Missing POST_GAME_THREAD"

            self.STICKY = settings.get('STICKY')
            if self.STICKY == None: return "Missing STICKY"
            
            self.MESSAGE = settings.get('MESSAGE')
            if self.MESSAGE == None: return "Missing MESSAGE"

            temp_settings = settings.get('POST_SETTINGS')
            self.POST_SETTINGS = (temp_settings.get('HEADER'),temp_settings.get('BOX_SCORE'),
                                    temp_settings.get('LINE_SCORE'),temp_settings.get('SCORING_PLAYS'),
                                    temp_settings.get('HIGHLIGHTS'))
            if self.POST_SETTINGS == None: return "Missing POST_SETTINGS"

        return 0

    def run(self):

        error_msg = self.read_settings()

        if error_msg != 0:
            print error_msg
            return

        r = praw.Reddit(user_agent='Baseball-GDT')
        r.login(self.USERNAME, self.PASSWORD)

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

        edit = editor.Editor(time_info, self.POST_SETTINGS)

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

            # getting dirc
            url = "http://gd2.mlb.com/components/game/mlb/"
            url = url + "year_" + today.strftime("%Y") + "/month_" + today.strftime("%m") + "/day_" + today.strftime("%d") + "/"

            # UNCOMMENT FOR TESTING PURPOSES ONLY
            # url = url + "year_2015" + "/month_04" + "/day_03/"

            response = ""
            while not response:
                try:
                    response = urllib2.urlopen(url)
                except:
                    print "Couldn't find URL, trying again..."
                    time.sleep(20)

            html = response.readlines()
            directories = []
            for v in html:
                if self.TEAM_CODE in v:
                    v = v[v.index("\"") + 1:len(v)]
                    v = v[0:v.index("\"")]
                    directories.append(url + v)

            for d in directories:
                timechecker.gamecheck(d)
                title = edit.generatetitle(d)
                if not timechecker.ppcheck(d):
                    while True:
                        check = datetime.today()
                        try:
                            print "Submitting game thread..."
                            sub = r.submit(self.SUBREDDIT, title, edit.generatecode(d))
                            print "Game thread submitted..."
                            if self.STICKY:
                                print "Stickying submission..." 
                                sub.sticky()
                                print "Submission stickied..."
                            if self.MESSAGE:
                                print "Messaging Baseballbot..."
                                r.send_message('baseballbot', 'Gamethread posted', sub.short_link)
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
                        str = edit.generatecode(d)
                        while True:
                            try:
                                sub.edit(str)
                                print "Edits submitted..."
                                print "Sleeping for two minutes..."
                                print datetime.strftime(check, "%d %I:%M %p")
                                time.sleep(120)
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
                        elif "##FINAL: TIE" in str:
                            check = datetime.today()
                            print datetime.strftime(check, "%d %I:%M %p")
                            print "Game final (tie)..."
                            pgt_submit = True
                        elif "##POSTPONED" in str:
                            check = datetime.today()
                            print datetime.strftime(check, "%d %I:%M %p")
                            print "Game postponed..."
                            pgt_submit = True
                        elif "##SUSPENDED" in str:
                            check = datetime.today()
                            print datetime.strftime(check, "%d %I:%M %p")
                            print "Game suspended..."
                            pgt_submit = True
                        elif "##CANCELLED" in str:
                            check = datetime.today()
                            print datetime.strftime(check, "%d %I:%M %p")
                            print "Game cancelled..."
                            pgt_submit = True
                        if pgt_submit:
                            if self.POST_GAME_THREAD:
                                print "Submitting postgame thread..."
                                posttitle = edit.generateposttitle(d)
                                sub = r.submit(self.SUBREDDIT, posttitle, edit.generatecode(d))
                                print "Postgame thread submitted..."
                                if self.STICKY:
                                    print "Stickying submission..." 
                                    sub.sticky()
                                    print "Submission stickied..."
                            break
                        time.sleep(10)
            if datetime.today().day == today.day:
                timechecker.endofdaycheck()

if __name__ == '__main__':
    program = Bot()
    program.run()
