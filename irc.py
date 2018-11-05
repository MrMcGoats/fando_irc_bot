import socket
import sys
from testing import *

TEST_MODE_NO_IRC=True #When true, doesn't actually connect to IRC, but instead just prints all the IRC commands it would normally make to stdout

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
    
if __name__=="__main__":
    print("This is not an executable")
