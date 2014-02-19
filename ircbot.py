#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, praw, json, time, datetime, threading, os
import cPickle as pickle
from random import randint
from time import localtime, strftime, mktime

import botvariables, nowPlaying, bookmark, googlewiki, urlDetection, redditcheck, remind, translate, wolfram

np = nowPlaying
bm = bookmark
gw = googlewiki
url = urlDetection
rmd = remind
reddit = redditcheck.RedditCheck()
wlf = wolfram
tran = translate

authname = botvariables.authname
authpass = botvariables.authpass
adminHost = botvariables.admin

STEAM_API_KEY = botvariables.STEAM_API_KEY
STEAM_API_URL = botvariables.STEAM_API_URL

running = True
MOTDended = False
class Bot:

    def __init__(self, server, port, nick, channel):
        self.irc_server = server
        self.irc_port = port
        self.nick = nick
        self.channel = channel
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        self.reconnect = False

    def connect(self):
        self.reconnect = True

        try:
            print "Connecting..."
            self.irc_socket.connect((self.irc_server,self.irc_port))
            time.sleep(5)    
            
        except:
            print "Could not connect to server " + self.irc_server + ":" + str(self.irc_port)
            exit(1)
        print "Connected to: " + self.irc_server + ":" + str(self.irc_port)

        while self.is_connected == False:
            recv = self.irc_socket.recv(4096)
            print recv

            if recv.find('Found your hostname') != -1 or recv.find("Couldn't look up your hostname") != -1:

                str_buff = ('NICK %s \r\n') % (self.nick)
                self.irc_socket.send(str_buff.encode())
                print "Setting nickname to: " + self.nick

                time.sleep(1)

                str_buff = ('USER %s 8 * X:\r\n') % (self.nick)
                self.irc_socket.send(str_buff.encode())
                print "Setting user"

                time.sleep(1)

            if str(recv).find("PING") != -1:
                str_buff = ("PONG ".encode() + recv.split()[1] + "\r\n".encode())
                self.irc_socket.send(str_buff.encode())
                
                time.sleep(1)

                str_buff = (('AUTH %s %s\r\n') % (authname, authpass))
                self.irc_socket.send(str_buff.encode())
                print "Authing..."

                time.sleep(1)

                str_buff = ('MODE ' + self.nick + ' +x\r\n')
                self.irc_socket.send(str_buff.encode())
                print "Setting mode: +x"
                
                time.sleep(1)

                str_buff = ('JOIN %s \r\n') % (self.channel)
                self.irc_socket.send(str_buff.encode())
                print "Joining Channel: " + self.channel
                
                time.sleep(1)

                self.is_connected = True

        self.listen()


    def listen(self):
        while self.is_connected:
            recv = self.irc_socket.recv(4096)
            #uncomment to print the recieved data
            #print recv
            if str(recv).find("PING") != -1:
                self.irc_socket.send("PONG ".encode() + recv.split()[1] + "\r\n".encode())

            #Check if someone that joins has a reminder set
            if str(recv).find("JOIN") != -1 and not str(recv).find("PRIVMSG") != -1:
                userNick = str(recv).split('!')[0].split(':')[1]
                channel = (str(recv)).split()[2]
                if rmd.pending(userNick):
                    message = ' '.join(rmd.get_messages(userNick))
                    self.sendMessage(message, channel)
            
            if str(recv).find("PRIVMSG") != -1 and str(recv).find(self.channel) != -1:
                userNick = str(recv).split('!')[0].split(':')[1]
                userHost = str(recv).split("@")[1].split(' ')[0]
                userMessage = self.messageData(str(recv))
                print "(" + strftime("%H:%M:%S", localtime()) + ")<" + userNick + "> " + userMessage
                #Checks for a command
                if (str(userMessage[0]) == '!' or str(userMessage[0] == '！')):
                    self.command = str(userMessage[1:])
                    self.process_command(userNick, userHost, ((str(recv)).split()[2]))
                if (str(userMessage).find('ACTION ' + self.nick) != -1):
                    self.sendMessage((userNick + ', SCHACKMATT!'), (str(recv)).split()[2])
                if (str(userMessage).find('slaps ' + self.nick) != -1 and str(userMessage).find('with a large trout') != -1):
                    self.sendMessage((userNick + ', This is the Trout Protection Agency. Please put the trout down and put your hands in the air'), (str(recv)).split()[2])
                if (str(userMessage).find(' alot') != -1 or str(userMessage).find('alot ') != -1):
                    self.sendMessage(('http://murklan.eu/img/alot.png'), (str(recv)).split()[2])
                if (str(userMessage).find('http://') != -1 or str(userMessage).find('https://') != -1 and not str(userMessage).find('blacklotus.net') != -1):
                    URL = url.getURLTitle(userMessage)
                    self.sendMessage(URL, str(recv).split()[2])
        if self.reconnect:
            self.connect()

    def messageData(self, data):
        data = data[data.find(':')+1:len(data)]
        data = data[data.find(':')+1:len(data)]
        data = str(data[0:len(data)-2])
        return data

    def sendMessage(self, data, channel):
        print "(" + strftime("%H:%M:%S", localtime()) + ")<" + self.nick + "> " + data
        self.irc_socket.send( (("PRIVMSG %s :%s\r\n") % (channel, data)))


    def process_command(self, user, host, channel):

        if len(self.command.split()) == 0:
            return

        command = self.command
        command = command.split()
        command[0] = command[0].lower()

        #admin commands
        if (host == adminHost):
            #dothings
            if (len(command) == 1):
                #things with only one parameter
                
                #shuts down bot
                if (command[0] == 'quit' or command[0] == 'restart'):
                    str_buff = ("QUIT Screw you guys! I'm going home!\r\n")
                    self.irc_socket.send(str_buff.encode())
                    self.irc_socket.close()
                    self.is_connected = False
                    self.reconnect = False
                    if (command[0] == 'restart'):
                        os.execl('restartbot.sh','')

                
            else:
                #!join <channel>
                if (command[0] == "join"):
                    if ( (command[1])[0] == "#"):
                        irc_channel = command[1]
                    else:
                        irc_channel = "#" + command[1]
                    self.join_channel(irc_channel)
                
                #!part <channel>
                if (command[0] == "part"):
                    if ( (command[1])[0] == "#"):
                        irc_channel = command[1]
                    else:
                        irc_channel = "#" + command[1]
                    self.quit_channel(irc_channel)

        #public commands
        if (len(command) == 1):

            if (command[0] == 'hi' or command[0] == 'hello' or command[0] == 'hey'):
                self.sendMessage(('Hello, ' + user + '!'), channel)

            if (command[0] == 'こんにちわ'):
                str_buff = str('こんにちわ, ' + user + '-さん')
                self.sendMessage(str_buff, channel)

            if (command[0] == 'roll'):
                number = str(randint(1,10))
                str_buff = str(user + ' rolled(1-10): ' + number)
                self.sendMessage(str_buff, channel)
            if (command[0] == 'help'):
                self.sendMessage('Available commands: roll, bm, reddit, google, np, remind, translate, wolfram', channel)

        else:
            if (command[0] == 'help'):
                if (command[1] == 'roll'):
                    self.sendMessage('!roll <number> will make a random roll between 1 and <number>. Defaults to 1-10 if you dont enter a number.', channel)
                if (command[1] == 'bm'):
                    if (len(command)>2):
                        if (command[2] == 'add' or command[2] == 'del'):
                            self.sendMessage('!bm add/del <key> will add or delete a key corresponding', channel)
                        elif (command[2] == 'list'):
                            self.sendMessage('!bm list will show a list of the available bookmarks', channel)
                    else:
                        self.sendMessage('!bm <key> will show a bookmark corresponding the given key.', channel)
                if (command[1] == 'reddit'):
                    self.sendMessage('!reddit firstpost/randompost <subreddit> will give the first or a random post from <subreddit>', channel)
                if (command[1] == 'google'):
                    self.sendMessage('!google <search> will give you the first result for <search>. Are you feeling lucky?', channel)
                if (command[1] == 'np'):
                    self.sendMessage("!np <username> will check if <username> is playing anything on steam. To add yourself to the bots 'database', type !setsteam <SteamCustomURL>. ", channel)
                    self.sendMessage('<SteamCustomURL> can be found in the Steam Client -> Community -> Edit profile -> Custom URL', channel)
                if (command[1] == 'remind'):
                    self.sendMessage('!remind <user> <message> will remind <user> of <message> the next time he/she joins the channel', channel)
                if (command[1] == 'translate'): 
                    self.sendMessage('!translate <lang> <phrase> will translate <phrase> into the language <lang>')
                if (command[1] == 'wolfram'):
                    self.sendMessage('Not yet implemented...', channel)

            #they see me rolling
            if (command[0] == 'roll'):
                try:
                    number = str(randint(1, int(command[1])))
                    str_buff = str(user + ' rolled (1-' + command[1] + '): ' + number)
                    self.sendMessage(str_buff, channel)
                except:
                    self.sendMessage("What's a number between 1 and " + command[1] + "...", channel)
                    time.sleep(1)
                    str_buff = str(randint(1, 2147483647) + '?')
                    self.sendMessage(str_buff, channel)
            #Reddit stuff. 
            if (command[0] == 'reddit'):
                if (command[1] == 'firstpost'):
                    try:
                        str_buff = reddit.redditFirst(command[2]).encode('utf-8')
                    except:
                        str_buff = reddit.redditFirst('all').encode('utf-8')
                    self.sendMessage(str_buff, channel)
                if (command[1] == 'randompost'):
                    try:
                        str_buff = reddit.redditRandom(command[2]).encode('utf-8')
                    except:
                        str_buff = reddit.redditRandom('all').encode('utf-8')
                    self.sendMessage(str_buff, channel)
            #Now Playing gaem
            if (command[0] == 'np'):
                str_buff = str(np.nowPlaying(command[1]))
                self.sendMessage(str_buff, channel)
            if (command[0] == 'setsteam'):
                if np.setSteam(user, command[1]):
                    str_buff = str('Successfully set ' + command[1] + ' as SteamID for ' + user)
                    self.sendMessage(str_buff, channel)
                else:
                    self.sendMessage("Successfully didn't set " + command[1] + " as SteamID for " + user + " :(", channel)

            if (command[0] == 'google'):
                commandList = command[1:]
                searchString = ' '.join(commandList)
                URL = gw.googleSearch(searchString)

                self.sendMessage('First result for: ' + searchString, channel)
                self.sendMessage(url.getURLTitle(URL), channel)
                self.sendMessage(URL, channel)

            if (command[0] == 'wolfram'):
                commandList = command[1:]
                searchString = ' '.join(commandList)
                
                wolf = wlf.ask_wolfram(searchString).encode('utf-8')

                self.sendMessage(wolf, channel)             


            if (command[0] == 'translate'):
                lang = command[1]
                commandList = command[2:]
                searchString = ' '.join(commandList)
                
                translation = (tran.translate(searchString, lang)).encode('utf-8')

                self.sendMessage('"' + translation + '"', channel)

            if (command[0] == 'bm'):
                if (len(command) > 2):
                    if (command[1] == 'del'):
                        self.sendMessage(bm.deleteBookmark(command[2]), channel)
                    if (command[1] == 'add'):
                        self.sendMessage(bm.createBookmark(command[2], command[3]), channel)
                else:
                    if (command[1] == 'list'):
                        self.sendMessage(bm.listBookmarks(), channel)
                    else:
                        self.sendMessage(bm.getBookmark(command[1]), channel)

            if (command[0] == 'remind'):
                userNick = command[1]
                commandList = command[2:]
                message = ' '.join(commandList)
                if rmd.add_message(userNick, user, message):
                    self.sendMessage("Set reminder '" + message + "'" + " for user " + userNick, channel)
                else:
                    self.sendMessage("Couldn't set the reminder '" + message + "' for " + userNick, channel)

    def join_channel(self,channel):
        if (channel[0] == "#"):
            str_buff = ( "JOIN %s \r\n" ) % (channel)
            self.irc_socket.send (str_buff.encode())
           
    def quit_channel(self,channel):
        if (channel[0] == "#"):
            str_buff = ( "PART %s \r\n" ) % (channel)
            self.irc_socket.send (str_buff.encode())


ircbot = Bot("irc.quakenet.org", 6667, "^MERKLERN^", '#murklan')
botThread = threading.Thread(None, ircbot.connect())
botThread.start()

while (ircbot.reconnect):
    time.sleep(5)