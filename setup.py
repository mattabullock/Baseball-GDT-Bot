import praw
r = praw.Reddit(client_id='xxx',
                client_secret='xxx',
                redirect_uri='http://localhost:8080',
                user_agent='OAuth Baseball-GDT Ver. 3.0.3 Setup')

url = r.auth.url(['identity', 'submit', 'edit', 'read', 'modposts', 'privatemessages', 'flair', 'modflair'], '...', 'permanent')
import webbrowser
webbrowser.open(url)

var_input = input("Enter code: ")
access_information = r.auth.authorize(var_input)
print access_information
raw_input()
