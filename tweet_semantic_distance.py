import json
import itertools
import numpy as np
import matplotlib.pyplot as plt

from time import time
from pprint import pprint
from src.nlp.SemanticString import SemanticString
from nltk.corpus import wordnet
from termcolor import colored
# from src.visualization.visualization import SemanticVisualization

filename = './data/semantic-distance-database.json'
READ = 'rb'
WRITE = 'wb'
APPEND = 'a+'
db = json.load(open(filename,READ))

txt_name = './tweet_comparison_data/drink_20.txt'
with open(txt_name) as f:
  strings = [tweet.strip() for tweet in f.readlines()]

lemmaStrings = [SemanticString(string, db).lemma() for string in strings]

start = time()



print('/----------------Beginning test ------------\\')

##for one in strings:
##	for two in strings:
##
##		d1 = SemanticString(one,db)
##		d2 = SemanticString(two,db)
##
##		print '|%s|'%(repr(d1))
##		print '|%s|'%(repr(d2))
##
##		print '|Semantic distance between them: %.04f |'%(d1-d2)

# matrixName = 'C:/Users/Default.Default-THINK/Documents/GitHub/Toxic/data/%s.similarity-matrix-tsv'%('test1')

##matrix = np.memmap(matrixName,dtype='float32',mode='w+',
##                        shape=(len(strings),len(strings)))
##
##for i in xrange(len(strings)):
##        for j in xrange(i):
##                matrix[i,j] = SemanticString(matrix[i],db) - SemanticString(matrix[j],db)
##
##matrix += matrix.transpose()
##matrix[np.diag_indices(len(strings))] = 0
##del matrix
##matrix.close()

distances = [[SemanticString(one,db)- SemanticString(two,db) for one in lemmaStrings] for two in lemmaStrings]

minDis = np.min(distances)
maxDis = np.max(distances)

scaledDistances = [[(d - minDis)/maxDis for d in distance] for distance in distances]

sizes = {'10_tweets': (10,10), '20_tweets': (15,15)}

size = sizes['20_tweets']
fig = plt.figure(figsize=size)
plt.xticks(range(len(lemmaStrings)+1))
plt.yticks(range(len(lemmaStrings)+1))
ax = fig.add_subplot(111)
cax = ax.imshow(scaledDistances,interpolation='nearest',aspect='auto')
cax.set_clim(vmin=0,vmax=1.0)
ax.set_xticklabels(lemmaStrings, rotation = 'vertical')
ax.set_yticklabels(lemmaStrings)
plt.tight_layout()
cbar = plt.colorbar(cax)
cbar.set_label('Semantic distance')
plt.show()

##x = SemanticVisualization(trigger='test1', data = distances)
##x.heatmap(savename='test1',show=True)

print '---'
# json.dump(db,open(filename,APPEND))	
print '|Duration %.04f s|'%(time()-start)
print('\----------------Finished test ------------/')


