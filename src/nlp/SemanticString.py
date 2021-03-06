import itertools
import string

import SemanticWord as sw
import numpy as np

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from pprint import pprint
from termcolor import colored

# Take out 0-freq base words

READ = 'rb'
# stopwords = open('./data/stopwords',READ).readlines()
stopwords = open('./data/stopwords',READ).readlines()
stopwords = [stopword.rstrip('\r\n') for stopword in stopwords]

bad_words = open('./data/words_0freq.txt',READ).readlines()

punctuation = set(string.punctuation) #Can make more efficient with a translator table

class SemanticString(object):
	def __init__(self,text,db,kernel):
		self.text = text
		self.db=db
		self.kernel = kernel
		self.tokens = [sw.SemanticWord(token,part_of_speech,self.db,self.kernel) 
						for token,part_of_speech in pos_tag(word_tokenize(text))
						if token not in punctuation and token not in (stopwords + bad_words)]			
		self.tokens = filter(lambda token: not token.orphan,self.tokens)

		self.synsets = [token.synset for token in self.tokens]
	def __len__(self):
		return len(filter(None,self.synsets)) if len(filter(None,self.synsets)) > 0 else None

	def __sub__(self,other):
		if self.text == other.text:
			return 0
		else:
			distances = np.array(filter(None,[self.tokens[i] - other.tokens[j] 
								for i in xrange(len(self.tokens)) for j in xrange(len(other.tokens))]))
			distances = distances[~np.isnan(distances)]
			#TEST
			print "All word-pair distances: ", distances
			print "Average distance between two tweets:", np.average(distances) if distances != [] else None
			#DONE
		return np.average(distances) if distances != [] else None

	def __repr__(self):
		return  '%s--> %s'%(colored(self.text,'red'),colored(' '.join(filter(None,[token.word for token in self.tokens])),'green'))

	def lemma(self):
		return ' '.join([token.word for token in self.tokens])

