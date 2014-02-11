from pygoogle import pygoogle


def googleSearch(searchString):
	
	g = pygoogle(searchString)
	g.pages = 1
	results = g.get_urls()
	try:
		return results[0]
	except:
		return "That was not the word you're looking for"