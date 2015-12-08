# -*- coding: utf-8 -*-

import json
import urllib2
from lxml import html
import requests


def cardSearch(name):

    searchUrl = 'http://api.mtgdb.info/cards/' + name

    cardData = json.load(urllib2.urlopen(searchUrl))
    cardName = cardData[0]['name']
    cardInfo = cardName + ' : http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=' + str(cardData[0]['id'])
    cardSet = cardData[0]['cardSetName']   
    return [cardName, cardInfo, cardSet]



def cardPrice(cardName, expansion):

	cardSet = expansion.replace(' ', '+')
	page = requests.get('https://www.magiccardmarket.eu/Products/Singles/' + cardSet + '/' + cardName)
	tree = html.fromstring(page.text)
	
	priceFrom = tree.xpath(u'//*[@id="ProductInformation"]/div/div[1]/div[1]/table/tbody/tr[2]/td[2]/span[1]')[0].text
	priceAvg = tree.xpath(u'//*[@id="ProductInformation"]/div/div[1]/div[1]/table/tbody/tr[3]/td[2]')[0].text
	try:
		priceFoil = tree.xpath(u'//*[@id="ProductInformation"]/div/div[1]/div[1]/table/tbody/tr[5]/td[2]')[0].text
	except:
		priceFoil = u'N/A'
	return [priceFrom, priceAvg, priceFoil]
