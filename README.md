Baseball GDT Bot v2.0 by Matt Bullock
=====================================

This project was originally written by Matt Bullock,
	A.K.A. /u/DetectiveWoofles on reddit and Woofles on GitHub.
	
The point of this project is to create a bot that will generate a
	game discussion thread that contains live linescore and boxscore,
	post it in the correct subreddit for that team, and keep it
	updated throughout the game.
	
Version 1.0 was written in a mix of Python and Java, and it is being
	completely ported to Python for v2.0 (this version).
	
Modules being used:

	praw - interfacing reddit
	
	simplejson - JSON parsing
	
	urllib2 - pulling data from MLB servers
	
	ElementTree - XML parsing
