
import json
from plugin import Plugin

class Twit(Plugin):
	def __init__(self, name, dong):
		super(Twit, self).__init__(name, dong)
		
	def google_suggest(self, who, str):
		w = self.build_query('http://google.com/complete/search', {'q': str})
		page = w.read()
		page_json = page.split('(', 1)[1][:-1]
		suggestions = json.loads(page_json)[1]
		if suggestions:
			suggestions = self.removeLyrics(suggestions)
			random_sug = random.choice(suggestions)
			self.storeSug(who, inp)
			return random_sug
			
	def removeLyrics(self, sug):
		nyt = []
		for s in sug:
			if s[0].find('lyrics') > -1: pass
			else: nyt.append(s)
		return nyt
	
	def storeSug(self, sug):
		sug = sug.strip('\r')
		sug = sug.strip()
		
		try:
			self.dong.db.insert('suggest', {'user': who, 'suggestion': sug})
		except:
			# UNIQUE constraint will balk here
			pass
		
	def pullSug(self):
		random_sug = self.dong.db.get_random_row('suggest')
		res = self.GoogleSuggest(random_sug)
		return res

	
