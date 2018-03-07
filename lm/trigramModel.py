from languageModel import *

class TrigramModel(LanguageModel):

	def __init__(self):
		super(TrigramModel, self).__init__()

	def __str__(self):
		"""
		If you try to print a TrigramModel object
		this is the string that prints
		"""
		return "This is a trigram language model"

	def trainText(self, text):
		"""
		Requires: text is all the text to train on,
			  a list of full-sentence strings
		Modifies: self.wordCounts, a 3D dictionary
			  This model is one level more complicated than
			  the BigramModel. This model counts 3-word phrases
			  instead of 2-word phrases like the BigramModel did.

		Effects: Nothing
		"""

		# Build word list
		words = ' '.join(self.prepText(text)).split(' ')

		# Build trigram frequency list
		for i in range(len(words) - 2):
			# Get first, second, and third parts of trigram
			first = words[i]
			second = words[i + 1]
			third = words[i + 2]

			# Initialize empty dictionaries for new trigrams
			self.wordCounts.setdefault(first, {})
			self.wordCounts[first].setdefault(second, {})

			if third in self.wordCounts[first][second]:
				# Count old trigram
				self.wordCounts[first][second][third] += 1
			else:
				# Count new trigram
				self.wordCounts[first][second][third] = 1

	def nextToken(self, sentence):
		"""
		Requires: sentence is the sentence so far
			  hasKey(self, sentence) == True
		Modifies: nothing
		Effects: returns the next word to be added to the sentence

		"""
		words = sentence.split(' ')
		second = words.pop()
		first = words.pop()

		cumulative_count = 0
		word_roulette = {}
		# Weigh words in word_roulette according to frequency
		for word in self.wordCounts[first][second]:
			cumulative_count += self.wordCounts[first][second][word]
			word_roulette[cumulative_count] = word

		# Get random word from word roulette
		key = 1
		# Generate key if more than one choice
		if cumulative_count > 1:
			key = random.randrange(1, cumulative_count)
			while key not in word_roulette:
				key += 1

		return word_roulette[key]

	def hasKey(self, sentence):
		"""
		Requires: sentence is the sentence so far
		Modifies: nothing
		Effects: Returns True iff this language model can be used
			 for this sentence. For a trigram model, this is True
			 as long as the model as seen the last two words
			 together before.
		"""
		words = sentence.split(' ')
		second = words.pop()
		first = words.pop()
		return first in self.wordCounts and second in self.wordCounts[first]
