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

	def __init__(self,word,part_of_speech,lookuptable,kernel):
		self.part_of_speech = morphy_tag[part_of_speech] if part_of_speech in morphy_tag else wordnet.NOUN
		self.word = wordnet.morphy(word,self.part_of_speech) #Lemmatization
		self.db = lookuptable
		self.kernel = kernel
		self.in_kernel = True if self.word in self.kernel else False

		self.synset = listify(wordnet.synsets(word,pos=self.part_of_speech)) if self.word else None
		self.orphan = not self.synset

		if self.synset and self.in_kernel:
			accounted,new_synset = ([],[])
			for synset in self.synset:
				if get_synset_name(synset) not in accounted:
					new_synset.append(synset)
					accounted.append(get_synset_name(synset))
			self.synset = new_synset

	# def lookup(self,other):
	# 	#construct query
	# 	query = '%s-%s'%(self.word,other.word)
	# 	if query not in self.db:
	# 		transpose_query = '%s-%s'%(other.word,self.word)
	# 		if transpose_query in self.db:
	# 			self.db[query] = self.db[transpose_query]
	# 		else:
	# 			distance = filter(None,[shortest_path_distance(a,b) for a in self.synset for b in other.synset])
	# 			self.db[query] = np.average(distance) if distance != [] else None
	# 	return self.db[query]

	def lookup(self,other):
		#construct query
		query = '%s-%s'%(self.word,other.word)
		if query not in self.db:
			divisor = 1 * len(self.synset) if not self.in_kernel else 1
			divisor *= len(other.synset) if not other.in_kernel else 1
			transpose_query = '%s-%s'%(other.word,self.word)
			if transpose_query in self.db:
				self.db[query] = self.db[transpose_query]
			else:
				distance = filter(None,[shortest_path_distance(a,b,self,other,self.kernel) 
									for a in self.synset for b in other.synset])
				# print distance
				self.db[query] = np.sum(distance)/float(divisor) if distance != [] else None
		return self.db[query]

	def __sub__(self,other):
		if self.synset and other.synset and self.part_of_speech == other.part_of_speech: 
			return 0 if self.word == other.word else self.lookup(other)
		else:
			return None

	def __repr__(self):
		return 'word: %s \n sense: %s'%(self.word,pformat(self.synset) if not self.orphan else 'Not in WordNet')

def get_synset_name(synset):
	return synset.name[:synset.name.index('.')]

def shortest_path_distance(a, b, aWord, bWord, kernel, simulate_root=False):
	if a == b:
		return 0

	# print a
	# print b

	path_distance = None

	dist_list1 = a.hypernym_distances(simulate_root=simulate_root)
	dist_dict1 = {}

	dist_list2 = b.hypernym_distances(simulate_root=simulate_root)
	dist_dict2 = {}

    # Transform each distance list into a dictionary. In cases where
    # there are duplicate nodes in the list (due to there being multiple
    # paths to the root) the duplicate with the shortest distance from
    # the original node is entered.

	for (l, d) in [(dist_list1, dist_dict1), (dist_list2, dist_dict2)]:
		for (key, value) in l:
			if key in d:
				if value < d[key]:
					d[key] = value
			else:
				d[key] = value

    # For each ancestor synset common to both subject synsets, find the
    # connecting path length. Return the shortest of these.

	for synset1 in dist_dict1.keys():
		for synset2 in dist_dict2.keys():
			if synset1 == synset2:
				new_distance = dist_dict1[synset1] + dist_dict2[synset2]
				if path_distance is None or path_distance < 0 or new_distance < path_distance:
					path_distance = new_distance

	# print path_distance
	if path_distance != None:
		path_distance *= kernel[aWord.word][get_synset_name(a)] if aWord.in_kernel else 1
		path_distance *= kernel[bWord.word][get_synset_name(b)] if bWord.in_kernel else 1

	# print path_distance

	return path_distance


