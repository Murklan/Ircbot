import praw
from random import randint

class RedditCheck:

    def __init__(self):
        self.reddit = praw.Reddit(user_agent='just a simple irc bot')


    #!firstpost <sub>(optional), gets the first post from <sub> (defaults to /all)
    def redditFirst(self, subreddit):
        try:
            sub = subreddit
            firstposts = self.reddit.get_subreddit(sub).get_hot(limit=1)
            for firstpost in firstposts:
                ups = str(firstpost.ups)
                downs = str(firstpost.downs)
                title = firstpost.title
                url = firstpost.url
            return '\x02Top post from ' + sub + ': \x02(\x037 ' + ups + '\x03 |\x032 ' + downs +'\x03 ) - \x034' +  title  + '\x03 - ' + url
        except:
            return "That subreddit probably doesn't exist :("
    
    def redditRandom(self, subreddit):
        try:
            sub = subreddit
            randomposts = self.reddit.get_subreddit(sub).get_hot(limit=100)
            for x in range (0, randint(1, 100)):
                randompost = next(randomposts)
            return '\x02Random post from ' + sub + ': \x02(\x037 ' + str(randompost.ups) + '\x03 |\x032 ' + str(randompost.downs) +'\x03 ) - \x034' +  randompost.title  + '\x03 - ' + randompost.url
        except:
            return "That subreddit probably doesn't exist :("
