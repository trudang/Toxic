import json
import itertools
import xlwt
import xlrd
from src.nlp.SemanticString import SemanticString

filename = './data/semantic-distance-database.json'
READ = 'rb'
db = json.load(open(filename,READ))

txt_name = './tweet_comparison_data/drink_20.txt'
with open(txt_name) as f:
  strings = [tweet.strip() for tweet in f.readlines()]

lemmaStrings = [SemanticString(string, db).lemma() for string in strings]

comb = itertools.combinations(lemmaStrings,2)

tweet_comb = [(a, ' -VS- ',b) for a,b in comb]

# print len(tweet_comb)

workbook = xlwt.Workbook() 
sheet = workbook.add_sheet("Tweets Comparison")

style = xlwt.easyxf('font: bold 1')
sheet.write(0, 0, 'Tweet Pair-Wise Combinations', style)
sheet.write(0, 1, 'Difference Rating (0: same, 1: completely different)', style)

for row in xrange(1, len(tweet_comb)+1):
	sheet.write(row, 0, tweet_comb[row-1])

# sheet.col(0).width = 256 * (len(key) + 1)

workbook.save("tweet20_comparison_template.xls") 




