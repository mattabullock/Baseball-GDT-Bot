import player, editor
from datetime import datetime

import praw
import urllib2
import simplejson as json

r = praw.Reddit(user_agent='Game Discission Thread Generator Bot by /u/DetectiveWoofles') 
r.login('*****', '*****')	

# getting dirc
d = datetime.today()
url = "http://gd2.mlb.com/components/game/mlb/"
url = url + "year_" + d.strftime("%Y") + "/month_" + d.strftime("%m") + "/day_" + d.strftime("%d") + "/"
# url = url + "year_" + d.strftime("%Y") + "/month_" + d.strftime("%m") + "/day_11/"

reponse = urllib2.urlopen(url)
html = reponse.readlines()
directories = []
# print html
for v in html:
	if "minmlb" in v:
		v = v[v.index("\"")+1:len(v)]
		v = v[0:v.index("\"")]
		directories.append(url + v)
# for v in directories:
	# generatecode(v)
# r.submit('test', 'test', editor.generatecode(directories[0]))
sub = r.get_submission(submission_id='1gmia3')
sub.edit(editor.generatecode(directories[0]))