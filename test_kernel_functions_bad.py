import numpy as np
import itertools
import copy
import matplotlib.pyplot as plt
import pylab as P

from nltk.corpus import wordnet
from src.nlp.SemanticString import SemanticString
from src.nlp.SemanticWord import SemanticWord

def get_corpus(filename):
	with open(filename) as f:
		strings = [tweet.strip() for tweet in f.readlines()]
	corpus = [token.word for string in strings for token in SemanticString(string, {}).tokens]
	return corpus

def get_nouns_from_corpus(corpus):
	# Getting list of unique words with no duplication
	all_words = list(set(corpus))
	# Keeping only nouns
	nouns = [word for word in all_words if SemanticWord(word,'NN',{}).synset != None]
	return nouns

def get_randint_freq(senses):
	freq = [list(np.random.randint(1,101,len(sense))) for sense in senses]
	# freq = [[24, 66, 87], [53, 19, 100, 33, 89, 68, 45]]
	return freq

def get_poisson_freq(senses):
	freq = [list(np.random.poisson(100,len(sense))) for sense in senses]
	# freq = [[91, 96, 103], [100, 108, 107, 93, 100, 104, 97]]
	return freq

def make_freq_dict(word_list, corpus):
	senses = [list(set([sense.name[:sense.name.index('.')] for sense in SemanticWord(word,'NN',{}).synset])) for word in word_list]
	freq = [list(np.zeros(len(sense))) for sense in senses]
	dic = {word: dict(zip(senses[i], freq[i])) for i,word in enumerate(word_list)}
	for element in corpus:
		for word in dic.keys():
			if element in dic[word].keys():
				dic[word][element] += 1
	return dic

def duplicated_freq(kernel, all_senses):
	print "Expecting %s duplicated senses."	% str(len(all_senses) - len(list(set(all_senses))))
	temp = []
	dup_senses = []
	for word in kernel:
		for sense in kernel[word]:
			if sense not in temp:
				temp.append(sense)
			else:
				dup_senses.append((word,sense))
	print "Actual number of duplicated senses:", len(dup_senses)
	tot = 0
	for word,sense in dup_senses:
		tot += kernel[word][sense]
	print "Additional duplicated frequencies:", tot
	return tot

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

def make_plot(kernel,txt_name=None,save=False,show=False):
	for base_word in kernel.keys():
		x,y = zip(*kernel[base_word].items())
		if len(kernel[base_word].keys()) >= 5:
			fig = plt.figure(figsize=(2*len(kernel[base_word].keys()),5))
		else:
			fig = plt.figure()
		ax = fig.add_subplot(111)         
		ax.plot(y,'k',linewidth=2)
		ax.set_xticks(range(len(x)))
		ax.set_xticklabels(x)
		plt.xlabel("Base Word: " + base_word)
		plt.ylabel("Frequency of Sense")
		if save:
			txt_name = txt_name[:txt_name.index('.')] if '.' in txt_name else txt_name
			plt.savefig('%s/%s.png' %(txt_name,base_word),dpi=50)
		if show:
			plt.show()

def test_kernel_functions(freq_dist, db_text=True):
	txt_name = 'test_kernel_data/db-text.txt'	#['tweets_for_test_kernel.txt', 'db-text.txt']
	corpus = get_corpus(txt_name)
	if db_text == True: 
		words = get_nouns_from_corpus(corpus)
	else:
		txt_name = 'test_kernel_data/rest_hold/%s'	%freq_dist
		words = ['rest', 'hold']
	print "Words (nouns) used:", words
	# print len(words)

	senses = [list(set([sense.name[:sense.name.index('.')] for sense in SemanticWord(word,'NN',{}).synset])) for word in words]
	all_senses = np.sum(senses)
	print "List of senses:", all_senses

	if freq_dist != 'from_text':
		distribution = {'randint': get_randint_freq, 'poisson': get_poisson_freq}
		freq = distribution[freq_dist](senses)
		all_freq = np.sum(freq)

		print "List of frequencies:", all_freq
		print "Expected total frequencies:", sum(all_freq)

		expected_kernel = {word: dict(zip(senses[i], freq[i])) for i,word in enumerate(words)}
		print "Expected kernel:"
		print expected_kernel
		corpus = [all_senses[i] for i in xrange(len(all_senses)) for n in xrange(all_freq[i])]

	kernel = make_freq_dict(words, corpus)
	print "Actual kernel:"
	print kernel

	if freq_dist != 'from_text':
		sum_kernel = sum(np.sum([word.values() for word in kernel.values()]))
		if kernel == expected_kernel:
			print "Actual kernel is same as expected."
			print "Total frequencies:", sum_kernel, "; Same as expected?", sum_kernel == sum(all_freq)
		else:
			print "Actual kernel is different from expected. Must have duplicated senses!"
			dup_freq = duplicated_freq(kernel, all_senses)
			print "Total frequencies:", sum_kernel, "; Same as expected + duplicated?", sum_kernel == sum(all_freq) + dup_freq

	print "Positive control normalization:"
	control_norm = normalize_control(kernel)
	print control_norm

	print "Normalization with dict as input:"
	dict_norm = normalize_dict(kernel)
	print dict_norm

	print "Normalization works?", dict_norm == control_norm
	print "Total of values in normalized kernel:", sum(np.sum([word.values() for word in dict_norm.values()]))

	# make_plot(kernel,txt_name,save=False,show=False)


test_kernel_functions(freq_dist='randint', db_text=True)