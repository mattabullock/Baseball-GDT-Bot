import player, editor
from datetime import datetime
import timecheck
import time

import praw
import urllib2
import simplejson as json
	
r = praw.Reddit(user_agent='Game Discission Thread Generator Bot by /u/DetectiveWoofles') 
r.login('*****', '*****')

while True:
	
	# getting dirc
	today = datetime.today()
	url = "http://gd2.mlb.com/components/game/mlb/"
	url = url + "year_" + today.strftime("%Y") + "/month_" + today.strftime("%m") + "/day_" + today.strftime("%d") + "/"
	
	# UNCOMMENT FOR TESTING PURPOSES ONLY
	# url = url + "year_" + today.strftime("%Y") + "/month_" + today.strftime("%m") + "/day_11/"

	response = ""
	while not response:
		try:
			response = urllib2.urlopen(url)
		except:
			print "Couldn't find file, trying again..."
			time.sleep(20)

	html = response.readlines()
	directories = []
	for v in html:
		if "minmlb" in v:
			v = v[v.index("\"")+1:len(v)]
			v = v[0:v.index("\"")]
			directories.append(url + v)
			
	for d in directories:
		timecheck.gamecheck(d)
		title = editor.generatetitle(d)
		if not timecheck.ppcheck(d):
			while True:
				try:
					sub = r.submit('test', title, editor.generatecode(d))
					break
				except Exception, err:
					print err
					time.sleep(300)
			while True:
				str = editor.generatecode(d)
				while True:
					try:
						sub.edit(str)
						break
					except Exception, err:
						print "Couldn't submit edits, trying again..."
						time.sleep(10)
				if "###FINAL" in str:
					break
				elif "###POSTPONED" in str:
					break
				time.sleep(10)
	if datetime.today().day == today.day:
		timecheck.endofdaycheck()