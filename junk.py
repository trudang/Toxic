# def histogram(kernel):
# 	words = kernel.keys()
# 	senses = [kernel[word].keys() for word in kernel.keys()]
# 	values = [kernel[word].values() for word in kernel.keys()]
# 	fig = plt.figure()
# 	n, bins, patches = plt.hist(values, 5, 
# 		#normed=True, 
# 		histtype='bar', label=words)
# 	plt.xlabel("Frequency of Sense")
# 	plt.ylabel("Number of Senses with Same Frequency")
# 	plt.legend()
# 	plt.show()

import numpy as np
from src.nlp.SemanticString import SemanticString
from src.nlp.SemanticWord import SemanticWord
# from test_kernel_functions import get_kernel

# db_name = 'db-text'
# txt_name = 'test_kernel_data/%s.txt'	% db_name

# kernel = get_kernel(db_name,normed=True)

# a = SemanticWord('book', 'NN', {}, kernel)
# b = SemanticWord('study', 'NN', {}, kernel)

# a = SemanticWord('study', 'NN', {}, {})
# b = SemanticWord('study', 'NN', {}, {})

# print a - b

# print kernel['book']

# print kernel['study']

# # print np.average([7,6,5,4,11,9,11,9,11,9])

# a = [1,1,1,1,1,1,1,1,1]
# c = [.5,.3,.2]
# c = [1,1,1]
# d = [1,1,1]
# # d = [.25,.35,.4]

# total = sum([1*c1*d1 for c1 in c for d1 in d])

# a = {1:2, 3:4}

# print a.items()
print ([2,4,6,7] + [2,6,8,2])

import numpy as np
import math

a = np.array([1,2,3,4,5,6,7, 0])

result = np.exp(a)

print result

result[result==1]=0

print result




