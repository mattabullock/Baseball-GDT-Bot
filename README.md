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
	
