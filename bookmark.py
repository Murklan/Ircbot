import cPickle as pickle

def createBookmark(key, bookmark):
	try:
		with open('bookmarks', 'rb') as f:
		    bookmarkDict = pickle.load(f)
	except EOFError:
		bookmarkDict = {}

	bookmarkDict[key] = bookmark		


	with open('bookmarks', 'wb') as f:
		pickle.dump(bookmarkDict, f)

	return "Bookmark '" + key + "' for the URL '" + bookmark + "' created sucessfully"


def getBookmark(key):
	try:
		with open('bookmarks', 'rb') as f:
			bookmarkDict = pickle.load(f)

		return "URL: " + bookmarkDict[key.lower()]
	except:
		return "Bookmark does not exist, create it by typing: '!bm " + key + "'"

def deleteBookmark(key):
	try:
		with open('bookmarks', 'rb') as f:
			bookmarkDict = pickle.load(f)
		tempDict = dict(bookmarkDict)
		del tempDict[key]

		with open('bookmarks', 'wb') as f:
			pickle.dump(tempDict, f)

		return "Bookmark sucessfully deleted." 
	except:
		return "The bookmark '" + key + "' does not exist."

def listBookmarks():
	try:
		with open('bookmarks', 'rb') as f:
			bookmarkDict = pickle.load(f)

		dictKeys = list(bookmarkDict.keys())

		return "Available bookmarks: " + '%s' % ', '.join(map(str, dictKeys)) 
	except:
		return "Yeah... something went wrong here... :("