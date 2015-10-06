import editor
from datetime import datetime
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
        self.PREGAME_THREAD = None
        self.POST_GAME_THREAD = None
        self.STICKY = None
        self.SUGGESTED_SORT = None
        self.MESSAGE = None
        self.PRE_THREAD_SETTINGS = None
        self.THREAD_SETTINGS = None
        self.POST_THREAD_SETTINGS = None

    def read_settings(self):
        with open('settings.json') as data:
            settings = json.load(data)

            self.CLIENT_ID = settings.get('CLIENT_ID')
            if self.CLIENT_ID == None: return "Missing CLIENT_ID"

            self.CLIENT_SECRET = settings.get('CLIENT_SECRET')
            if self.CLIENT_SECRET == None: return "Missing CLIENT_SECRET"

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

        r = praw.Reddit('OAuth Baseball-GDT-Bot V. 3.0.0'
                        'https://github.com/mattabullock/Baseball-GDT-Bot')
        r.set_oauth_app_info(client_id=self.CLIENT_ID,
                            client_secret=self.CLIENT_SECRET,
                            redirect_uri=self.REDIRECT_URI)        
        r.refresh_access_information(self.REFRESH_TOKEN)   

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
                title = edit.generatetitle(d)
                while True:
                    check = datetime.today()
                    try:
                        print "Submitting game thread..."
                        sub = r.submit(self.SUBREDDIT, title, edit.generatecode(d))
                        if self.STICKY: sub.sticky()
                        print "Game thread submitted..."
                        print datetime.strftime(check, "%d %I:%M %p")
                        time.sleep(5)
                        break
                    except Exception, err:
                        print err
                        time.sleep(300)
                pgt_submit = False
                while True:
                    str = edit.generatecode(d)
                    if "|Decisions|" in str:
                        check = datetime.today()
                        print datetime.strftime(check, "%d %I:%M %p")
                        print "Game final..."
                        pgt_submit = True
                    elif "##COMPLETED EARLY" in str:
                        check = datetime.today()
                        print datetime.strftime(check, "%d %I:%M %p")
                        print "Completed Early..."
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
                            if self.STICKY: sub.sticky()
                            print "Postgame thread submitted..."
                        break
            break

if __name__ == '__main__':
    program = Bot()
    program.run()
