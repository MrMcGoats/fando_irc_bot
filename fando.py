#!/usr/bin/env python3

import socket
import sys
import os
import random
import datetime

channel = "#testing_59561478"
server = "irc.freenode.net"
nickname = "testbot_0000"

class IRC:

    irc=socket.socket()
    botnick="DEFAULT_NAME_PLEASE_CHANGE"

    def __init__(self):
        self.irc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def send(self, chan, msg):
        self.irc.send("PRIVMSG "+chan+" "+msg+"\n")

    def connect(self, server, channel, botnick):
        self.botnick=botnick
        print("connecting to:"+server)
        self.irc.connect((server,6667))
        self.irc.send("USER "+botnick+" "+botnick+" "+botnick+" "+" :This is a fun bot!\n")
        self.irc.send("NICK "+botnick+"\n")
        self.irc.send("JOIN "+channel+"\n")

    def switch_channel(self, channel):
        self.irc.send("JOIN "+channel+"\n")

    def get_text(self):
        text=self.irc.recv(2040)

        if text.find("PING") != -1:
            self.irc.send("PONG "+text.split()[1]+"\r\n")

        return text

def calc_goal(day=datetime.datetime.now().day,month=datetime.datetime.now().month,year=datetime.datetime.now().year):
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
    print("today="+str(today))
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

irc = IRC()
irc.connect(server, channel, nickname)


while 1:
    text = irc.get_text()
    print(text)

    if not request_to_race:
        irc.send(channel,".startrace alttphacks")
        request_to_race=True

    if race_channel=="":
        if "PRIVMSG" in text and channel in text and "Race initiated for The Legend of Zelda: A Link to the Past Hacks" in text:
            next=False
            for i in text.split():
                print(i)
                if next:
                    if i[0]!="#":
                        continue

                    race_channel=i 
                    print("joining "+race_channel)
                    del irc
                    irc = IRC()
                    irc.connect(server,race_channel,nickname)
                    break
                if i=="Join":
                    next=True

    else:
        if not goal_set:
            goal=calc_goal()
            if goal==-1:
                goal="ALTTPFando Presents; Spoiler Log Sunday!  Spoiler log and seed provided at 9:45pm EST. Please .ready BEFORE 10pm."
            elif goal==-2:
                goal="ALTTPFando Presents: The Community Nightly 10pm Race! Inverted Wednesday!!!! Mode: Inverted with Randomized Swords. Seed gen at 9:50pm EST."
            elif goal==1:
                goal="ALTTPFando Presents: The Community Nightly 10pm Race! Mode: Standard with Randomized Swords. Seed gen at 9:50pm EST."
            elif goal==0:
                goal="ALTTPFando Presents: The Community Nightly 10pm Race! Mode: Open with Randomized Swords. Seed gen at 9:50pm EST."
            else:
                #Something went wrong. Shit.
                exit(1)
            
            irc.send(race_channel,".setgoal "+goal)



