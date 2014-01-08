import json
import itertools

from time import time
from pprint import pprint
from src.nlp.SemanticString import SemanticString
from nltk.corpus import wordnet
from termcolor import colored 

filename = './data/semantic-distance-database.json'
READ = 'rb'
WRITE = 'wb'
APPEND = 'a+'
db = json.load(open(filename,READ))

##strings = ["Making out with the air while trying to find the straw in your drink.",
##           "You drink too much, swear too much and your morals are questionable.",
##           "I drink green juice every morning",
##           "Drink some water after you wake up.",
##           "When u feelin the drinks and drugs in the club",
##           "i tink i had a bit too many drinks!cant find m phone!would u mind looking for it?",
##           "Sitting outside at a cafe drinking our first legal drinks.",
##           "I don't have a drinking problem",
##           "Keep horses drinking during freezing weather...and all animals.",
##           "Chillen, smokin, and drinking Jesus juice"]

strings = ['tag', 'u t@g me', 'TAKE ME TO WORK AND SING']
start = time()



print('/----------------Beginning test ------------\\')

for one in strings:
	for two in strings:

		d1 = SemanticString(one,db)
		d2 = SemanticString(two,db)

		print '|%s|'%(repr(d1))
		print '|%s|'%(repr(d2))

		print '|Semantic distance between them: %.04f |'%(d1-d2)

print '---'
json.dump(db,open(filename,WRITE))	
print '|Duration %.04f s|'%(time()-start)
print('\----------------Finished test ------------/')

