import json
import numpy as np

wordcount_name = 'test_kernel_data/db-text_wordcount.txt'
# wordcount = json.load(open(wordcount_name,'rb'))
with open(wordcount_name,'r') as f:
		wordcount = eval(f.readline()) #.rstrip('\n')

keys = wordcount.keys()

vals = wordcount.values()

sum_vals = float(np.sum(vals))

freqs = [val/sum_vals for val in vals]

wordfreq = dict(zip(keys,freqs))

textname = 'test_kernel_data/db-text_wordfreq.txt'
with open(textname,'wb') as f:
	print>>f,wordfreq