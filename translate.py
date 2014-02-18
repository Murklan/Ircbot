import goslate
gs = goslate.Goslate()

#Usage is quite obvious
def translate(phrase,lang):
	try:
		return gs.translate(phrase,lang)
	except:
		return "Translation failed"