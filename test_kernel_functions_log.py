import os,copy,itertools,json
import numpy as np
import matplotlib.pyplot as plt
import pylab as P

from nltk.corpus import wordnet
from src.nlp.SemanticString import SemanticString
from src.nlp.SemanticWord import SemanticWord
# from src.visualization import Graphics as artist

# from matplotlib import rcParams

# rcParams['text.usetex'] =True

def get_corpus(filename):
	with open(filename,'r') as f:
		strings = [tweet.strip() for tweet in f.readlines()]
	corpus = [token.word for string in strings for token in SemanticString(string, {}).tokens]
	return corpus

def get_nouns_from_corpus(corpus):
	# Getting list of unique words with no duplication
	all_words = list(set(corpus))
	# Keeping only nouns
	nouns = [word for word in all_words if SemanticWord(word,'NN',{}).synset != None]
	return nouns

def import_saved_corpus(txt_name):
	filename = '%s_corpus.txt'	% txt_name[:txt_name.index('.')] if '.' in txt_name else txt_name
	with open(filename,'r') as f:
		corpus = eval(f.readline()) #.rstrip('\n')
	return corpus

def import_saved_wordcount(txt_name):
	filename = '%s_wordcount.txt'	% txt_name[:txt_name.index('.')] if '.' in txt_name else txt_name
	with open(filename,'r') as f:
		wordcount = eval(f.readline()) #.rstrip('\n')
	return wordcount

def import_saved_kernel(txt_name,normed=True):
	if normed:
		filename = '%s_normed_kernel.txt'	% txt_name[:txt_name.index('.')] if '.' in txt_name else txt_name
	else:
		filename = '%s_kernel.txt'	% txt_name[:txt_name.index('.')] if '.' in txt_name else txt_name
	with open(filename,'r') as f:
		kernel = eval(f.readline()) #.rstrip('\n')
	return kernel

def get_randint_freq(senses):
	freq = [list(np.random.randint(1,101,len(sense))) for sense in senses]
	# freq = [[24, 66, 87], [53, 19, 100, 33, 89, 68, 45]]
	return freq

def get_poisson_freq(senses):
	freq = [list(np.random.poisson(100,len(sense))) for sense in senses]
	# freq = [[91, 96, 103], [100, 108, 107, 93, 100, 104, 97]]
	return freq

def wordcount_from_corpus(word_list, corpus):
	count = list(np.zeros(len(word_list)).astype(int))
	dic = dict(zip(word_list,count))
	for element in corpus:
		if element in dic.keys():
			dic[element] += 1
	return dic

def neg_inf_to_zero(array):
	array[array==-np.inf] = 0
	return array

def create_kernel_from_wordcount(wordcount):
	word_list = wordcount.keys()
	senses = [list(set([sense.name[:sense.name.index('.')] for sense in SemanticWord(word,'NN',{},{}).synset])) for word in word_list]
	count = [list(np.zeros(len(sense)).astype(int)) for sense in senses]
	dic = {word: dict(zip(senses[i], count[i])) for i,word in enumerate(word_list)}
	for word in dic.keys():
		for sense in dic[word].keys():
			if sense in wordcount:
				dic[word][sense] = wordcount[sense]
	senses = [dic[word].keys() for word in word_list]
	values = [dic[word].values() for word in word_list]
	sum_of_dic = sum(np.sum(values))
	new_values = [list(neg_inf_to_zero(np.log(np.array(v) / float(sum_of_dic)))) for v in values]
	return {word: dict(zip(senses[i], new_values[i])) for i,word in enumerate(word_list)}

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
	total = 0
	for word,sense in dup_senses:
		total += kernel[word][sense]
	print "Additional duplicated frequencies:", total
	return total

def normalize_control(dic):
	new_dic = copy.deepcopy(dic)
	for word in new_dic:
		sum_of_freq = float(np.sum([new_dic[word].values()])) if float(np.sum([new_dic[word].values()])) != 0 else 1
		for sense in new_dic[word]:
			new_dic[word][sense] /= sum_of_freq
	return new_dic

def normalize_dict(dic):
	words = dic.keys()
	senses = [dic[word].keys() for word in words]
	values = [dic[word].values() for word in words]
	# sum_of_dic = sum(np.sum(values))
	new_values = [list(np.array(v) / float(np.sum(v)) if float(np.sum(v)) != 0 else np.zeros(len(v))) for v in values]
	return {word: dict(zip(senses[i], new_values[i])) for i,word in enumerate(words)}

def save_corpus(corpus, txt_name):
	textname = '%s_corpus.txt'	% txt_name[:txt_name.index('.')] if '.' in txt_name else txt_name
	with open(textname,'wb') as f:
		print>>f,corpus

def save_wordcount(wordcount, txt_name):
	textname = '%s_wordcount.txt'	% txt_name[:txt_name.index('.')] if '.' in txt_name else txt_name
	with open(textname,'wb') as f:
		print>>f,wordcount

def save_kernel(kernel, txt_name):
	textname = '%s_kernel.txt'	% txt_name[:txt_name.index('.')] if '.' in txt_name else txt_name
	with open(textname,'wb') as f:
		print>>f,kernel

def save_normed_kernel(normed_kernel, txt_name):
	textname = '%s_normed_kernel.txt'	% txt_name[:txt_name.index('.')] if '.' in txt_name else txt_name
	with open(textname,'wb') as f:
		print>>f,normed_kernel

def make_plot(kernel,txt_name=None,interval='all',save=False,show=False):
	# Set interval of words in kernel
	# interval can be 'all' or a tuple
	interval = kernel.keys() if interval == 'all' else kernel.keys()[interval[0]:interval[1]]
	# make_pretty = lambda string: r'\Large \textbf{%s}'%string
	for base_word in interval:
		if len(kernel[base_word].keys()) >= 3:
			x,y = zip(*kernel[base_word].items())
			if len(kernel[base_word].keys()) >= 5:
				fig = plt.figure(figsize=(2*len(kernel[base_word].keys()),5))
			else:
				fig = plt.figure()
			ax = fig.add_subplot(111)   
			ax.plot(y,'k',linewidth=2)
			ax.set_ylim((0,1))
			# artist.adjust_spines(ax)
			ax.set_xticks(range(len(x)))
			ax.set_xticklabels(x)
			plt.xlabel("Base Word: " + base_word)
			plt.ylabel("Frequency of Sense")
			# plt.xlabel(make_pretty("Base Word: " + base_word))
			# plt.ylabel(make_pretty("Frequency of Sense"))
			if save:
				txt_name = txt_name[:txt_name.index('.')] if '.' in txt_name else txt_name
				plt.savefig('%s/%s.png' %(txt_name,base_word),dpi=300)
			if show:
				plt.show()

def find_0freq_words_in_kernel(kernel,with_senses=False):
	words_0freq = [word for word in kernel.keys() if sum([kernel[word][sense] for sense in kernel[word].keys()]) == 0]
	if with_senses:
			words_0freq = {word: kernel[word].keys() for word in kernel.keys() if sum([kernel[word][sense] for sense in kernel[word].keys()]) == 0}
	return words_0freq

def write_to_json(data, filename):
	with open('%s.txt' %filename, 'w') as f:
		json.dump(data, f)

def test_kernel_functions(freq_dist, db_text=True, save=False):
	txt_name = 'test_kernel_data/tweets_for_test_kernel.txt'	#['tweets_for_test_kernel.txt', 'db-text.txt']
	corpus = get_corpus(txt_name)
	if db_text == True: 
		words = get_nouns_from_corpus(corpus)
	else:
		txt_name = 'test_kernel_data/rest_hold/%s'	%freq_dist
		words = ['rest', 'hold']
	print "Words (nouns) used:", words
	print len(words)

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

	wordcount = wordcount_from_corpus(words, corpus)
	print "Wordcount:"
	print wordcount

	kernel = create_kernel_from_wordcount(wordcount)
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

	if dict_norm == control_norm and save:
		save_wordcount(wordcount, txt_name)
		save_kernel(kernel, txt_name)
		save_normed_kernel(dict_norm, txt_name)

	freq_per_word = sum(np.sum([dict_norm[word].values() for word in dict_norm.keys()]))/len([word for word in dict_norm.keys() if 0.9999 <= sum(dict_norm[word].values()) <= 1.0001])
	print "Total of values per word in normalized kernel:", freq_per_word

	make_plot(dict_norm,txt_name,save=True,show=False)


def get_kernel(db_name,normed=True):
	txt_name = 'test_kernel_data/%s.txt'	% db_name
	corpus_trigger = '%s_corpus'	%(db_name)
	wordcount_trigger = '%s_wordcount'	%(db_name)
	kernel_trigger = '%s_normed_kernel'%(db_name) if normed else '%s_kernel'%(db_name)
	txt_records = [filename for filename in os.listdir('./test_kernel_data') if filename.endswith('txt') and db_name in filename]
	
	if not any([kernel_trigger in record for record in txt_records]):
		print "Normalized kernel not found. Checking for unnormalized kernel file..."

		if not any(['%s_kernel'%(db_name) in record for record in txt_records]):
			print "Unnormalized kernel not found. Checking for wordcount file..."

			if not any([wordcount_trigger in record for record in txt_records]):
				print "Wordcount file not found. Checking for corpus file..."

				if not any([corpus_trigger in record for record in txt_records]):
					print "Corpus file not found. Start building corpus file."
					corpus = get_corpus(txt_name)
					save_corpus(corpus, txt_name)
					print "Saved corpus."
				else:
					print "Found a local copy of corpus for %s."	% db_name
					corpus = import_saved_corpus(txt_name)
				words = get_nouns_from_corpus(corpus)
				print "Number of base words (nouns):", len(words)
				wordcount = wordcount_from_corpus(words, corpus)
				save_wordcount(wordcount, txt_name)
				print "Saved wordcount."

			else:
				print "Found a local copy of wordcount for %s."	% db_name
				wordcount = import_saved_wordcount(txt_name)

			print "Creating kernel..."
			kernel = create_kernel_from_wordcount(wordcount)
			save_kernel(kernel, txt_name)
			print "Saved kernel."

		else:
			print "Found a local copy of unnormalized kernel for %s."	% db_name
			kernel = import_saved_kernel(txt_name,normed=False)

		print "Normalizing kernel..."
		normed_kernel = normalize_dict(kernel)
		save_normed_kernel(normed_kernel, txt_name)
		print "Saved normalized kernel."

	else:
		print "Found a local copy of kernel for %s."	% db_name
		if normed:
			normed_kernel = import_saved_kernel(txt_name,normed=True)
		else: kernel = import_saved_kernel(txt_name,normed=False)

	return normed_kernel if normed else kernel



db_name = 'db-text'
txt_name = 'test_kernel_data/%s.txt'	% db_name
# kernel = get_kernel(db_name,normed=False)
normed_kernel = get_kernel(db_name,normed=True)

# print len(normed_kernel)
# bad_words = find_0freq_words_in_kernel(normed_kernel, with_senses=False)

# print len(bad_words)

# filename = 'data/words_0freq'

# write_to_json(bad_words,filename)

# make_plot(normed_kernel,txt_name,interval=(0,300),save=True,show=False)

#12708 325 8068

# test_kernel_functions(freq_dist='from_text', db_text=True, save=True)