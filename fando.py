#!/usr/bin/env python3

from calc_goal import *
from irc import *
from testing import *



channel = "#speedrunslive"
server = "irc.speedrunslive.com"
nickname = "FandoNightlyBot"

race_channel=""
request_to_race=False
goal_set=False
seed_gen=False
goal=-3

irc = IRC()
irc.connect(server, channel, nickname)

try:
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
                    print("Invalid goal. Something bad happened. Exiting.")
                    exit(1)

                irc.send(race_channel,".setgoal "+goal_str)

            #Ask the other bot to generate a seed at the designated time
            if TEST_MODE_NO_IRC or (((goal==-1 and datetime.datetime.now(est).minute==45) or datetime.datetime.now(est).minute==50) and datetime.datetime.now(est).hour==21) and not seed_gen:
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
except KeyboardInterrupt as e:
    exit(0)
