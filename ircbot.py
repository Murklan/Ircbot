#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, praw, json, time, datetime, threading, os
import cPickle as pickle
from random import randint
from time import localtime, strftime, mktime

import botvariables, nowPlaying, bookmark, googlewiki, urlDetection, redditcheck, remind, translate, wolfram, mtgsearch

np = nowPlaying
bm = bookmark
gw = googlewiki
url = urlDetection
rmd = remind
reddit = redditcheck.RedditCheck()
wlf = wolfram
tran = translate
mtg = mtgsearch

authname = botvariables.authname
authpass = botvariables.authpass
adminHost = botvariables.admin
moderatorHost = botvariables.moderator

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
            self.irc_socket.connect((self.irc_server, self.irc_port))
            time.sleep(5)

        except:
            print "Could not connect to server " + self.irc_server + ":" + str(self.irc_port)
            exit(1)
        print "Connected to: " + self.irc_server + ":" + str(self.irc_port)

        while not self.is_connected:
            recv = self.irc_socket.recv(4096)
            print recv

            if recv.find('Found your hostname') != -1 or recv.find("Couldn't look up your hostname") != -1:
                str_buff = 'NICK %s \r\n' % self.nick
                self.irc_socket.send(str_buff.encode())
                print "Setting nickname to: " + self.nick

                time.sleep(1)

                str_buff = 'USER %s 8 * X:\r\n' % self.nick
                self.irc_socket.send(str_buff.encode())
                print "Setting user"

                time.sleep(1)

            if str(recv).find("PING") != -1:
                str_buff = ("PONG ".encode() + recv.split()[1] + "\r\n".encode())
                self.irc_socket.send(str_buff.encode())

                time.sleep(1)

                str_buff = ('AUTH %s %s\r\n' % (authname, authpass))
                self.irc_socket.send(str_buff.encode())
                print "Authing..."

                time.sleep(1)

                str_buff = ('MODE ' + self.nick + ' +x\r\n')
                self.irc_socket.send(str_buff.encode())
                print "Setting mode: +x"

                time.sleep(1)

                str_buff = 'JOIN %s \r\n' % self.channel
                self.irc_socket.send(str_buff.encode())
                print "Joining Channel: " + self.channel

                time.sleep(1)

                self.is_connected = True

        self.listen()

    def listen(self):
        while self.is_connected:
            recv = self.irc_socket.recv(4096)

            # uncommented to print the recieved data
            # print recv

            if str(recv).find("PING") != -1:
                self.irc_socket.send("PONG ".encode() + recv.split()[1] + "\r\n".encode())

            # Check if someone that joins has a reminder set
            if str(recv).find("JOIN") != -1 and not str(recv).find("PRIVMSG") != -1:
                usernick = str(recv).split('!')[0].split(':')[1]
                channel = (str(recv)).split()[2]
                if rmd.pending(usernick):
                    message = ' '.join(rmd.get_messages(usernick))
                    self.send_message(message, channel)

            if str(recv).find("PRIVMSG") != -1 and str(recv).lower().find(self.channel) != -1:
                usernick = str(recv).split('!')[0].split(':')[1]
                userhost = str(recv).split("@")[1].split(' ')[0]
                usermessage = self.message_data(str(recv))
                print "(" + strftime("%H:%M:%S", localtime()) + ")<" + usernick + "> " + usermessage
                # Checks for a command
                if str(usermessage[0]) == '!':
                    self.command = str(usermessage[1:])
                    self.process_command(usernick, userhost, ((str(recv)).split()[2]))
                # if (str(userMessage).find('ACTION ' + self.nick) != -1):
                #     self.sendMessage((userNick + ', SCHACKMATT!'), (str(recv)).split()[2])
                if (str(usermessage).find('slaps ' + self.nick) != -1 and str(usermessage).find(
                        'with a large trout') != -1):
                    self.send_message((
                                     usernick + ', This is the Trout Protection Agency. Please put the trout down and put your hands in the air'),
                                     (str(recv)).split()[2])
                if str(usermessage).find(' alot') != -1 or str(usermessage).find('alot ') != -1:
                    self.send_message('http://murklan.eu/img/alot.png', (str(recv)).split()[2])
                if (str(usermessage).find('http://') != -1 or str(usermessage).find('https://') != -1 and not str(
                        usermessage).find('blacklotus.net') != -1):
                    reload(urlDetection)
                    URL = url.get_url_title(usermessage)
                    self.send_message(URL, str(recv).split()[2])
        if self.reconnect:
            self.connect()

    def message_data(self, data):
        data = data[data.find(':') + 1:len(data)]
        data = data[data.find(':') + 1:len(data)]
        data = str(data[0:len(data) - 2])
        return data

    def send_message(self, data, channel):
        print "(" + strftime("%H:%M:%S", localtime()) + ")<" + self.nick + "> " + data
        self.irc_socket.send(("PRIVMSG %s :%s\r\n" % (channel, data)))

    def process_command(self, user, host, channel):

        if len(self.command.split()) == 0:
            return

        command = self.command
        command = command.split()
        command[0] = command[0].lower()

        # admin commands
        if host == adminHost:
            # dothings
            if len(command) == 1:
                # things with only one parameter

                # shuts down bot
                if command[0] == 'quit' or command[0] == 'restart':
                    str_buff = "QUIT Screw you guys! I'm going home!\r\n"
                    self.irc_socket.send(str_buff.encode())
                    self.irc_socket.close()
                    self.is_connected = False
                    self.reconnect = False
                    if command[0] == 'restart':
                        os.execl('restartbot.sh', '')


            else:
                # !join <channel>
                if command[0] == "join":
                    if (command[1])[0] == "#":
                        irc_channel = command[1]
                    else:
                        irc_channel = "#" + command[1]
                    self.join_channel(irc_channel)

                # !part <channel>
                if command[0] == "part":
                    if (command[1])[0] == "#":
                        irc_channel = command[1]
                    else:
                        irc_channel = "#" + command[1]
                    self.quit_channel(irc_channel)

        if host == moderatorHost:
            # dothings
            if len(command) == 1:
                # things with only one parameter

                # shuts down bot
                if command[0] == 'restart':
                    str_buff = "QUIT Screw you guys! I'm going home!\r\n"
                    self.irc_socket.send(str_buff.encode())
                    self.irc_socket.close()
                    self.is_connected = False
                    self.reconnect = False
                    os.execl('restartbot.sh', '')

        # public commands
        if len(command) == 1:

            if command[0] == 'hi' or command[0] == 'hello' or command[0] == 'hey':
                self.send_message(('Hello, ' + user + '!'), channel)

            if command[0] == 'こんにちわ':
                str_buff = str('こんにちわ, ' + user + '-さん')
                self.send_message(str_buff, channel)

            if command[0] == 'roll':
                number = str(randint(1, 10))
                str_buff = str(user + ' rolled(1-10): ' + number)
                self.send_message(str_buff, channel)
            if command[0] == 'help':
                self.send_message('Available commands: roll, bm, reddit, google, np, remind, translate, wolfram',
                                  channel)

        else:
            if command[0] == 'help':
                if command[1] == 'roll':
                    self.send_message(
                        '!roll <number> will make a random roll between 1 and <number>. Defaults to 1-10 if you dont enter a number.',
                        channel)
                if command[1] == 'bm':
                    if len(command) > 2:
                        if command[2] == 'add' or command[2] == 'del':
                            self.send_message('!bm add/del <key> will add or delete a key corresponding', channel)
                        elif command[2] == 'list':
                            self.send_message('!bm list will show a list of the available bookmarks', channel)
                    else:
                        self.send_message('!bm <key> will show a bookmark corresponding the given key.', channel)
                if command[1] == 'reddit':
                    self.send_message(
                        '!reddit firstpost/randompost <subreddit> will give the first or a random post from <subreddit>',
                        channel)
                if command[1] == 'google':
                    self.send_message(
                        '!google <search> will give you the first result for <search>. Are you feeling lucky?', channel)
                if command[1] == 'np':
                    self.send_message(
                        "!np <username> will check if <username> is playing anything on steam. To add yourself to the bots 'database', type !setsteam <SteamCustomURL>. ",
                        channel)
                    self.send_message(
                        '<SteamCustomURL> can be found in the Steam Client -> Community -> Edit profile -> Custom URL',
                        channel)
                if command[1] == 'remind':
                    self.send_message(
                        '!remind <user> <message> will remind <user> of <message> the next time he/she joins the channel',
                        channel)
                if command[1] == 'translate':
                    self.send_message('!translate <lang> <phrase> will translate <phrase> into the language <lang>')
                if command[1] == 'wolfram':
                    self.send_message('Not yet implemented...', channel)

            # they see me rolling
            if command[0] == 'roll':
                try:
                    number = str(randint(1, int(command[1])))
                    str_buff = str(user + ' rolled (1-' + command[1] + '): ' + number)
                    self.send_message(str_buff, channel)
                except:
                    self.send_message("What's a number between 1 and " + command[1] + "...", channel)
                    time.sleep(1)
                    str_buff = str(randint(1, 2147483647)) + '?'
                    self.send_message(str_buff, channel)
            # Reddit stuff.
            if command[0] == 'reddit':
                reload(redditcheck)
                if command[1] == 'firstpost':
                    try:
                        str_buff = reddit.get_first_reddit_post(command[2]).encode('utf-8')
                    except:
                        str_buff = reddit.get_first_reddit_post('all').encode('utf-8')
                    self.send_message(str_buff, channel)
                if command[1] == 'randompost':
                    try:
                        str_buff = reddit.get_random_reddit_post(command[2]).encode('utf-8')
                    except:
                        str_buff = reddit.get_random_reddit_post('all').encode('utf-8')
                    self.send_message(str_buff, channel)
            # Now Playing gaem
            if command[0] == 'np':
                reload(nowPlaying)
                print 'Checking if ' + command[1] + 'is a name in my Steam-"database"'
                str_buff = str(np.now_playing(command[1]))
                self.send_message(str_buff, channel)
            if command[0] == 'setsteam':
                reload(nowPlaying)
                if np.set_steam(user, command[1]):
                    str_buff = str('Successfully set ' + command[1] + ' as SteamID for ' + user)
                    self.send_message(str_buff, channel)
                else:
                    self.send_message(
                        "Something went wrong while trying to set " + command[1] + " as SteamID for " + user + " :(",
                        channel)

            if command[0] == 'google':
                reload(googlewiki)
                commandlist = command[1:]
                searchstring = ' '.join(commandlist)
                URL = gw.google_search(searchstring)

                self.send_message('First result for: ' + searchstring, channel)
                self.send_message(url.get_url_title(URL), channel)
                self.send_message(URL, channel)

            if command[0] == 'wolfram':
                reload(wolfram)
                commandlist = command[1:]
                searchstring = ' '.join(commandlist)

                wolf = wlf.ask_wolfram(searchstring).encode('utf-8')

                self.send_message(wolf, channel)

            if command[0] == 'translate':
                reload(translate)
                lang = command[1]
                commandlist = command[2:]
                searchstring = ' '.join(commandlist)

                translation = (tran.translate(searchstring, lang)).encode('utf-8')

                self.send_message('"' + translation + '"', channel)

            if command[0] == 'bm':
                reload(bookmark)
                if len(command) > 2:
                    if command[1] == 'del':
                        self.send_message(bm.delete_bookmark(command[2]), channel)
                    if command[1] == 'add':
                        self.send_message(bm.create_bookmark(command[2], command[3]), channel)
                else:
                    if command[1] == 'list':
                        self.send_message(bm.list_bookmark(), channel)
                    else:
                        self.send_message(bm.get_bookmark(command[1]), channel)

            if command[0] == 'remind':
                reload(remind)
                usernick = command[1]
                commandlist = command[2:]
                message = ' '.join(commandlist)
                if rmd.add_message(usernick, user, message):
                    self.send_message("Set reminder '" + message + "'" + " for user " + usernick, channel)
                else:
                    self.send_message("Couldn't set the reminder '" + message + "' for " + usernick, channel)

            if command[0] == 'mtg':
                reload(mtgsearch)
                commandlist = command[1:
                              ]
                searchname = ' '.join(commandlist)

                try:
                    cardinfo = mtg.card_search(searchname)

                    self.send_message(cardinfo[0], channel)
                except:
                    self.send_message("Can't find the card " + searchname, channel)

                try:
                    self.send_message(mtg.card_price(searchname, cardinfo[1]), channel)
                except:
                    self.send_message(
                        "Can't find the price for the card " + searchname + " (This is borked, will fix someday)",
                        channel)

    def join_channel(self, channel):
        if channel[0] == "#":
            str_buff = "JOIN %s \r\n" % channel
            self.irc_socket.send(str_buff.encode())

    def quit_channel(self, channel):
        if channel[0] == "#":
            str_buff = "PART %s \r\n" % channel
            self.irc_socket.send(str_buff.encode())


ircbot = Bot("irc.quakenet.org", 6667, "^MERKLERN^", '#murklan')

botThread = threading.Thread(None, ircbot.connect())
botThread.start()

while ircbot.reconnect:
    time.sleep(5)
