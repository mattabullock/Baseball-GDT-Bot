import praw
import os
import sys
import simplejson as json
import webbrowser

cwd = os.path.dirname(os.path.realpath(__file__))
with open(cwd + '/src/settings.json') as data:
    settings = json.load(data)

    CLIENT_ID = settings.get('CLIENT_ID')
    if CLIENT_ID == None: sys.exit("Missing CLIENT_ID")

    CLIENT_SECRET = settings.get('CLIENT_SECRET')
    if CLIENT_SECRET == None: sys.exit("Missing CLIENT_SECRET")

    USER_AGENT = settings.get('USER_AGENT')
    if USER_AGENT == None: sys.exit("Missing USER_AGENT")

    REDIRECT_URI = settings.get('REDIRECT_URI')
    if REDIRECT_URI == None: sys.exit("Missing REDIRECT_URI")


r = praw.Reddit(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri=REDIRECT_URI,
                user_agent=USER_AGENT)

url = r.auth.url(['identity', 'submit', 'edit', 'read', 'modposts', 'privatemessages'], '...', 'permanent')
webbrowser.open(url)

var_input = raw_input("Enter code: ")
access_information = r.auth.authorize(var_input)
print "Refresh token: " + access_information
