from bs4 import BeautifulSoup
import urllib2


def get_url_title(data):
    start = data.find('http')
    stop = data.find(' ', start)
    if stop == -1:
        stop = len(data)
    url = data[start:stop]

    if url.find('i.imgur') != -1 and not url.find('/a/') != -1:
        url = fix_imgur_url(url)
        if return_title(url).find('the simple image sharer') != -1:
            return 'That Imgur link does not seem to have a proper title'
        return return_title(url)
    else:
        if url.find('twitch.tv') != -1:
            return get_twitch_title(url)

        return return_title(url)


def get_twitch_title(URL):
    nomnom = get_soup(URL)
    stream_title = nomnom.findAll(attrs={'property': 'og:description'})
    streamer = nomnom.findAll(attrs={'property': 'og:title'})

    title = 'Twitch > ' + streamer[0]['content'] + ' - ' + stream_title[0]['content']
    return title


def fix_imgur_url(url):
    tempurl = url.split('.')
    url = tempurl[0]
    url = 'http://' + tempurl[1] + '.' + tempurl[2]
    return url


def return_title(url):
    try:
        soup = get_soup(url)
        title = soup.title.contents[0]
        return 'URL > ' + title.lstrip().encode("utf-8")
    except:
        return "Couldn't find a proper title and/or something went wrong :("


def get_soup(url):
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    return soup
