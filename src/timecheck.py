# does all the time checking

import urllib2
import time
from datetime import datetime
import simplejson as json

class TimeCheck:

    def __init__(self,time_before):
        self.time_before = time_before

    def endofdaycheck(self):
        today = datetime.today()
        while True:
            check = datetime.today()
            if today.day != check.day:
                print datetime.strftime(check, "%d %I:%M %p")
                print "NEW DAY"
                return
            else:
                print "Last time check: " + datetime.strftime(check, "%d %I:%M %p")
                time.sleep(600)


    def gamecheck(self,dir):
        while True:
            try:
                response = urllib2.urlopen(dir + "linescore.json")
                break
            except:
                check = datetime.today()
                print datetime.strftime(check, "%d %I:%M %p")
                print "gamecheck couldn't find file, trying again..."
                time.sleep(20)
        jsonfile = json.load(response)
        game = jsonfile.get('data').get('game')
        timestring = game.get('time_date') + " " + game.get('ampm')
        date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
        while True:
            check = datetime.today()
            if date_object >= check:
                if (date_object - check).seconds <= self.time_before:
                    return
                else:
                    print "Last game check: " + datetime.strftime(check, "%d %I:%M %p")
                    time.sleep(600)
            else:
                return

    def ppcheck(self,dir):
        try:
            response = urllib2.urlopen(dir + "linescore.json")
        except:
            check = datetime.today()
            print datetime.strftime(check, "%d %I:%M %p")
            print "ppcheck Couldn't find file, trying again..."
            time.sleep(20)
        jsonfile = json.load(response)
        game = jsonfile.get('data').get('game')
        return (game.get('status') == "Postponed")

    def pregamecheck(self,pre_time):
        date_object = datetime.strptime(pre_time, "%I%p")
        while True:
            check = datetime.today()
            if date_object.hour <= check.hour:
                return
            else:
                print "Last pre-game check: " + datetime.strftime(check, "%d %I:%M %p")
                time.sleep(600)
