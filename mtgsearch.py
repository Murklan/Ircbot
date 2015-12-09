# -*- coding: utf-8 -*-

import json
import urllib2
from lxml import html
import requests


def cardSearch(cardname):

	cardData = json.load(urllib2.urlopen('http://mtgjson.com/json/AllCards-x.json'))
	cardSetList = json.load(urllib2.urlopen('http://mtgjson.com/json/AllSets.json'))

	cardName = cardData[cardname]['name']
	cardSetName = cardData[cardname]['printings'][0]
	cardSet = cardSetList[cardSetName]
	print cardSetName

	try:
		print 'Getting multiverseid'
		for card in cardSet['cards']:
			if card['name'] == cardname:
				cardMultiverseId = card['multiverseid']
				print cardMultiverseId
				break
	except KeyError:
		print 'KeyError while getting id'
		cardSetName = cardData[cardname]['printings'][1]
		cardSet = cardSetList[cardSetName]
		print cardSetName
		for card in cardSet['cards']:
			if card['name'] == cardname:
				cardMultiverseId = card['multiverseid']
				print cardMultiverseId
				break

	cardSetNameFull = cardSet['name']
	print cardSetNameFull
	cardInfo = cardName + ' : http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=' + str(cardMultiverseId)
	print cardInfo
	return [cardInfo, cardSetNameFull]

def cardPrice(cardname, expansion):

	print 'Getting Price of ' + cardname + ' in ' + expansion
    searchUrl = 'http://api.mtgdb.info/cards/' + name

    cardData = json.load(urllib2.urlopen(searchUrl))
    cardName = cardData[0]['name']
    cardInfo = cardName + ' : http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=' + str(cardData[0]['id'])
    cardSet = cardData[0]['cardSetName']   
    return [cardName, cardInfo, cardSet]



def cardPrice(cardName, expansion):

>>>>>>> master
	cardSet = expansion.replace(' ', '+')
	page = requests.get('https://www.magiccardmarket.eu/Products/Singles/' + cardSet + '/' + cardname)
	tree = html.fromstring(page.text)
	
	priceFrom = tree.xpath(u'//*[@id="ProductInformation"]/div/div[1]/div[1]/table/tbody/tr[2]/td[2]/span[1]')[0].text
	priceAvg = tree.xpath(u'//*[@id="ProductInformation"]/div/div[1]/div[1]/table/tbody/tr[3]/td[2]')[0].text
	try:
		priceFoil = tree.xpath(u'//*[@id="ProductInformation"]/div/div[1]/div[1]/table/tbody/tr[5]/td[2]')[0].text
	except:
		priceFoil = u'N/A'

	priceMessage = cardName + ' > From: ' + priceFrom + u' € Avg: ' + priceAvg + ' Foil: ' + priceFoil + '\r'
	print priceMessage

	return priceMessage

