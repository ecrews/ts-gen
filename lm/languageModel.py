import random

class LanguageModel(object):

	def __init__(self):
		self.wordCounts = {}

	def __str__(self):
		s = "This should never print.\n"
		s += "Please use a real language model."
		return s

	def prepText(self, text):
		"""
		Requires: Text is a list of full-sentence strings
		Modifies: Nothing
		Effects: Returns a copy of text where each sentence
			 starts with the words "^::^ ^:::^"
			 and ends with "$:::$"
		"""
		return ['^::^ ^:::^ ' + sentence + ' $:::$' for sentence in text]

	def nextToken(self, sentence):
		"""
		Requires: sentence is the current sentence so far
		Modifies: nothing
		Effects: Chooses the next word to add to the sentence
			 This is already done because it will never be used
			 All other language models have a better version
			 of this for you to write
		"""
		return random.choice(self.wordCounts.keys())

	def hasKey(self, sentence):
		"""
		Requires: sentence is the current sentence so far
		Modifies: nothing
		Effects: Returns a boolean of whether or not this
			 language model can be used for the current sentence.
		"""
		return False
