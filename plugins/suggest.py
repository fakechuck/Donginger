
import json
from plugin import Plugin
from random import choice

class Suggest(Plugin):
	def __init__(self, dong, conf):
		super(Suggest, self).__init__(dong, conf)
		
	def google_suggest(self, callback, who, arg, store=True):
		"""<suggest string> - returns a random Google Suggestion based on the string."""
		
		sugs = self.get_xml('http://google.com/complete/search', {'output':'toolbar', 'q': arg})

		if sugs is not None:
			try:
				sugs = [x[0].get('data') for x in suggestions]
			except Exception, e:
				print "XML error with Google Suggest: %s" % e
			
			suggestions = self.remove_lyrics(sugs)
			random_sug = choice(suggestions)
			
			# Same string as we started with - roll again
			if random_sug == arg:
				try:
					suggestions.pop(suggestions.index(random_sug))
				except:
					pass
				random_sug = choice(suggestions)
				
			if random_sug is not None:
				if store:
					self.store_suggestion(who, arg)
				return random_sug
			
	def remove_lyrics(self, sug):
		filtered_list = []
		for s in sug:
			if s[0].find('lyrics') > -1: pass
			else: filtered_list.append(s[0])
		return filtered_list
	
	def store_suggestion(self, who, sug):
		sug = sug.strip('\r')
		sug = sug.strip()
		
		try:
			self.dong.db.insert('suggest', {'user': who, 'suggestion': sug})
		except:
			# UNIQUE constraint will balk here
			pass
		
	def pull_suggestion(self, callback, who, arg):
		"""Nudging the bot makes it return a random Google suggestion."""
		
		random_sug = self.dong.db.get_random_row('suggest')
		res = self.google_suggest(callback, who, random_sug[2], False)
		
		w = res.split()
		if w[0] in ('what', 'why', 'was', 'where', 'who', 'which', 'whom', 'when', 'how', 'is', 'are', 'did'):
			res = res + '?'
		return res.capitalize()

	
