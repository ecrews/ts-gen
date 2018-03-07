import sys
import pysynth
import random

sys.path.append('./lm')

from dataLoader import *
from unigramModel import *
from bigramModel import *
from trigramModel import *
from songPlayer import *


def main():
	# Load sheet music
	SOURCEDIRS = ['transcriptions']
	dl = DataLoader()
	for dir in SOURCEDIRS:
		dl.loadMusic(dir)

	# Create models
	unigrams = UnigramModel()
	bigrams = BigramModel()
	trigrams = TrigramModel()
	models = [trigrams, bigrams, unigrams]

	# Train models on sheet music
	unigrams.trainText(dl.data)
	bigrams.trainText(dl.data)
	trigrams.trainText(dl.data)

	# Build chorus, verse, bridge melodies
	VERSE_LENGTH = 9
	CHORUS_LENGTH = 6

	verse_melody = generateSentence(models, CHORUS_LENGTH)
	chorus_melody = generateSentence(models, VERSE_LENGTH)
	bridge_melody = generateSentence(models, VERSE_LENGTH)

	for i in range(3):
		chorus_melody += ' ' + generateSentence(models, CHORUS_LENGTH)
		verse_melody +=  ' ' + generateSentence(models, VERSE_LENGTH)
		bridge_melody += ' ' + generateSentence(models, VERSE_LENGTH)

	# Collect melodic fragments into song
	notes = (verse_melody + ' ' + chorus_melody + ' ') * 2 \
			+ bridge_melody + ' ' + chorus_melody
	notes =  notes.split()

	# Prep notes for PySynth
	sheet = ()
	for i in notes:
		parts = i.split('|')
		sheet += (parts[0], int(parts[1])),

	# Build audio file from notes and random tempo
	pysynth.make_wav(sheet, fn="song.wav", bpm=random.randrange(90, 155))

	SOURCEDIRS = ['taylor_swift']  # For collaborations, add to this list
	dl = DataLoader()
	for dir in SOURCEDIRS:
		dl.loadMusic(dir)
	print("Loaded Data" + '\n')

	# Clear dictionaries for lyrics
	unigrams.wordCounts.clear()
	bigrams.wordCounts.clear()
	trigrams.wordCounts.clear()

	# Train models on text
	unigrams.trainText(dl.data)
	bigrams.trainText(dl.data)
	trigrams.trainText(dl.data)

	# Build chorus
	chorus = ''
	for i in range(4):
		chorus += generateSentence(models, CHORUS_LENGTH).capitalize() + '\n'

		# Build and print lyrics - VC x 3
	for i in range(3):
		verse = ''
		# Build verse
		for i in range(4):
			verse += generateSentence(models,VERSE_LENGTH).capitalize() + '\n'

		print(verse)
		print(chorus)

	# Play song
	song_player = SongPlayer("song.wav")
	song_player.play()

def generateSentence(models, length):
	"""
	Requires: models is a list of LanguageModel objects, sorted by priority
		  For the core, the priority is trigrams, then bigrams,
		  then unigrams. length is roughly the desired length of the
		  sentence. The resulting sentence will not automatically be
		  this long, but it is likely to be close.
	Modifies: nothing
	Effects: This function takes the trained LanguageModel objects
		 and uses them to generate a sentence of a desired length.
		 Choruses have a desired length of 6, verses of 9 for the Core.
		 To do this, it must generate several words using the
		 procedure described in the spec.
		 Returns a string representing the sentence.
	"""
	sentence = "^::^ ^:::^"  # These are always our starting symbols
	current_length = 2
	next_token = ''

	while not over(length, current_length) and next_token != '$:::$':
		model = backOff(models, sentence)
		next_token = model.nextToken(sentence)

		# Don't do anything if end of sentence
		if next_token != '$:::$':
			sentence += ' ' + next_token
			current_length += 1

	return sentence[11:]


def backOff(models, sentence):
	"""
	Requires: models is a list of LanguageModel objects. It is sorted
		  by descending priority, meaning tri-, then bi-, then unigrams
	Modifies: nothing
	Effects: Selects the best (first) possible model that can be used.
		 If the models list were [A,B], it would first see if A
		 has any knowledge that can be used for the current sentence
		 if so, it returns A. If not, it checks if B applies.
		 It is recommended you use the hasKey() method of each model.

		 Returns None if no models are usable.
	"""
	if models[0].hasKey(sentence):
		# Use trigram model
		return models[0]
	elif models[1].hasKey(sentence):
		# Use bigram model
		return models[1]
	elif models[2].hasKey(sentence):
		# Use unigram model
		return models[2]
	return None



def over(maxLength, currentLength):
	"""
	Requires: length is (roughly) the maximum desired length of the sentence
		This function ends the sentence at close to length number
		of words with some random variation to make it seem
		more natural.
		SentenceLength is the length of the current sentence so far
	Modifies: Nothing
	Effects: Returns a boolean of whether or not to end the sentence
		based solely on length.
		Also, this is already done for you.
		Please do not change this for the core
		true is done, false needs more words
	"""
	STDEV = 1  # This must be 1 for the core
	val = random.gauss(currentLength, STDEV)
	return val > maxLength


if __name__ == '__main__':
	main()
