from bs4 import BeautifulSoup
import urllib2

def getURLTitle(data):
        start = data.find('http')
        stop = data.find(' ', start)
        if stop == -1:
            stop = len(data)
        URL = data[start:stop]
        print URL    

        try:
            if URL.find('imgur') != -1 and not URL.find('/a/') != -1:
                print "imgur link found"
                tempUrl = URL.split('.')
                URL = tempUrl[0]
                for x in range(1, len(tempUrl)-1):
                    URL = URL + '.' + tempUrl[x]
            soup = BeautifulSoup(urllib2.urlopen(URL).read())
            title = soup.title.contents[0]
            return title.lstrip().encode("utf-8")
        except:
            return "No title for URL: " + URL + " was found"