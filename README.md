Baseball GDT Bot by Matt Bullock
=====================================

####Current Version: 3.0.0

This project was originally written by Matt Bullock,
	A.K.A. /u/DetectiveWoofles on reddit and Woofles on GitHub.
	User avery-crudeman is the only other contributor.
	
The point of this project is to create a bot that will generate a
	game discussion thread that contains live linescore and boxscore,
	post it in the correct subreddit for that team, and keep it
	updated throughout the game.
	
Version 1.0 was written in a mix of Python and Java, and has been
	completely ported to Python for v2.0 and v3.0 (this version).

---

####SET UP YOUR OWN BOT!

All you need to do is edit sample_settings.json with the following information, rename it to settings.json, and copy it into the src folder!

BOT_TIME_ZONE - time zone of the computer running the bot, uncomment the line that you want to use
TIME_ZONE - time zone of the team. uncomment the line that you want to use
POST_TIME - bot posts the thread POST_TIME hours before the game
USERNAME - reddit username
PASSWORD - reddit password
SUBREDDIT - subreddit that you want the threads posted to
TEAM_CODE - three letter code that represents team, look this up
POST_GAME_THREAD - do you want a post game thread?
STICKY - do you want the thread stickied?
	
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

####v3.0.0
* Modular - If you want a certain feature, just change a variable at the top!
* Easier to read - Cleaned up some code, started using more OOP.

####v2.0.4
* Fixed crash caused by game not being aired on TV.
* Fixed another crash related to scoring plays.

####v2.0.3
* Fixed the Diamondbacks' subreddit not working properly.
* Fixed crash related to scoring plays.

####v2.0.2

* Fixed random crashing.
* Fixed bug where some teams names were not displayed correctly. (Though Chi White Sox White Sox is a great name...)

####v2.0.1

* Fixed gamecheck not always working correctly.
* Fixed the TV media showing the same for both home and away.
* Fixed the timestamp on the game/time checks not displaying correctly.
	
