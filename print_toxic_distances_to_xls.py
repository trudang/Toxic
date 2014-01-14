import json
import itertools
import xlwt
import xlrd
from src.nlp.SemanticString import SemanticString

filename = './data/semantic-distance-database.json'
READ = 'rb'
db = json.load(open(filename,READ))

txt_name = './tweet_comparison_data/drink_10.txt'
with open(txt_name) as f:
  strings = [tweet.strip() for tweet in f.readlines()]

lemmaStrings = [SemanticString(string, db).lemma() for string in strings]

comb_itertools = itertools.combinations(lemmaStrings,2)

comb = [(a,b) for a,b in comb_itertools]

tweet_comb = [(a, ' -VS- ',b) for a,b in comb]

# print len(tweet_comb)

distances = [SemanticString(a,db) - SemanticString(b,db) for a,b in comb]

maxDis = max(distances)

scaledDistances = [distance/maxDis for distance in distances]

workbook = xlwt.Workbook() 
sheet = workbook.add_sheet("Tweets Comparison")

style = xlwt.easyxf('font: bold 1')
sheet.write(0, 0, 'Tweet Pair-Wise Combinations', style)
sheet.write(0, 1, 'Difference Rating (0: same, 1: completely different)', style)

for row in xrange(1, len(tweet_comb)+1):
	sheet.write(row, 0, tweet_comb[row-1])

for row in xrange(1, len(tweet_comb)+1):
  sheet.write(row, 1, scaledDistances[row-1])

# workbook.save("tweet10_comparison_toxic.xls") 




