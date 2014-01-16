import numpy as np

from nltk.corpus import wordnet
from src.nlp.SemanticString import SemanticString
from src.nlp.SemanticWord import SemanticWord

txt_name = 'tweets_for_test_kernel.txt'
with open(txt_name) as f:
  strings = [tweet.strip() for tweet in f.readlines()]

print "Collected %s tweets from Tweeters."	% len(strings)

words= [token.word for string in strings for token in SemanticString(string, {}).tokens]

print "Lemmatized down to total %s words."	% len(words)

dic = {}

for word in words:
	if word not in dic:
		dic[word] = 1
	else:
		dic[word] += 1

print "There are %s distinct words."	%len(dic)

print "Words that appear more than once:"
for word in dic.keys():
	if dic[word] > 1:
		print word + ':', dic[word]

sum_of_dic = sum([dic[key] for key in dic.keys()])

print "Doublechecking sum of all entry values in kernel: %s total words." % sum_of_dic

norm_dic = dic.copy()

for key in norm_dic:
	norm_dic[key] /= float(sum_of_dic)

sum_of_norm_dic = sum([norm_dic[key] for key in norm_dic.keys()])

print "After normalization, sum of all entry values in normalized kernel: %s"	% sum_of_norm_dic

print "Original kernel: %s"	% dic
print "Normalized kernel: %s"	% norm_dic
