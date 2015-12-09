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
		for card in cardSet['cards']:
			if card['name'] == cardname:
				cardMultiverseId = card['multiverseid']
				print multiverseid
				break
	except KeyError:
		cardSetName = cardData[cardname]['printings'][1]
		for card in cardSet['cards']:
			if card['name'] == cardname:
				cardMultiverseId = card['multiverseid']
				print multiverseid
				break

	cardSetNameFull = cardSet['name']
	print cardSetName
	cardInfo = cardName + ' : http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=' + str(cardMultiverseId)

	return [cardName, cardInfo, cardSetNameFull]

def cardPrice(cardname, expansion):

	cardSet = expansion.replace(' ', '+')
	page = requests.get('https://www.magiccardmarket.eu/Products/Singles/' + cardSet + '/' + cardname)
	tree = html.fromstring(page.text)

	priceFrom = tree.xpath(u'//*[@id="siteContents"]/div/div[3]/div[1]/div[2]/table/tbody/tr[2]/td[2]/span[1]')[0].text
	priceAvg = tree.xpath(u'//*[@id="siteContents"]/div/div[3]/div[1]/div[2]/table/tbody/tr[3]/td[2]')[0].text
	try:
		priceFoil = tree.xpath(u'//*[@id="siteContents"]/div/div[3]/div[1]/div[2]/table/tbody/tr[5]/td[2]')[0].text
	except:
		priceFoil = u'N/A'
	return [priceFrom, priceAvg, priceFoil]