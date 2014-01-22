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

a = range(100)

print a[:10]
print a[10:20]

print sum([7.0])

a = {'b':{'c':3.0}}

print a.keys()
print a['b'].values()

print len([sum(a['b'].values())])

look = range(100)

interval = (1,20)

interval = 100 if interval == 'all' else look[interval[0]:interval[1]]

print interval