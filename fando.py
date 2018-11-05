#!/usr/bin/env python3

import socket
import sys
import os
import random
import datetime
from pytz import timezone


TEST_MODE_NO_IRC=True #When true, doesn't actually connect to IRC, but instead just prints all the IRC commands it would normally make to stdout

class print_class:
    def send(self,msg):
        print(self,msg)
    def recv(self,i):
        return "PRIVMSG #speedrunslive Race initiated for The Legend of Zelda: A Link to the Past Hacks Join TestIfThisWorksFFS"
    def connect(self,j):
        return 1

channel = "#speedrunslive"
server = "irc.freenode.net"
nickname = "testbot_0000"

est=timezone("Canada/Eastern") #AlttpFando hates the west and east coasts. They also hate central NA and all of Europe and Asia, among many other places

class IRC:

    irc=socket.socket()
    botnick="DEFAULT_NAME_PLEASE_CHANGE"

    def __init__(self):
        if TEST_MODE_NO_IRC:
            self.irc=print_class()
        else:
            self.irc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def send(self, chan, msg):
        self.irc.send("PRIVMSG "+chan+" "+msg+"\n")

    def connect(self, server, channel, botnick):
        self.botnick=botnick
        print("connecting to:"+server)
        self.irc.connect((server,6667))
        self.irc.send("USER "+botnick+" "+botnick+" "+botnick+" "+" :This is a bot!\n")
        self.irc.send("NICK "+botnick+"\n")
        self.irc.send("JOIN "+channel+"\n")

    def get_text(self):
        text=self.irc.recv(2040)

        if text.find("PING") != -1:
            self.irc.send("PONG "+text.split()[1]+"\r\n")
        print(text)
        return text

def calc_goal(day=datetime.datetime.now(est).day,month=datetime.datetime.now(est).month,year=datetime.datetime.now(est).year):
    #fix any fuckery from subtracting the day by 1
    if day<1:
        month-=1
        if month<1:
            month=12
        if month in [4,6,9,11]:
            day=30
        elif month==2:
            if year%4==0: #leap year
                day=29
            else:
                day=28
        else:
            day=31

    today=datetime.date(year,month,day).weekday()
    if today==3: #Inverted
        return -2
    elif today==6: #Spoiler Log Sunday
        return -1
    else: #Alright…fuck. So, the easiest way I can think to do this is to just hardcode the mode on a specific date, then do recursive calls until we find that fucker

        #NOTE: this method is super shitty and should be replaced eventually, although I doubt it will be
        if today==0 or today==4: #It's not wednesday or sunday, so skip those days
            return calc_goal(day=day-2)

        if year==2018 and month==11 and day==3:
            return 1 #Standard

        return (calc_goal(day=day-1)+1)%2      


race_channel=""
request_to_race=False
goal_set=False
seed_gen=False
goal=-3

irc = IRC()
irc.connect(server, channel, nickname)


while 1: #If this loop ends, something bad happened. I don't know what, but now 1==0, so…

    #Wait until it's time to race (18:00 PST/21:00 EST)
    while not TEST_MODE_NO_IRC and datetime.datetime.now(est).hour<21:
        #reset all these
        request_to_race=False
        goal_set=False
        race_channel=""
        seed_gen=False
        goal=-3


    text = irc.get_text()

    #Generate race room
    if not request_to_race:
        irc.send(channel,".startrace alttphacks")
        request_to_race=True

    if race_channel=="":
        if "PRIVMSG" in text and channel in text and "Race initiated for The Legend of Zelda: A Link to the Past Hacks" in text:
            j=0
            for i in text.split():
                j+=1
                if i=="Join":
                    race_channel=text.split()[j]
                    print("joining "+race_channel)
                    del irc
                    irc = IRC()
                    irc.connect(server,race_channel,nickname)

    else:
        if not goal_set:
            goal=calc_goal()
            if goal==-1:
                goal_str="ALTTPFando Presents; Spoiler Log Sunday!  Spoiler log and seed provided at 9:45pm EST. Please .ready BEFORE 10pm."
            elif goal==-2:
                goal_str="ALTTPFando Presents: The Community Nightly 10pm Race! Inverted Wednesday!!!! Mode: Inverted with Randomized Swords. Seed gen at 9:50pm EST."
            elif goal==1:
                goal_str="ALTTPFando Presents: The Community Nightly 10pm Race! Mode: Standard with Randomized Swords. Seed gen at 9:50pm EST."
            elif goal==0:
                goal_str="ALTTPFando Presents: The Community Nightly 10pm Race! Mode: Open with Randomized Swords. Seed gen at 9:50pm EST."
            else:
                #Something went wrong. Shit.
                del irc
                print("Invalid goal. Something bad happened")
                exit(1)

            irc.send(race_channel,".setgoal "+goal_str)

        #Ask the other bot to generate a seed at the designated time
        if TEST_MODE_NO_IRC or (((goal==-1 and datetime.datetime.now(est).minute!=45) or datetime.datetime.now(est).minute!=50) and datetime.datetime.now(est).hour!=21) and not seed_gen:
            race_cmd=""
            if goal==0:
               race_cmd=".standard"
            elif goal==1:
               race_cmd=".open"
            elif goal==-2:
               race_cmd=".inverted"
            elif goal==-1:
               race_cmd=".spoiler" #I'm not sure if this is a real thing yet

        irc.send(race_channel,race_cmd)
        seed_gen=True
        if TEST_MODE_NO_IRC:
            exit()



