import numpy as np

from nltk.corpus import wordnet
from src.nlp.SemanticString import SemanticString
from src.nlp.SemanticWord import SemanticWord

strings = ['hall change', 'coffee mug']

string_distance = SemanticString(strings[0], {}) - SemanticString(strings[1], {})

#'NN':wordnet.NOUN,'JJ':wordnet.ADJ,'VB':wordnet.VERB,'RB':wordnet.ADV

words1 = [SemanticWord(word, wordnet.NOUN, {}) for word in ['hall', 'change']]
words2 = [SemanticWord(word, wordnet.NOUN, {}) for word in ['coffee', 'mug']]

for w1 in words1:
	for w2 in words2:
		print 'Distance between', w1.word, 'and', w2.word, 'is:', w1-w2

distances = [(w1 - w2) for w1 in words1 for w2 in words2]

avg_distance = np.average(distances)

print 'Hand-calculated distance is:', avg_distance
print 'SemanticString distance is:', string_distance

for word in words1+words2:
	print word.word + ':', word.synset




