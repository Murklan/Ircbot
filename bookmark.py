import cPickle as pickle


def create_bookmark(key, bookmark):
    try:
        with open('bookmarks', 'rb') as f:
            bookmarkdict = pickle.load(f)
    except EOFError:
        bookmarkdict = {}

    bookmarkdict[key] = bookmark

    with open('bookmarks', 'wb') as f:
        pickle.dump(bookmarkdict, f)

    return "Bookmark '" + key + "' for the URL '" + bookmark + "' created sucessfully"


def get_bookmark(key):
    try:
        with open('bookmarks', 'rb') as f:
            bookmarkdict = pickle.load(f)

        return "URL: " + bookmarkdict[key.lower()]
    except:
        return "Bookmark does not exist, create it by typing: '!bm " + key + "'"


def delete_bookmark(key):
    try:
        with open('bookmarks', 'rb') as f:
            bookmarkdict = pickle.load(f)
        tempdict = dict(bookmarkdict)
        del tempdict[key]

        with open('bookmarks', 'wb') as f:
            pickle.dump(tempdict, f)

        return "Bookmark sucessfully deleted."
    except:
        return "The bookmark '" + key + "' does not exist."


def list_bookmark():
    try:
        with open('bookmarks', 'rb') as f:
            bookmarkdict = pickle.load(f)

        dictkeys = list(bookmarkdict.keys())

        return "Available bookmarks: " + '%s' % ', '.join(map(str, dictkeys))
    except:
        return "Yeah... something went wrong here... :("
