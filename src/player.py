# Pitcher class
# Represents a pitcher in game, holds a pitcher's stats

import math


class pitcher:
    def __init__(self, name="", ip="", h="", r="", er="", bb="", so="", p="", s="", era="", id=""):
        self.name = name
        self.ip = ip
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
        ps = ""
        if self.id != "":
            s = "[" + str(self.name) + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(self.id) + ")"
            ps = str(self.p) + "-" + str(self.s)
        s = s + "|" + str(self.ip) + "|" + str(self.h) + "|" + str(self.r) + "|" + str(self.er) + "|" + str(self.bb) + "|" + str(
            self.so) + "|" + ps + "|" + self.era
        return s


# Batter class
# Represents a batter in game, holds a batter's stats

class batter:
    def __init__(self="", name="", pos="", ab="", r="", h="", rbi="", bb="", so="", ba="", obp="", ops="", id=""):
        self.name = name
        self.pos = pos
        self.ab = ab
        self.r = r
        self.h = h
        self.rbi = rbi
        self.bb = bb
        self.so = so
        self.ba = ba
        self.obp = obp
        self.ops = ops
        self.id = id

    def __str__(self):
        s = " "
        if self.id != "":
            s = "[" + str(self.name) + "](http://mlb.mlb.com/team/player.jsp?player_id=" + str(self.id) + ")"
        s = s + "|" + str(self.pos) + "|" + str(self.ab) + "|" + str(self.r) + "|" + str(self.h) + "|" + str(self.rbi) + "|" + str(self.bb) + "|" + str(self.so) + "|" + str(self.ba) + "/" + str(self.obp) + "/" + str(self.ops)
        return s
