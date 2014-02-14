import pickle
messages = {"^MERKLERN^":[]}
pickle.dump( messages, open ("messages.p","wb"))

def pending(nick):
	messages = pickle.load(open ("messages.p","rb"))
	if nick in messages:
		return True
	else:
		return False

def add_message(nick,sender,message):
	messages = pickle.load(open ("messages.p","rb"))
	message = "Reminder from " + sender + " to " + nick + ": " + message
	if nick in messages:
		messages[nick].append(message)
	else:
		messages[nick] = [message]
	pickle.dump( messages, open ("messages.p","wb"))

def get_messages(nick):
	messages = pickle.load(open ("messages.p","rb"))
	messagelist = messages[nick]
	del messages[nick]
	pickle.dump( messages, open ("messages.p","wb"))
	return messagelist

add_message("Gurka","Sven","Det har ar ett meddelande")
add_message("Gurka","Sven","Det har ar ett meddelande")
print pending("Gurka")
print get_messages("Gurka")
print pending("Gurka")
