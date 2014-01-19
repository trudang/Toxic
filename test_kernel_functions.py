import numpy as np
import itertools

from nltk.corpus import wordnet
from src.nlp.SemanticString import SemanticString
from src.nlp.SemanticWord import SemanticWord

words = ['rest', 'hold']

print "Words used:", words

senses = list(set([sense.name[:sense.name.index('.')] for word in words for sense in SemanticWord(word,'NN',{}).synset]))

print "List of unique senses:", senses

# freq = np.random.randint(1,101,len(senses))
freq = [58, 28, 22, 26, 66, 83, 34, 18, 44, 77]

print "List of frequencies:", freq
print "Total frequencies:", sum(freq)

expected_kernel = dict(zip(senses, freq))

print "Expected kernel:"
print expected_kernel

corpus = [senses[i] for i in xrange(len(senses)) for n in xrange(freq[i])]

def make_freq_dict(corpus):
	dic = {}
	for word in corpus:
		if word not in dic:
			dic[word] = 1
		else:
			dic[word] += 1
	return dic

def normalize_control(dic):
	new_dic = dic.copy()
	sum_of_dic = float(np.sum(new_dic.values()))
	for key in dic:
		new_dic[key] /= sum_of_dic
	return new_dic

def normalize_list(data):
	array = np.array(data)
	new_array = array / float(np.sum(array))
	return new_array

def normalize_dict(dic):
	keys = dic.keys()
	values = np.array(dic.values())
	new_values = values / float(np.sum(values))
	return dict(zip(keys,new_values))

kernel = make_freq_dict(corpus)

print "Actual kernel:"
print kernel

print "Actual kernel is same as expected:", kernel == expected_kernel

print "Total frequencies:", np.sum(kernel.values()), "; Same as expected:", np.sum(kernel.values()) == sum(freq)

print "Positive control normalization:"
control_norm = normalize_control(kernel)
print control_norm

print "Normalization with list of values as input:"
list_norm = dict(zip(kernel.keys(),normalize_list(kernel.values())))
print list_norm

print "Normalization with dict as input:"
dict_norm = normalize_dict(kernel)
print dict_norm

print "Normalization works?", all([a == b for a,b in itertools.combinations([control_norm, list_norm, dict_norm],2)])

print "Total of values in normalized kernel:", np.sum(dict_norm.values())