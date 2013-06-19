# does all the time checking

import urllib2
import time
from datetime import datetime
import simplejson as json

def endofdaycheck():
	today = datetime.today()
	while True:
		check = datetime.today()
		if today.day != check.day:
			print "NEW DAY"
			return
		else:
			print "Last time check: " + datetime.strftime(check, "%I:%M %p") 
			time.sleep(600)
			
def gamecheck(dir):
	while True:
		try:
			response = urllib2.urlopen(dir + "linescore.json")
			break
		except:
			print "Couldn't find file, trying again..."
			time.sleep(20)
	jsonfile = json.load(response)
	game = jsonfile.get('data').get('game')
	timestring = game.get('time_date') + " " + game.get('ampm')
	date_object = datetime.strptime(timestring, "%Y/%m/%d %I:%M %p")
	while True:
		check = datetime.today()
		if (date_object - check).seconds <= 5400:
			return
		else:
			print "Last game check: " + datetime.strftime(check, "%I:%M %p")
			time.sleep(600)
			
def ppcheck(dir):
	try:
		response = urllib2.urlopen(dir + "linescore.json")
	except:
		print "Couldn't find file, trying again..."
		time.sleep(20)
	jsonfile = json.load(response)
	game = jsonfile.get('data').get('game')
	return (game.get('status') == "Postponed")