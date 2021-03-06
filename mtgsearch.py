# -*- coding: utf-8 -*-

import json
from lxml import html
import requests


def card_search(name):
    with open('AllCards-x.json') as data_file:
        carddata = json.load(data_file)

    with open('AllSets-x.json') as data_file:
        cardsetlist = json.load(data_file)

    name = carddata[name]['name']
    setname = carddata[name]['printings'][0]
    set = cardsetlist[setname]

    try:
        print 'Getting multiverseid'
        for card in set['cards']:
            if card['name'] == name:
                multiverseid = card['multiverseid']
                break
    except KeyError:
        print 'KeyError while getting id'
        setname = carddata[name]['printings'][1]
        set = cardsetlist[setname]
        for card in set['cards']:
            if card['name'] == name:
                multiverseid = card['multiverseid']
                break

    full_setname = set['name']
    cardinfo = name + ' : http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=' + str(multiverseid)
    return [cardinfo, full_setname]


def card_price(name, expansion):
    set = expansion.replace(' ', '+')
    mcm_url = 'https://www.magiccardmarket.eu/Products/Singles/' + set + '/' + name

    page = requests.get(mcm_url)
    tree = html.fromstring(page.text)

    price_low = tree.xpath(u'//*[@id="ProductInformation"]/div/div[1]/div[1]/table/tbody/tr[2]/td[2]/span[1]')[0].text
    price_avg = tree.xpath(u'//*[@id="ProductInformation"]/div/div[1]/div[1]/table/tbody/tr[3]/td[2]')[0].text
    try:
        price_foil = tree.xpath(u'//*[@id="ProductInformation"]/div/div[1]/div[1]/table/tbody/tr[5]/td[2]')[0].text
    except:
        price_foil = u'N/A'

    price_message = name + ' > From: ' + price_low + u' € Avg: ' + price_avg + ' Foil: ' + price_foil + '\r'

    return price_message
