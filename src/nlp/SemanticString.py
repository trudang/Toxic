import itertools
import string

import SemanticWord as sw
import numpy as np

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from pprint import pprint
from termcolor import colored

READ = 'rb'
# stopwords = open('./data/stopwords',READ).readlines()
stopwords = open('./data/stopwords',READ).readlines()
stopwords = [stopword.rstrip('\r\n') for stopword in stopwords]

punctuation = set(string.punctuation) #Can make more efficient with a translator table

class SemanticString(object):
	def __init__(self, text,db):
		self.text = text
		self.db=db
		self.tokens = [sw.SemanticWord(token,part_of_speech,self.db) 
						for token,part_of_speech in pos_tag(word_tokenize(text))
						if token not in punctuation and token not in stopwords]			
		self.tokens = filter(lambda token: not token.orphan,self.tokens)

		self.synsets = [token.synset for token in self.tokens]
	def __len__(self):
		return len(filter(None,self.synsets)) if len(filter(None,self.synsets)) > 0 else None

	def __sub__(self,other):
		if self.text == other.text:
			return 0
		else:
			similarities = np.array(filter(None,[self.tokens[i] - other.tokens[j] 
								for i in xrange(len(self.tokens)) for j in xrange(len(other.tokens))]))
			similarities = similarities[~np.isnan(similarities)]
		return 1-np.average(similarities) if similarities != [] else None

	def __repr__(self):
		return  '%s--> %s'%(colored(self.text,'red'),colored(' '.join([token.word for token in self.tokens]),'green'))

	def lemma(self):
		return ' '.join([token.word for token in self.tokens])
