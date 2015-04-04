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

import praw
import urllib2

###################################################################################################

'''
THIS INFORMATION CAN BE EDITED. DON'T CHANGE ANYTHING ELSE PLEASE AND THANK YOU.

BOT_TIME_ZONE - time zone of the computer running the bot, uncomment the line that you want to use
TIME_ZONE - time zone of the team. uncomment the line that you want to use
POST_TIME - bot posts the thread POST_TIME hours before the game
USERNAME - reddit username
PASSWORD - reddit password
SUBREDDIT - subreddit that you want the threads posted to
TEAM_CODE - three letter code that represents team, look this up
POST_GAME_THREAD - do you want a post game thread?
STICKY - do you want the thread stickied?
'''

# BOT_TIME_ZONE = 'ET' # Eastern time
BOT_TIME_ZONE = 'CT' # Central time
# BOT_TIME_ZONE = 'MT' # Mountain time
# BOT_TIME_ZONE = 'PT' # Pacific time

# TIME_ZONE = 'ET' # Eastern time
TIME_ZONE = 'CT' # Central time
# TIME_ZONE = 'MT' # Mountain time
# TIME_ZONE = 'PT' # Pacific time

POST_TIME = 1 # Hours before the game that the thread will be posted

USERNAME = 'XXX'
PASSWORD = 'XXX'
SUBREDDIT = 'XXX'
TEAM_CODE = 'XXX'

POST_GAME_THREAD = False
STICKY = False

###################################################################################################

# DO NOT EDIT THIS CODE

def main():

    r = praw.Reddit(user_agent='GDTBot')
    r.login(USERNAME, PASSWORD)

    if TIME_ZONE == 'ET':
        time_info = (TIME_ZONE,0)
    elif TIME_ZONE == 'CT':
        time_info = (TIME_ZONE,1)
    elif TIME_ZONE == 'MT':
        time_info = (TIME_ZONE,2)
    elif TIME_ZONE == 'PT':
        time_info = (TIME_ZONE,3)
    else:
        print "Invalid time zone settings."
        break

    edit = editor.Editor(time_info)

    if BOT_TIME_ZONE == 'ET':
        time_before = POST_TIME * 60 * 60
    elif BOT_TIME_ZONE == 'CT':
        time_before = (1 + POST_TIME) * 60 * 60
    elif BOT_TIME_ZONE == 'MT':
        time_before = (2 + POST_TIME) * 60 * 60
    elif BOT_TIME_ZONE == 'PT':
        time_before = (3 + POST_TIME) * 60 * 60
    else:
        print "Invalid bot time zone settings."
        break

    timechecker = timecheck.TimeCheck(time_before)

    while True:
        today = datetime.today()

        # getting dirc
        url = "http://gd2.mlb.com/components/game/mlb/"
        url = url + "year_" + today.strftime("%Y") + "/month_" + today.strftime("%m") + "/day_" + today.strftime("%d") + "/"

        # UNCOMMENT FOR TESTING PURPOSES ONLY
        #url = url + "year_2014" + "/month_03" + "/day_31/"

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
            if TEAM_CODE in v:
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
                        sub = r.submit(SUBREDDIT, title, edit.generatecode(d))
                        if STICKY: sub.sticky()
                        print "Game thread submitted..."
                        print "Sleeping for two minutes..."
                        print datetime.strftime(check, "%d %I:%M %p")
                        time.sleep(120)
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
                        if POST_GAME_THREAD:
                            print "Submitting postgame thread..."
                            posttitle = edit.generateposttitle(d)
                            sub = r.submit(SUBREDDIT, posttitle, edit.generatecode(d))
                            print "Postgame thread submitted..."
                        break
                    time.sleep(10)
        if datetime.today().day == today.day:
            timechecker.endofdaycheck()

if __name__ == '__main__':
    main()