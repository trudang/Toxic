import json
import xlrd
import numpy as np
import matplotlib.pyplot as plt

from src.nlp.SemanticString import SemanticString
# from src.visualization.visualization import SemanticVisualization

filename = './data/semantic-distance-database.json'
READ = 'rb'
db = json.load(open(filename,READ))

txt_name = './tweet_comparison_data/drink_20.txt'
with open(txt_name) as f:
  strings = [tweet.strip() for tweet in f.readlines()]

lemmaStrings = [SemanticString(string, db).lemma() for string in strings]

wb_name = 'tweet20_comparison_total.xls'
workbook_input = xlrd.open_workbook(wb_name)
sheet_input = workbook_input.sheet_by_index(0)

ntweets = {'10_tweets': {'toxic': 1, 'tru': 2, 'mike': 3, 'nick': 4}, '20_tweets': {'toxic': 1, 'nick': 2, 'tru': 3, 'mike': 4}}

raters = ntweets['20_tweets']

rater = 'tru'

data = [sheet_input.cell_value(row, raters[rater]) for row in xrange(1, sheet_input.nrows)]

matrix = np.memmap('distances',dtype='float32',mode='w+',
                       shape=(len(lemmaStrings),len(lemmaStrings)))

i = 0
for c in xrange(len(lemmaStrings)-1):
	for r in xrange(c+1, len(lemmaStrings)):
		matrix[r,c] = data[i]
		i += 1

matrix += matrix.transpose()
matrix[np.diag_indices(len(lemmaStrings))] = 0

sizes = {'10_tweets': (10,10), '20_tweets': (15,15)}

size = sizes['20_tweets']
fig = plt.figure(figsize=size)
plt.xticks(range(len(lemmaStrings)+1))
plt.yticks(range(len(lemmaStrings)+1))
ax = fig.add_subplot(111)
cax = ax.imshow(matrix,interpolation='nearest',aspect='auto')
cax.set_clim(vmin=0,vmax=1.0)
del matrix
ax.set_xticklabels(lemmaStrings, rotation = 'vertical')
ax.set_yticklabels(lemmaStrings)
plt.tight_layout()
cbar = plt.colorbar(cax)
cbar.set_label('Semantic distance')
plt.show()
