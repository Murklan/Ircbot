import cPickle as pickle
import lxml.html
import json
import urllib2
import botvariables

STEAM_API_KEY = botvariables.STEAM_API_KEY
STEAM_API_URL = botvariables.STEAM_API_URL


def now_playing(nickname):
    try:
        with open('nowPlaying', 'rb') as f:
            npdict = pickle.load(f)

            if npdict[nickname]:
                gamenick = npdict[nickname]
                steammessage = steam_status(gamenick)
    except:
        steammessage = str(
            nickname + " is misspelled or does not exist. To add your Steam CustomURL ID type !setsteam <steamcustomurlid>")

    return steammessage


def set_steam(nickname, parameter):
    try:
        with open('nowPlaying', 'rb') as f:
            npdict = pickle.load(f)
    except EOFError:
        npdict = {}

    try:
        nickurl = 'http://steamcommunity.com/id/{0}/games?tab=all&xml=1'.format(parameter)
        steamid = lxml.etree.parse(nickurl).find("steamID64").text
        steamuserdata = json.load(urllib2.urlopen(STEAM_API_URL + '/?key=' + STEAM_API_KEY + '&steamids=' + steamid))

        if steamuserdata['response']['players'][0]['profilestate']:
            npdict[nickname] = parameter
    except:
        return False

    with open('nowPlaying', 'wb') as f:
        pickle.dump(npdict, f)

    return True


# Shows status of player on steam
def steam_status(nickname):
    nickurl = 'http://steamcommunity.com/id/{0}/games?tab=all&xml=1'.format(nickname)
    steamid = lxml.etree.parse(nickurl).find("steamID64").text
    userdata = json.load(urllib2.urlopen(STEAM_API_URL + '/?key=' + STEAM_API_KEY + '&steamids=' + steamid))
    nick = userdata['response']['players'][0]['personaname']

    if userdata['response']['players'][0]['personastate'] >= 1:
        try:
            currentlyplaying = userdata['response']['players'][0]['gameextrainfo']
            return nickname + " is currently Online and playing " + currentlyplaying + " on Steam"
        except KeyError:
            return nickname + " is currently Online but not playing anything on Steam"
    else:
        return nickname + " is currently Offline on Steam"
