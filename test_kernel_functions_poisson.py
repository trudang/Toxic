import numpy as np
import itertools
import copy
import matplotlib.pyplot as plt
import pylab as P

from nltk.corpus import wordnet
from src.nlp.SemanticString import SemanticString
from src.nlp.SemanticWord import SemanticWord

words = ['rest', 'hold']

print "Words used:", words

senses = [list(set([sense.name[:sense.name.index('.')] for sense in SemanticWord(word,'NN',{}).synset])) for word in words]

all_senses = np.sum(senses)

print "List of unique senses:", all_senses

# freq = [list(np.random.poisson(100,len(sense))) for sense in senses]
freq = [[91, 96, 103], [100, 108, 107, 93, 100, 104, 97]]

print freq

all_freq = np.sum(freq)

print "List of frequencies:", all_freq
print "Total frequencies:", sum(all_freq)

expected_kernel = {word: dict(zip(senses[i], freq[i])) for i,word in enumerate(words)}

print "Expected kernel:"
print expected_kernel

corpus = [all_senses[i] for i in xrange(len(all_senses)) for n in xrange(all_freq[i])]

def make_freq_dict(word_list, corpus):
	senses = [list(set([sense.name[:sense.name.index('.')] for sense in SemanticWord(word,'NN',{}).synset])) for word in words]
	freq = [list(np.zeros(len(sense))) for sense in senses]
	dic = {word: dict(zip(senses[i], freq[i])) for i,word in enumerate(words)}
	for element in corpus:
		for word in dic.keys():
			if element in dic[word].keys():
				dic[word][element] += 1
	return dic

def normalize_control(dic):
	new_dic = copy.deepcopy(dic)
	sum_of_dic = float(sum(np.sum([word.values() for word in dic.values()])))
	for word in new_dic:
		for sense in new_dic[word]:
			new_dic[word][sense] /= sum_of_dic
	return new_dic

def normalize_dict(dic):
	words = dic.keys()
	senses = [dic[word].keys() for word in dic.keys()]
	values = [dic[word].values() for word in dic.keys()]
	sum_of_dic = sum(np.sum(values))
	new_values = [list(np.array(v) / float(sum_of_dic)) for v in values]
	return {word: dict(zip(senses[i], new_values[i])) for i,word in enumerate(words)}

def histogram(kernel):
	words = kernel.keys()
	senses = [kernel[word].keys() for word in kernel.keys()]
	values = [kernel[word].values() for word in kernel.keys()]
	fig = plt.figure()
	n, bins, patches = plt.hist(values, 5, 
		#normed=True, 
		histtype='bar', label=words)
	plt.xlabel("Frequency of Sense")
	plt.ylabel("Number of Senses with Same Frequency")
	plt.legend()
	plt.show()

kernel = make_freq_dict(words, corpus)

print "Actual kernel:"
print kernel

print "Actual kernel is same as expected:", kernel == expected_kernel

sum_kernel = sum(np.sum([word.values() for word in kernel.values()]))

print "Total frequencies:", sum_kernel, "; Same as expected:", sum_kernel == sum(all_freq)

print "Positive control normalization:"
control_norm = normalize_control(kernel)
print control_norm

print "Normalization with dict as input:"
dict_norm = normalize_dict(kernel)
print dict_norm

print "Normalization works?", dict_norm == control_norm

print "Total of values in normalized kernel:", sum(np.sum([word.values() for word in dict_norm.values()]))

histogram(kernel)