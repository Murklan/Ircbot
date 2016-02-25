# -*- coding: utf-8 -*-

import json
import urllib2
from lxml import html
import requests


def card_search(name):
    carddata = json.load(urllib2.urlopen('http://mtgjson.com/json/AllCards-x.json'))
    cardsetlist = json.load(urllib2.urlopen('http://mtgjson.com/json/AllSets.json'))

    name = carddata[name]['name']
    setname = carddata[name]['printings'][0]
    set = cardsetlist[setname]
    print setname

    try:
        print 'Getting multiverseid'
        for card in set['cards']:
            if card['name'] == name:
                multiverseid = card['multiverseid']
                print multiverseid
                break
    except KeyError:
        print 'KeyError while getting id'
        setname = carddata[name]['printings'][1]
        set = cardsetlist[setname]
        print setname
        for card in set['cards']:
            if card['name'] == name:
                multiverseid = card['multiverseid']
                print multiverseid
                break

    full_setname = set['name']
    print full_setname
    cardinfo = name + ' : http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=' + str(multiverseid)
    print cardinfo
    return [cardinfo, full_setname]


def card_price(name, expansion):
    set = expansion.replace(' ', '+')
    print set
    mcm_url = 'https://www.magiccardmarket.eu/Products/Singles/' + set + '/' + name
    print mcm_url

    page = requests.get(mcm_url)
    tree = html.fromstring(page.text)

    price_low = tree.xpath(u'//*[@id="ProductInformation"]/div/div[1]/div[1]/table/tbody/tr[2]/td[2]/span[1]')[0].text
    price_avg = tree.xpath(u'//*[@id="ProductInformation"]/div/div[1]/div[1]/table/tbody/tr[3]/td[2]')[0].text
    try:
        price_foil = tree.xpath(u'//*[@id="ProductInformation"]/div/div[1]/div[1]/table/tbody/tr[5]/td[2]')[0].text
    except:
        price_foil = u'N/A'

    price_message = name + ' > From: ' + price_low + u' € Avg: ' + price_avg + ' Foil: ' + price_foil + '\r'
    print price_message

    return price_message
