import wolframalpha
client = wolframalpha.Client("6L26HY-PHR2XXGER9")

def ask_wolfram(phrase):
	res = client.query(phrase)
	print next(res.results).text