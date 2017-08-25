from Tkinter import *
import json
from sys import executable, exit
from subprocess import Popen, CREATE_NEW_CONSOLE

def GUI():
    root = Tk()
    root.title("Baseball GDT Bot 3.0.2")
    root.geometry('605x625')
    def quit():
        root.quit()

    while True:
        with open('settings.json') as data:
            settings = json.load(data)
            CLIENT_ID = settings.get('CLIENT_ID')
            CLIENT_SECRET = settings.get('CLIENT_SECRET')
            REDIRECT_URI = settings.get('REDIRECT_URI')
            REFRESH_TOKEN = settings.get('REFRESH_TOKEN')
            BOT_TIME_ZONE = settings.get('BOT_TIME_ZONE')
            TEAM_TIME_ZONE = settings.get('TEAM_TIME_ZONE')
            POST_TIME = settings.get('POST_TIME')
            PRE_POST_TIME = settings.get('PRE_POST_TIME')
            SUBREDDIT = settings.get('SUBREDDIT')
            TEAM_CODE = settings.get('TEAM_CODE')
            PREGAME_THREAD = settings.get('PREGAME_THREAD')
            POST_GAME_THREAD = settings.get('POST_GAME_THREAD')
            STICKY = settings.get('STICKY')
            SUGGESTED_SORT = settings.get('SUGGESTED_SORT')
            MESSAGE = settings.get('MESSAGE')
            thread_settings = settings.get('THREAD_SETTINGS')
            content_settings = thread_settings.get('CONTENT')
            THREAD_TAG = thread_settings.get('THREAD_TAG')
            HEADER = content_settings.get('HEADER')
            BOX_SCORE = content_settings.get('BOX_SCORE')
            LINE_SCORE = content_settings.get('LINE_SCORE')
            SCORING_PLAYS = content_settings.get('SCORING_PLAYS')
            HIGHLIGHTS = content_settings.get('HIGHLIGHTS')
            FOOTER = content_settings.get('FOOTER')
            postthread_settings = settings.get('POST_THREAD_SETTINGS')
            postcontent_settings = postthread_settings.get('CONTENT')
            POST_THREAD_TAG = postthread_settings.get('POST_THREAD_TAG')
            POST_HEADER = postcontent_settings.get('HEADER')
            POST_BOX_SCORE = postcontent_settings.get('BOX_SCORE')
            POST_LINE_SCORE = postcontent_settings.get('LINE_SCORE')
            POST_SCORING_PLAYS = postcontent_settings.get('SCORING_PLAYS')
            POST_HIGHLIGHTS = postcontent_settings.get('HIGHLIGHTS')
            POST_FOOTER = postcontent_settings.get('FOOTER')
            prethread_settings = settings.get('PRE_THREAD_SETTINGS')
            precontent_settings = prethread_settings.get('CONTENT')
            PRE_THREAD_TAG = prethread_settings.get('PRE_THREAD_TAG')
            PRE_THREAD_TIME = prethread_settings.get('PRE_THREAD_TIME')
            PROBABLES = precontent_settings.get('PROBABLES')
            FIRST_PITCH = precontent_settings.get('FIRST_PITCH')

        def SaveSettings():
            data = {
                "CLIENT_ID": ClientID.get(),
                "CLIENT_SECRET": ClientSecret.get(),
                "REDIRECT_URI": RedirectURI.get(),
                "REFRESH_TOKEN": RefreshToken.get(),
                "BOT_TIME_ZONE": BotTimeZoneVar.get(),
                "TEAM_TIME_ZONE": TeamTimeZoneVar.get(),
                "POST_TIME": int(PostTimeVar.get()),
                "PRE_POST_TIME": PreThreadTimeVar.get(),
                "SUBREDDIT": Subreddit.get(),
                "TEAM_CODE": TeamCodeVar.get(),
                "PREGAME_THREAD": PregameThreadVar.get(),
                "POST_GAME_THREAD": PostgameThreadVar.get(),
                "SUGGESTED_SORT": SuggestedSortVar.get(),
                "MESSAGE": MessageVar.get(),
                "STICKY": StickyVar.get(),
                "PRE_THREAD_SETTINGS": {
                    "PRE_THREAD_TAG": PregameThreadTag.get(),
                    "PRE_THREAD_TIME": PreThreadTimeVar.get(),
                    "CONTENT": {
                        "PROBABLES": ProbablesVar.get(),
                        "FIRST_PITCH": FirstPitchVar.get()
                    }
                },
                "THREAD_SETTINGS": {
                    "THREAD_TAG": ThreadTag.get(),
                    "CONTENT": {
                        "HEADER": HeaderVar.get(),
                        "BOX_SCORE": BoxScoreVar.get(),
                        "LINE_SCORE": LineScoreVar.get(),
                        "SCORING_PLAYS": ScoringPlaysVar.get(),
                        "HIGHLIGHTS": HighlightsVar.get(),
                        "FOOTER": FooterVar.get()
                    }
                },
                "POST_THREAD_SETTINGS": {
                    "POST_THREAD_TAG": PostgameThreadTag.get(),
                    "CONTENT": {
                        "HEADER": PostHeaderVar.get(),
                        "BOX_SCORE": PostBoxScoreVar.get(),
                        "LINE_SCORE": PostLineScoreVar.get(),
                        "SCORING_PLAYS": PostScoringPlaysVar.get(),
                        "HIGHLIGHTS": PostHighlightsVar.get(),
                        "FOOTER": PostFooterVar.get()
                    }
                }
            }
            with open("settings.json","w") as f:
                json.dump(data, f, indent=4, sort_keys=True)

        def RunBot():
            Popen([executable, 'main.py'])

        def RunBotnWin():
            Popen([executable, 'main.py'],creationflags=CREATE_NEW_CONSOLE)

        def Reload():
            quit()

        #Controls
        group = LabelFrame(root, text="Controls", padx=5, pady=5)
        group.place(x=0,y=400,height=225,width=300)

        f = Frame(group)

        SaveSettingsButton = Button(f, text="Save Settings", command=SaveSettings)
        SaveSettingsButton.pack(anchor=W,padx=1,pady=2)

        ReloadSettingsButton = Button(f, text="Load Settings", command=Reload)
        ReloadSettingsButton.pack(anchor=W,padx=1,pady=2)

        f.pack(side=LEFT,anchor=NW)

        f = Frame(group)

        RunBotButton = Button(f, text="Run in New Console", command=RunBotnWin)
        RunBotButton.pack(side=BOTTOM,anchor=SW,padx=1,pady=2)

        RunBotButton = Button(f, text="Run in This Console", command=RunBot)
        RunBotButton.pack(side=BOTTOM,anchor=SW,padx=1,pady=2)

        f.pack(side=LEFT,anchor=NW,padx=2)

        f = Frame(group)

        ReloadSettingsButton = Button(f, text="Close", command=exit)
        ReloadSettingsButton.pack(anchor=W,padx=1,pady=2)

        f.pack(side=RIGHT,anchor=NW,padx=2)

        #OAuthSettings
        group = LabelFrame(root, text="OAuth Settings", padx=5, pady=5)
        group.place(x=0,y=0,height=200,width=300)

        l = Label(group, text="Client ID")
        l.pack(anchor=W)

        ClientID = Entry(group)
        ClientID.pack(fill=X,padx=10)
        if CLIENT_ID != "":
            ClientID.insert(0, CLIENT_ID)
        else:
            ClientID.insert(0, "Client ID")

        l = Label(group, text="Client Secret")
        l.pack(anchor=W)

        ClientSecret = Entry(group)
        ClientSecret.pack(fill=X,padx=10)
        if CLIENT_SECRET != "":
            ClientSecret.insert(0, CLIENT_SECRET)
        else:
            ClientSecret.insert(0, "Client Secret")

        l = Label(group, text="Redirect URI")
        l.pack(anchor=W)

        RedirectURI = Entry(group)
        RedirectURI.pack(fill=X,padx=10)
        if REDIRECT_URI != "":
            RedirectURI.insert(0, REDIRECT_URI)
        else:
            RedirectURI.insert(0, "Redirect URI")

        l = Label(group, text="Refresh Token")
        l.pack(anchor=W)

        RefreshToken = Entry(group)
        RefreshToken.pack(fill=X,padx=10)
        if REFRESH_TOKEN != "":
            RefreshToken.insert(0, REFRESH_TOKEN)
        else:
            RefreshToken.insert(0, "Refresh Token")

        #GeneralSettings
        group = LabelFrame(root, text="General Settings", padx=5, pady=5)
        group.place(x=0,y=200,height=200,width=300)

        l = Label(group, text="Subreddit")
        l.pack(anchor=W)

        Subreddit = Entry(group)
        Subreddit.pack(fill=X,padx=10)
        if SUBREDDIT != "":
            Subreddit.insert(0, SUBREDDIT)
        else:
            Subreddit.insert(0, "Subreddit")

        StickyVar = IntVar()
        Sticky = Checkbutton(group, text="Toggle Sticky", variable=StickyVar)
        if STICKY == 1:
            Sticky.select()
            Sticky.pack(anchor=W)
        else:
            Sticky.pack(anchor=W)

        l = Label(group, text="Localization")
        l.pack(anchor=W)

        f = Frame(group)

        BotTimeZone = [
            "ET","CT","MT","PT"
        ]
        BotTimeZoneVar = StringVar(f)
        if BOT_TIME_ZONE == "ET" or "CT" or "MT" or "PT":
            BotTimeZoneVar.set(BOT_TIME_ZONE)
        else:
            BotTimeZoneVar.set(BotTimeZone[0])
        BotTimeZone = apply(OptionMenu, (f, BotTimeZoneVar) + tuple(BotTimeZone))
        BotTimeZone.pack(anchor=W, side=LEFT)

        l = Label(f, text="Bot Time Zone")
        l.pack(anchor=W, side=LEFT)

        f.pack(fill=X,padx=10)

        f = Frame(group)

        TeamTimeZone = [
            "ET","CT","MT","PT"
        ]
        TeamTimeZoneVar = StringVar(f)
        if TEAM_TIME_ZONE == "ET" or "CT" or "MT" or "PT":
            TeamTimeZoneVar.set(TEAM_TIME_ZONE)
        else:
            TeamTimeZoneVar.set(TeamTimeZone[0])
        TeamTimeZone = apply(OptionMenu, (f, TeamTimeZoneVar) + tuple(TeamTimeZone))
        TeamTimeZone.pack(side=LEFT, anchor=W)

        l = Label(f, text="Team Time Zone")
        l.pack(side=LEFT, anchor=W)

        f.pack(fill=X,padx=10)

        f = Frame(group)

        TeamCode = [
            "ana","ari","atl","bal","bos","cha","chn","cin","cle","col","det","hou","kca","lan","mia","min","mil","nya","nyn","oak","phi","pit","sdn","sea","sfn","sln","tex","tba","tor","was"
        ]
        TeamCodeVar = StringVar(f)
        if TEAM_CODE != "":
            TeamCodeVar.set(TEAM_CODE)
        else:
            TeamCodeVar.set(TeamCode[0])
        TeamCode = apply(OptionMenu, (f, TeamCodeVar) + tuple(TeamCode))
        TeamCode.pack(side=LEFT, anchor=W)

        l = Label(f, text="Team Code")
        l.pack(side=LEFT, anchor=W)

        f.pack(fill=X,padx=10)

        #GameThreadSettings
        group = LabelFrame(root, text="Game Thread Settings", padx=5, pady=5)
        group.place(x=305,y=200,height=250,width=300)

        l = Label(group, text="Game Thread Tag")
        l.pack(anchor=W)

        ThreadTag = Entry(group)
        ThreadTag.pack(fill=X,padx=10)
        if THREAD_TAG != "":
            ThreadTag.insert(0, THREAD_TAG)
        else:
            ThreadTag.insert(0, "Game Thread Tag")

        l = Label(group, text="Modules")
        l.pack(anchor=W)

        f = Frame(group)

        SuggestedSort = [
            "New","Best","Blank"
        ]
        SuggestedSortVar = StringVar(f)
        if SUGGESTED_SORT != "":
            SuggestedSortVar.set(SUGGESTED_SORT)
        else:
            SuggestedSortVar.set(SuggestedSort[0])
        SuggestedSort = apply(OptionMenu, (f, SuggestedSortVar) + tuple(SuggestedSort))
        SuggestedSort.pack(side=LEFT, anchor=W)

        l = Label(f, text="Suggested Sort")
        l.pack(side=LEFT, anchor=W)

        f.pack(side=BOTTOM,fill=X,padx=10)

        f = Frame(group)
        PostTime = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        ]
        PostTimeVar = StringVar(f)
        if POST_TIME != "":
            PostTimeVar.set(POST_TIME)
        else:
            PostTimeVar.set(PostTime[0])
        PostTime = apply(OptionMenu, (f, PostTimeVar) + tuple(PostTime))
        PostTime.pack(side=LEFT, anchor=W)

        l = Label(f, text="Post Time (hours before game)")
        l.pack(side=LEFT, anchor=W)

        f.pack(side=BOTTOM,fill=X,padx=10)

        f = Frame(group)

        HeaderVar = IntVar()
        Header = Checkbutton(f, text="Header", variable=HeaderVar)
        if HEADER == 1:
            Header.select()
            Header.pack(anchor=W)
        else:
            Header.pack(anchor=W)

        BoxScoreVar = IntVar()
        BoxScore = Checkbutton(f, text="Box Score", variable=BoxScoreVar)
        if BOX_SCORE == 1:
            BoxScore.select()
            BoxScore.pack(anchor=W)
        else:
            BoxScore.pack(anchor=W)

        LineScoreVar = IntVar()
        LineScore = Checkbutton(f, text="Line Score", variable=LineScoreVar)
        if LINE_SCORE == 1:
            LineScore.select()
            LineScore.pack(anchor=W)
        else:
            LineScore.pack(anchor=W)

        MessageVar = IntVar()
        Message = Checkbutton(f, text="Message BaseballBot", variable=MessageVar)
        if MESSAGE == 1:
            Message.select()
            Message.pack(anchor=W)
        else:
            Message.pack(anchor=W)

        f.pack(side=LEFT, anchor=N)

        f = Frame(group)

        ScoringPlaysVar = IntVar()
        ScoringPlays = Checkbutton(f, text="Scoring Plays", variable=ScoringPlaysVar)
        if SCORING_PLAYS == 1:
            ScoringPlays.select()
            ScoringPlays.pack(anchor=W)
        else:
            ScoringPlays.pack(anchor=W)

        HighlightsVar = IntVar()
        Highlights = Checkbutton(f, text="Highlights", variable=HighlightsVar)
        if HIGHLIGHTS == 1:
            Highlights.select()
            Highlights.pack(anchor=W)
        else:
            Highlights.pack(anchor=W)

        FooterVar = IntVar()
        Footer = Checkbutton(f, text="Footer", variable=FooterVar)
        if FOOTER == 1:
            Footer.select()
            Footer.pack(anchor=W)
        else:
            Footer.pack(anchor=W)

        f.pack(side=RIGHT, anchor=N)

        #PregameSettings
        group = LabelFrame(root, text="Pregame Thread Settings", padx=5, pady=5)
        group.place(x=305,y=0,height=200,width=300)

        PregameThreadVar = IntVar()
        PregameThread = Checkbutton(group, text="Toggle Pregame Thread", variable=PregameThreadVar)
        if PREGAME_THREAD == 1:
            PregameThread.select()
            PregameThread.pack(anchor=W)
        else:
            PregameThread.pack(anchor=W)

        l = Label(group, text="Pregame Thread Tag")
        l.pack(anchor=W)

        PregameThreadTag = Entry(group)
        PregameThreadTag.pack(fill=X,padx=10)
        if PRE_THREAD_TAG != "":
            PregameThreadTag.insert(0, PRE_THREAD_TAG)
        else:
            PregameThreadTag.insert(0, "Pregame Thread Tag")

        l = Label(group, text="Modules")
        l.pack(anchor=W)

        ProbablesVar = IntVar()
        Probables = Checkbutton(group, text="Probables", variable=ProbablesVar)
        if PROBABLES == 1:
            Probables.select()
            Probables.pack(anchor=W)
        else:
            Probables.pack(anchor=W)

        FirstPitchVar = IntVar()
        FirstPitch = Checkbutton(group, text="First Pitch", variable=FirstPitchVar)
        if FIRST_PITCH == 1:
            FirstPitch.select()
            FirstPitch.pack(anchor=W)
        else:
            FirstPitch.pack(anchor=W)

        f = Frame(group)

        PreThreadTime = [
            "6AM", "7AM", "8AM", "9AM", "10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM", "5PM", "6PM", "7PM"
        ]
        PreThreadTimeVar = StringVar(f)
        if PRE_THREAD_TIME != "":
            PreThreadTimeVar.set(PRE_POST_TIME)
        else:
            PreThreadTimeVar.set(PreThreadTime[0])
        PreThreadTime = apply(OptionMenu, (f, PreThreadTimeVar) + tuple(PreThreadTime))
        PreThreadTime.pack(side=LEFT)

        l = Label(f, text="Pregame Thread Time")
        l.pack(side=LEFT)

        f.pack(side=BOTTOM,fill=X,padx=10)

        #Postgame settings
        group = LabelFrame(root, text="Postgame Thread Settings", padx=5, pady=5)
        group.place(x=305,y=450,height=175,width=300)

        PostgameThreadVar = IntVar()
        PostgameThread = Checkbutton(group, text="Toggle Postgame Thread", variable=PostgameThreadVar)
        if POST_GAME_THREAD == 1:
            PostgameThread.select()
            PostgameThread.pack(anchor=W)
        else:
            PostgameThread.pack(anchor=W)

        l = Label(group, text="Postgame Thread Tag")
        l.pack(anchor=W)

        PostgameThreadTag = Entry(group)
        PostgameThreadTag.pack(fill=X,padx=10)
        if PRE_THREAD_TAG != "":
            PostgameThreadTag.insert(0, POST_THREAD_TAG)
        else:
            PostgameThreadTag.insert(0, "Postgame Thread Tag")

        l = Label(group, text="Modules")
        l.pack(anchor=W)

        f = Frame(group)

        PostHeaderVar = IntVar()
        PostHeader = Checkbutton(f, text="Header", variable=PostHeaderVar)
        if POST_HEADER == 1:
            PostHeader.select()
            PostHeader.pack(anchor=W)
        else:
            PostHeader.pack(anchor=W)

        PostBoxScoreVar = IntVar()
        PostBoxScore = Checkbutton(f, text="Box Score", variable=PostBoxScoreVar)
        if POST_BOX_SCORE == 1:
            PostBoxScore.select()
            PostBoxScore.pack(anchor=W)
        else:
            PostBoxScore.pack(anchor=W)

        PostLineScoreVar = IntVar()
        PostLineScore = Checkbutton(f, text="Line Score", variable=PostLineScoreVar)
        if POST_LINE_SCORE == 1:
            PostLineScore.select()
            PostLineScore.pack(anchor=W)
        else:
            PostLineScore.pack(anchor=W)

        f.pack(side=LEFT, anchor=N)

        f = Frame(group)

        PostScoringPlaysVar = IntVar()
        PostScoringPlays = Checkbutton(f, text="Scoring Plays", variable=PostScoringPlaysVar)
        if POST_SCORING_PLAYS == 1:
            PostScoringPlays.select()
            PostScoringPlays.pack(anchor=W)
        else:
            PostScoringPlays.pack(anchor=W)

        PostHighlightsVar = IntVar()
        PostHighlights = Checkbutton(f, text="Highlights", variable=PostHighlightsVar)
        if POST_HIGHLIGHTS == 1:
            PostHighlights.select()
            PostHighlights.pack(anchor=W)
        else:
            PostHighlights.pack(anchor=W)

        PostFooterVar = IntVar()
        PostFooter = Checkbutton(f, text="Footer", variable=PostFooterVar)
        if POST_FOOTER == 1:
            PostFooter.select()
            PostFooter.pack(anchor=W)
        else:
            PostFooter.pack(anchor=W)

        f.pack(side=RIGHT, anchor=N)

        root.mainloop()

GUI()
