import json
import itertools
import xlwt
import xlrd
from src.nlp.SemanticString import SemanticString

filename = './data/semantic-distance-database.json'
READ = 'rb'
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

lemmaStrings = [SemanticString(string, db).lemma() for string in strings]

comb_itertools = itertools.combinations(lemmaStrings,2)

comb = [(a,b) for a,b in comb_itertools]

tweet_comb = [(a, ' -VS- ',b) for a,b in comb]

# print len(tweet_comb)

distances = [SemanticString(a,db)- SemanticString(b,db) for a,b in comb]

# print distances

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

workbook.save("tweet_comparison_toxic.xls") 




