# -*- coding: utf-8 -*-

import json
import urllib2
from lxml import html
import requests


def cardSearch(name):

    cardData = json.load(urllib2.urlopen('http://mtgjson.com/json/AllCards-x.json'))
    cardSet = json.load(urllib2.urlopen('http://mtgjson.com/json/AllSets.json'))

    print cardData[cardname]

    print cardData[cardname]['name']

    cardName = cardData[cardname]['name']

    print cardData[cardname]['printings'][0]

    return cardName

    # cardName = 'http://api.mtgdb.info/cards/' + name

    # cardData = json.load(urllib2.urlopen(searchUrl))
    # cardName = cardData[0]['name']
    # cardInfo = cardName + ' : http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=' + str(cardData[0]['id'])
    # cardSet = cardData[0]['cardSetName']   

    # return [cardName, cardInfo, cardSet]



def cardPrice(cardName, expansion):


	cardSet = expansion.replace(' ', '+')
	page = requests.get('https://www.magiccardmarket.eu/Products/Singles/' + cardSet + '/' + cardName)
	tree = html.fromstring(page.text)

	priceFrom = tree.xpath(u'//*[@id="siteContents"]/div/div[3]/div[1]/div[2]/table/tbody/tr[2]/td[2]/span[1]')[0].text
	priceAvg = tree.xpath(u'//*[@id="siteContents"]/div/div[3]/div[1]/div[2]/table/tbody/tr[3]/td[2]')[0].text
	try:
		priceFoil = tree.xpath(u'//*[@id="siteContents"]/div/div[3]/div[1]/div[2]/table/tbody/tr[5]/td[2]')[0].text
	except:
		priceFoil = u'N/A'
	return [priceFrom, priceAvg, priceFoil]

while(True):
	cardname = raw_input()
	cardSearch(cardname)