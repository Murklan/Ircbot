import wolframalpha, botvariables

client = wolframalpha.Client(botvariables.wolfram)

def ask_wolfram(phrase):
	res = client.query(phrase)
	try:
		return next(res.results).text
	except:
		return "No results fround"