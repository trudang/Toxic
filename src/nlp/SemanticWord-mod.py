import itertools
import string
import json

import numpy as np

from nltk.corpus import wordnet

from pprint import pformat
from termcolor import colored

morphy_tag = {'NN':wordnet.NOUN,'JJ':wordnet.ADJ,'VB':wordnet.VERB,'RB':wordnet.ADV}
listify = lambda item: item if type(item) == type([]) and item != None else list(item)


class SemanticWord(object):

	def __init__(self,word,part_of_speech,lookuptable):
		self.part_of_speech = morphy_tag[part_of_speech] if part_of_speech in morphy_tag else wordnet.NOUN
		self.word = wordnet.morphy(word,self.part_of_speech) #Lemmatization

		self.synset = listify(wordnet.synsets(word,pos=self.part_of_speech)) if self.word else None
		self.orphan = not self.synset
		self.db = lookuptable

	def lookup(self,other):
		#construct query
		query = '%s-%s'%(self.word,other.word)
		if True:
		# if query not in self.db:
			transpose_query = '%s-%s'%(other.word,self.word)
			if False:
				pass
			# if transpose_query in self.db:
			# 	self.db[query] = self.db[transpose_query]
			else:
                                combinations = filter(None,[((a.name,b.name),1/2.*a.path_similarity(b)* b.path_similarity(a))
							for a,b in itertools.combinations(self.synset+other.synset,2)])
                                print combinations
                                similarity = np.average(filter(None,[comb[1] for comb in combinations]))
##				similarity = np.average(filter(None,[a,b,a.path_similarity(b) 
##							for a,b in itertools.combinations(self.synset+other.synset,2)]))
				distance = 1-similarity if similarity else None #But now None means both no distance and not found
				# self.db[query] = distance
		print "Words being compared: ", query, "; Distance: ", distance, "\n"
		return distance
		# return self.db[query]


	def __sub__(self,other):
		if self.synset and other.synset and self.part_of_speech == other.part_of_speech: 
			return 0 if self.word == other.word else self.lookup(other)
		else:
			return None

	def __repr__(self):
		return 'word: %s \n sense: %s'%(self.word,pformat(self.synset) if not self.orphan else 'Not in WordNet')

