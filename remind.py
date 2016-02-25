import pickle

messages = {"^MERKLERN^": []}
pickle.dump(messages, open("messages.p", "wb"))
senders = {"^MERKLKERN^": []}
pickle.dump(senders, open("senders.p", "wb"))


def pending(nick):
    messages = pickle.load(open("messages.p", "rb"))
    if nick in messages:
        return True
    else:
        return False


def add_message(nick, sender, message):
    messages = pickle.load(open("messages.p", "rb"))
    senders = pickle.load(open("senders.p", "rb"))
    if nick not in senders or sender not in senders[nick]:
        if nick in senders:
            senders[nick].append(sender)
        else:
            senders[nick] = [sender]
        message = "Reminder from " + sender + " to " + nick + ": " + message
        if nick in messages:
            messages[nick].append(message)
        else:
            messages[nick] = [message]
        pickle.dump(messages, open("messages.p", "wb"))
        pickle.dump(senders, open("senders.p", "wb"));
        return True
    else:
        return False


def get_messages(nick):
    messages = pickle.load(open("messages.p", "rb"))
    senders = pickle.load(open("senders.p", "rb"))
    messagelist = messages[nick]
    del messages[nick]
    del senders[nick]
    pickle.dump(messages, open("messages.p", "wb"))
    pickle.dump(senders, open("senders.p", "wb"));
    return messagelist
