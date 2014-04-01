import cPickle as pickle
import lxml.html
import json
import urllib2
import botvariables

STEAM_API_KEY = botvariables.STEAM_API_KEY
STEAM_API_URL = botvariables.STEAM_API_URL

def nowPlaying(nickname):
    try:
        with open('nowPlaying', 'rb') as f:
            npDict = pickle.load(f)

            if npDict[nickname]:
                gameNick = npDict[nickname]
                steamMessage = steamStatus(gameNick) 
    except :
        steamMessage =  str(nickname + " is misspelled or does not exist. To add your Steam CustomURL ID type !setsteam <steamcustomurlid>")

    # try:
    #     with open('nowPlaying', 'rb') as f:
    #         npDict = pickle.load(f)

    #         if npDict[nickname + "xbl"]:
    #             gameNick = npDict[nickname + "xbl"]
    #             xblMessage = xblStatus(gameNick)
    # except :
    #     xblMessage = " is misspelled or does not exist. To add your Xbox Live gamertag type !setxbl <gamertag>"

    #return xblMessage
    return steamMessage

def setSteam(nickname, parameter):
    
    try:
        with open('nowPlaying', 'rb') as f:
            npDict = pickle.load(f)
    except EOFError:
        npDict = {}

    try:
        nickUrl = 'http://steamcommunity.com/id/{0}/games?tab=all&xml=1'.format(parameter)
        steamid = lxml.etree.parse(nickUrl).find("steamID64").text
        steamUserData = json.load(urllib2.urlopen(STEAM_API_URL + '/?key=' + STEAM_API_KEY + '&steamids=' + steamid))

        if steamUserData['response']['players'][0]['profilestate']:
            npDict[nickname] = parameter  
    except:
        return False

    with open('nowPlaying', 'wb') as f:
        pickle.dump(npDict, f)

    return True

#Shows status of player on steam
def steamStatus(nickname):
    
    nickUrl = 'http://steamcommunity.com/id/{0}/games?tab=all&xml=1'.format(nickname)
    steamid = lxml.etree.parse(nickUrl).find("steamID64").text
    userData = json.load(urllib2.urlopen(STEAM_API_URL + '/?key=' + STEAM_API_KEY + '&steamids=' + steamid))
    nick = userData['response']['players'][0]['personaname']

    if userData['response']['players'][0]['personastate'] >= 1:
        try:
            currentlyPlaying = userData['response']['players'][0]['gameextrainfo']
            return nickname + " is currently Online and playing " + currentlyPlaying + " on Steam"
        except KeyError:
            return nickname + " is currently Online but not playing anything on Steam"
    else:
        return nickname + " is currently Offline on Steam"


# def setXbl(nickname, parameter):
#     parameter = parameter[1]
#     xblUserData = json.load(urllib2.urlopen('https://www.xboxleaders.com/api/1.0/profile.json?gamertag=' + parameter))

#     try:
#         with open('nowPlaying', 'rb') as f:
#             npDict = pickle.load(f)
#     except EOFError:
#         npDict = {}

#     try:
#         if xblUserData['Data']['Gamertag']:
#             npDict[nickname + "xbl"] = parameter
#     except KeyError:
#         return False

#     with open('nowPlaying', 'wb') as f:
#         pickle.dump(npDict, f)
        
#     return True

# def xblStatus(nickname):

#     xblUserData = json.load(urllib2.urlopen('https://www.xboxleaders.com/api/1.0/profile.json?gamertag=' + nickname))
#     xblnick = xblUserData['Data']['Gamertag']
    
#     if xblUserData['Data']['IsOnline'] == 1:
#         xblCurrentlyPlaying = xblUserData['Data']['OnlineStatus']
#         return " is currently " + xblCurrentlyPlaying + " on XBOX Live"
#     else:
#         return "Offline"
