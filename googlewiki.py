from pygoogle import pygoogle


def google_search(search_string):
    g = pygoogle(search_string)
    g.pages = 1
    results = g.get_urls()
    try:
        return results[0]
    except:
        return "That was not the word you're looking for"
