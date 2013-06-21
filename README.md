Baseball GDT Bot by Matt Bullock
=====================================

####Current Version: 2.0.2

This project was originally written by Matt Bullock,
	A.K.A. /u/DetectiveWoofles on reddit and Woofles on GitHub.
	
The point of this project is to create a bot that will generate a
	game discussion thread that contains live linescore and boxscore,
	post it in the correct subreddit for that team, and keep it
	updated throughout the game.
	
Version 1.0 was written in a mix of Python and Java, and has been
	completely ported to Python for v2.0 (this version).

---

####SET UP YOUR OWN BOT!

To set up a bot for your own sub, there are a few spots in the code you 
	need to change things. 
	
First is line 34 of main.py, change it to be your team's code. Search through [this page](http://gd2.mlb.com/components/game/mlb/year_2013/month_06/day_19/) and you can probably find it. 
	
Second place to change is line 91 of editor.py.
	You need to change the number to match your time zone, so 0 is ET,
	1 is CT, 2 is MT, and 3 is PT. Right under that is the third place
	to change, and you just need to change what time zone it displays.
	Next you'll need to go back to main.py and change the first parameter
	in line 45 to the sub you want to post to (just the name, like 
	minnesotatwins, not /r/minnesotatwins). 
	
Next, make sure you type in your login credentials to line 11 of main.py.

Lastly, in timecheck.py, search for the number 5400 and change it to 9000 for MT,
	1800 for ET, and 12600 for PT. Keep it the same for CT.
	
---	

If something doesn't seem right, feel free to message me or post it as a bug here.
	
This was written in Python 2.7, so beware if you are running Python 3 or
	above that it may not work correctly. Also make sure you install
	praw and simplejson before running!
	
Modules being used:

	praw - interfacing reddit
	simplejson - JSON parsing
	urllib2 - pulling data from MLB servers
	ElementTree - XML parsing

###Updates

####v2.0.2

* Fixed random crashing
* Fixed bug where some teams names were not displayed correctly. (Though Chi White Sox White Sox is a great name...)

####v2.0.1

* Fixed gamecheck not always working correctly.
* Fixed the TV media showing the same for both home and away.
* Fixed the timestamp on the game/time checks not displaying correctly.
	
