import numpy as np
import itertools

from nltk.corpus import wordnet
from src.nlp.SemanticString import SemanticString
from src.nlp.SemanticWord import SemanticWord

txt_name = 'tweets_for_test_kernel.txt'
with open(txt_name) as f:
  strings = [tweet.strip() for tweet in f.readlines()]

print "Collected %s tweets from Twitter."	% len(strings)

word_list = [token.word for string in strings for token in SemanticString(string, {}).tokens]

print word_list

print "Lemmatized down to total %s words."	% len(word_list)

frequency_dic = {}
frequency_dic1 = {}

# frequency_dic1[word] += 1 if word not in frequency_dic1 else 1 for word in word_list

for word in word_list:
	if word not in frequency_dic:
		frequency_dic[word] = 1
	else:
		frequency_dic[word] += 1

parts = ['NN', 'JJ', 'VB', 'RB']			#[wordnet.NOUN, wordnet.ADJ, wordnet.VERB, wordnet.ADV]
for word in frequency_dic:
	part_comb = itertools.combinations(parts,2)
	a = [SemanticWord(word,part1,{}).synset == SemanticWord(word,part2,{}).synset for part1,part2 in part_comb]
	if all(a):
		print word, 'GOOD!'
		print a
		for part in parts:
			print SemanticWord(word,part,{}).synset
	else:
		print word, 'NOT EQUAL!'
		print a
		for part in parts:
			print SemanticWord(word,part,{}).synset

def frequency(sense, corpus):
	word = sense.name[:sense.name.index('.')]
	return corpus[word] if word in corpus else 0

# def normalize(senses):
# 	if senses == {}:
# 		print "THIS IS NONE!"
# 	sum_of_freq = sum([senses[key] for key in senses.keys()])
# 	# for key in senses:
# 	# 	if sum_of_freq != 0:
# 	# 		senses[key] /= float(sum_of_freq)
# 	for key in senses:
# 		senses[key] = senses[key]/float(sum_of_freq) if sum_of_freq != 0 else 0.0
# 	print senses
# 	return senses


# kernel = {word: {sense: frequency(sense,frequency_dic) for sense in SemanticWord(word, wordnet.NOUN, {}).synset} for word in frequency_dic}

# print kernel







# NOUN = 0
# kernel = {word: normalize({sense: frequency(sense,frequency_dic) for sense in SemanticWord(word, wordnet.NOUN, {}).synset}) for word in frequency_dic}
# kernel[NOUN::4].sum()
# kernel /= normalize 
# kernel = {}

# for word in frequency_dic:
# 	print SemanticWord(word, wordnet.NOUN, {}).synset
# 	for sense in SemanticWord(word, wordnet.NOUN, {}).synset:
# 		kernel[word] = normalize({sense: frequency(sense,frequency_dic)})


# print kernel


















# print "There are %s distinct words."	%len(dic)

# print "Words that appear more than once:"
# for word in dic.keys():
# 	if dic[word] > 1:
# 		print word + ':', dic[word]

# sum_of_dic = sum([dic[key] for key in dic.keys()])

# print "Doublechecking sum of all entry values in kernel: %s total words." % sum_of_dic

# norm_dic = dic.copy()

# for key in norm_dic:
# 	norm_dic[key] /= float(sum_of_dic)

# sum_of_norm_dic = sum([norm_dic[key] for key in norm_dic.keys()])

# print "After normalization, sum of all entry values in normalized kernel: %s"	% sum_of_norm_dic

# print "Original kernel: %s"	% dic
# print "Normalized kernel: %s"	% norm_dic
