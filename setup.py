import praw
r = praw.Reddit(client_id='Y9ii85xkpxdFdw',
                client_secret='APUT0YMWILRisrdSk4YTNs41c10',
                redirect_uri='http://localhost:8080',
                user_agent='OAuth Baseball-GDT Ver. 3.0.3 Setup')

url = r.auth.url(['identity', 'submit', 'edit', 'read', 'modposts', 'privatemessages'], '...', 'permanent')
import webbrowser
webbrowser.open(url)

var_input = input("Enter code: ")
access_information = r.auth.authorize(var_input)
print access_information
raw_input()
