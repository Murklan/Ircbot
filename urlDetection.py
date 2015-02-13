from bs4 import BeautifulSoup
import urllib2

def getURLTitle(data):
    start = data.find('http')
    stop = data.find(' ', start)
    if stop == -1:
        stop = len(data)
    URL = data[start:stop]
    
    if URL.find('i.imgur') != -1 and not URL.find('/a/') != -1:
        URL = fixImgurURL(URL)
        if returnTitle(URL).find('the simple image sharer') != -1:
            return 'That Imgur link does not seem to have a proper title'
        return returnTitle(URL)
    else:
        if URL.find('twitch.tv') != -1:
            return getTwitchTitle(URL)

        return returnTitle(URL)
        

def getTwitchTitle(URL):

    nomnom = getSoup(URL)
    streamTitle = nomnom.findAll(attrs={'property':'og:description'})
    streamer = nomnom.findAll(attrs={'property':'og:title'})
    
    title = 'Twitch > ' + streamer[0]['content'] + ' - ' + streamTitle[0]['content']
    return title

def fixImgurURL(URL):
    
        tempUrl = URL.split('.')
        URL = tempUrl[0]
        URL = 'http://' + tempUrl[1] + '.' + tempUrl[2]
        return URL
 

def returnTitle(URL):
    
    try:
        soup = getSoup(URL)
        title = soup.title.contents[0]
        return 'URL > ' + title.lstrip().encode("utf-8")
    except:
        return "Couldn't find a proper title and/or something went wrong :("


def getSoup(URL):

    soup = BeautifulSoup(urllib2.urlopen(URL).read())
    return soup