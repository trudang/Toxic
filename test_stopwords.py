import json
# import itertools
# import numpy as np
# import matplotlib.pyplot as plt

# from time import time
# from pprint import pprint
from src.nlp.SemanticString import SemanticString
# from nltk.corpus import wordnet
# from termcolor import colored

filename = './data/semantic-distance-database.json'
READ = 'rb'
db = json.load(open(filename,READ))
strings = ['a', 'a\n\n', 'a ', 'a\r\n']

stopwords = open('./data/stopwords',READ).readlines()
print stopwords[0:2]
stopwords = [stopword.rstrip('\r\n') for stopword in stopwords]
print stopwords[0:2]

for string in strings:
	print '|%s|'%(repr(SemanticString(string, db)))


