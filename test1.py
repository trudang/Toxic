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


strings = ["Making out with the air while trying to find the straw in your drink.",
           "You drink too much, swear too much and your morals are questionable.",
           "I drink green juice every morning",
           "Drink some water after you wake up.",
           "When u feelin the drinks and drugs in the club",
           "i tink i had a bit too many drinks!cant find m phone!would u mind looking for it?",
           "Sitting outside at a cafe drinking our first legal drinks.",
           "I don't have a drinking problem",
           "Keep horses drinking during freezing weather...and all animals.",
           "establishing difference is a crucial element to satisfying programming"]

##strings = ['tag', 'u t@g me', 'TAKE ME TO WORK AND SING']
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

distances = [[SemanticString(one,db)- SemanticString(two,db) for one in strings ] for two in strings ]

print distances

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(distances,interpolation='nearest',aspect='auto')
plt.tight_layout()
plt.show()

##x = SemanticVisualization(trigger='test1', data = distances)
##x.heatmap(savename='test1',show=True)

print '---'
# json.dump(db,open(filename,APPEND))	
print '|Duration %.04f s|'%(time()-start)
print('\----------------Finished test ------------/')

