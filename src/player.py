# Pitcher class
# Represents a pitcher in game, holds a pitcher's stats

import math


class pitcher:
    def __init__(self, name="", o="", h="", r="", er="", bb="", so="", p="", s="", era="", id=""):
        self.name = name
        self.o = o
        self.h = h
        self.r = r
        self.er = er
        self.bb = bb
        self.so = so
        self.p = p
        self.s = s
        self.era = era
        self.id = id

    def __str__(self):
        s = " "
        ip = ""
        ps = ""
        if self.id != "":
            ipf = str(math.floor(float(self.o) / 3))
            ipd = str(math.floor(float(self.o) % 3))
            ip = ipf[0][0] + "." + ipd[0][0]
            s = "[" + str(self.name) + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(self.id) + ")"
            ps = str(self.p) + "-" + str(self.s)
        s = s + "|" + ip + "|" + str(self.h) + "|" + str(self.r) + "|" + str(self.er) + "|" + str(self.bb) + "|" + str(
            self.so) + "|" + ps + "|" + self.era
        return s


# Batter class
# Represents a batter in game, holds a batter's stats

class batter:
    def __init__(self="", name="", pos="", ab="", r="", h="", rbi="", bb="", so="", ba="", id=""):
        self.name = name
        self.pos = pos
        self.ab = ab
        self.r = r
        self.h = h
        self.rbi = rbi
        self.bb = bb
        self.so = so
        self.ba = ba
        self.id = id

    def __str__(self):
        s = " "
        if self.id != "":
            s = "[" + str(self.name) + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(self.id) + ")"
        s = s + "|" + str(self.pos) + "|" + str(self.ab) + "|" + str(self.r) + "|" + str(self.h) + "|" + str(
            self.rbi) + "|" + str(self.bb) + "|" + str(self.so) + "|" + str(self.ba)
        return s


class decision:
    def __init__(self, name="", note="", id=""):
        self.name = name
        self.note = note
        self.id = id

    def __str__(self):
        w = ""
        h = ""
        s = ""
        l = ""
        b = ""
        n = ""

        if 'W' in str(self.note):
            w = "[" + str(self.name) + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(
                self.id) + ")" + " " + str(self.note) + " "
        else:
            if 'H' in str(self.note):
                h = "[" + str(self.name) + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(
                    self.id) + ")" + " " + str(self.note) + " "
            else:
                if 'S' in str(self.note):
                    s = "[" + str(self.name) + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(
                        self.id) + ")" + " " + str(self.note) + " "
                else:
                    if 'L' in str(self.note):
                        l = "[" + str(self.name) + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(
                            self.id) + ")" + " " + str(self.note) + " "
                    else:
                        if 'B' in str(self.note):
                            s = "[" + str(self.name) + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(
                                self.id) + ")" + " " + str(self.note) + " "
                        else:
                            if 'N' in str(self.note):
                                n = ""
        return w + h + s + l + b + n