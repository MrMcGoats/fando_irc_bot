#!/usr/bin/env python3

import socket
import sys
from testing import *

TEST_MODE_NO_IRC=False #When true, doesn't actually connect to IRC, but instead just prints all the IRC commands it would normally make to stdout

class IRC:

    irc=socket.socket()
    botnick="DEFAULT_NAME_PLEASE_CHANGE"

    def __init__(self):
        if TEST_MODE_NO_IRC:
            self.irc=print_class()
        else:
            self.irc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def send(self, chan, msg):
        if not TEST_MODE_NO_IRC: print("PRIVMSG "+chan+" "+msg)
        msg="PRIVMSG "+chan+" "+msg+"\n"
        self.irc.sendall(msg.encode('utf-8'))

    def connect(self, server, channel, botnick):
        self.botnick=botnick
        print("connecting to:"+server)
        self.irc.connect((server,6667))
        join_msg="USER "+botnick+" "+botnick+" "+botnick+" "+" :This is a bot!\n"
        login_msg="NICK "+botnick+"\n"
        chan_msg="JOIN "+channel+"\n"
        self.irc.sendall(join_msg.encode('utf-8'))
        self.irc.sendall(login_msg.encode('utf-8'))
        self.irc.sendall(chan_msg.encode('utf-8'))
        print("Connected!")
        
    def get_text(self):
        text=self.irc.recv(2040)

        if text.find(b"PING") != -1:
            pong="PONG "+text.split()[1]+"\r\n"
            self.irc.sendall(pong.encode('utf-8'))
        print(text)
        return text
    
if __name__=="__main__":
    TEST_MODE_NO_IRC=True
    test_bot=IRC()
    test_bot.connect("test_serv","test_chan","testbot")
    test_bot.send("test_chan","This is a test message")
    print(test_bot.get_text())
