import praw
r = praw.Reddit(client_id='XXX',
                client_secret='XXX',
                redirect_uri='http://localhost:8080',
                user_agent='OAuth Baseball-GDT Ver. 3.0.3 Setup')

url = r.auth.url(['identity', 'submit', 'edit', 'read', 'modposts', 'privatemessages'], '...', 'permanent')
import webbrowser
webbrowser.open(url)

var_input = input("Enter code: ")
access_information = r.auth.authorize(var_input)
print access_information
raw_input()
