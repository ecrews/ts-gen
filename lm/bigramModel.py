from languageModel import *

class BigramModel(LanguageModel):
    def __init__(self):
        super(BigramModel, self).__init__()

    def __str__(self):
        return "This is a bigram language model"

    def trainText(self, text):
        """
        Requires: text is all the text to train on,
              a list of full-sentence strings
        Modifies: self.wordCounts, a 2D dictionary
              This model is one level more complicated
              than the UnigramModel. This model counts how
              often each word appears AFTER each other word.

        Effects: nothing
        """
        # Build word list
        words = ' '.join(self.prepText(text)).split(' ')

        # Build bigram frequency list
        for i in range(len(words) - 1):
            # Get first, second part of bigram
            first = words[i]
            second = words[i + 1]

            # Initialize empty dictionaries for new bigrams
            self.wordCounts.setdefault(first, {})
            if second in self.wordCounts[first]:
                # Count old bigram
                self.wordCounts[first][second] += 1
            else:
                # Count new bigram
                self.wordCounts[first][second] = 1

    def nextToken(self, sentence):
        """
        Requires: sentence is the sentence so far
                          hasKey(self, sentence) == True
        Modifies: nothing
        Effects: returns the next word to be added to the sentence
        """
        # Get last word in sentence
        last = sentence.split(' ').pop()

        # Weigh words in word_roulette according to frequency
        cumulative_count = 0
        word_roulette = {}
        for word in self.wordCounts[last]:
            cumulative_count += self.wordCounts[last][word]
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
             for this sentence. For a bigram model, this is True
             as long as the model has seen the last word
             in the sentence before at the start of a bigram.
        """
        words = sentence.split(' ')
        return words.pop() in self.wordCounts
        