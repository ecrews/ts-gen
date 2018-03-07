from languageModel import *

class UnigramModel(LanguageModel):
	def __init__(self):
		super(UnigramModel, self).__init__()

	def __str__(self):
		"""
		If you try to print a UnigramModel object,
		this is the string that prints
		"""
		return "This is a unigram language model"

	def trainText(self, text):
		"""
		Requires: text is all the text to train on,
			  a list of full-sentence strings
		Modifies: self.wordCounts, a dictionary of {word: frequency}
			  pairs. Before training, this dictionary exists
			  but it is empty. In this function we want to
			  populate it with the frequency information
			  for whatever text you are using to train.
		Effects: nothing

		Make sure to call prepText! We need the special symbols
		it introduces later
		So please count each of the three special symbols,
		"^::^", "^:::^", "$:::$" as their own words
		"""
		# Build word list
		words = ' '.join(self.prepText(text)).split(' ')

		for word in words:
			if word in self.wordCounts:
				# Count old unigram
				self.wordCounts[word] += 1
			else:
				# Count new unigram
				self.wordCounts[word] = 1


	def nextToken(self, sentence):
		"""
		Requires: sentence is the sentence so far
		Modifies: nothing
		Effects: Returns the next word to be added to the sentence

		"""
		# Build word roulette according to unigram frequency
		cumulative_count = 0
		word_roulette = {}
		for word in self.wordCounts:
			cumulative_count += self.wordCounts[word]
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
			 for this sentence. For a unigram model,
			 this is True as long as the model knows about
			 any words (i.e. has been trained at all).
		"""
		return len(self.wordCounts) > 0
