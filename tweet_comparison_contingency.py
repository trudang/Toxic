import numpy as np
import xlwt
import xlrd
import itertools

# Define labels for rows & columns in Excel sheet
labels = ['SD < toxic - 5%', 'SD == toxic +- 5%', 'SD > toxic + 5%']

# Import data of all ratings
workbook_input = xlrd.open_workbook('tweet20_comparison_total.xls')
sheet_input = workbook_input.sheet_by_index(0)

ntweets = {'10_tweets': {'toxic': 1, 'tru': 2, 'mike': 3, 'nick': 4, 'toxicNEW': 5},
			'20_tweets': {'toxic': 1, 'nick': 2, 'tru': 3, 'mike': 4, 'toxicNEW': 5}}

raters = ntweets['20_tweets']

toxic = [sheet_input.cell_value(row, raters['toxic']) for row in xrange(1, sheet_input.nrows)]
tru = [sheet_input.cell_value(row, raters['tru']) for row in xrange(1, sheet_input.nrows)]
mike = [sheet_input.cell_value(row, raters['mike']) for row in xrange(1, sheet_input.nrows)]
nick = [sheet_input.cell_value(row, raters['nick']) for row in xrange(1, sheet_input.nrows)]
toxicNEW = [sheet_input.cell_value(row, raters['toxicNEW']) for row in xrange(1, sheet_input.nrows)]

# Function to obtain name of variable
def namestr(obj, namespace = globals()):
    return [name for name in namespace if namespace[name] is obj][0]

# Create and 
def contigencyTable(x, y, workbook):
	new_x = x[:]
	new_y = y[:]
	dic = {}

	# Convert ratings into -1,0,1 in comparison to toxic's ratings
	for num_x in [-1,0,1]:
		for num_y in [-1,0,1]:
			dic[num_x,num_y] = 0

	for var in [new_x, new_y]:
		for i in range(len(var)):
			# print var[i], toxic[i] - .05*toxic[i], toxic[i] + .05*toxic[i]
			if toxic[i] - .05*toxic[i] <= var[i] <= toxic[i] + .05*toxic[i]:
				# print 'equal'
				var[i] = 0
			elif var[i] < toxic[i] - .05*toxic[i]:
				# print 'smaller'
				var[i] = -1
			elif var[i] > toxic[i] + .05*toxic[i]:
				# print 'larger'
				var[i] = 1

	for i in range(len(toxic)):
		dic[new_x[i], new_y[i]] += 1

	# Creating sheet with combination label
	sheetName = namestr(x)+'-'+namestr(y)
	sheet = workbook.add_sheet(sheetName)

	style = xlwt.easyxf('font: bold 1')

	# Input labels for rows and columns
	for i in xrange(len(labels)):
		sheet.write(i+1, 0, labels[i], style)
	for j in xrange(len(labels)):
		sheet.write(0, j+1, labels[j], style)

	# Input entries into the contigency table
	for row,col in dic:
		sheet.write(row+2, col+2, dic[row,col])

	# Create matrix & calculate trace, sum, etc.
	m = np.zeros(shape=(len(labels), len(labels)))

	for r,c in dic:
		m[r,c] = dic[r,c]

	sheet.write(0, len(labels)+2, 'Trace', style)
	sheet.write(0, len(labels)+3, np.trace(m))

	sheet.write(1, len(labels)+2, 'Sum', style)
	sheet.write(1, len(labels)+3, m.sum())

	sheet.write(3, len(labels)+2, 'Trace/Sum', style)
	sheet.write(3, len(labels)+3, np.trace(m)/float(m.sum()))

	# Adjust the cell's width
	col_width = 256 * (len(labels[1]) + 1)
	try:
		for i in itertools.count():
			sheet.col(i).width = col_width
	except ValueError:
		pass

# Create & save Excel sheet
def contigencyTables_to_xls(combs):
	workbook = xlwt.Workbook()
	for x,y in combs:
		contigencyTable(x,y, workbook)
	workbook.save("tweet20_comparison_contigency.xls")

raters = [toxic, tru, nick, toxicNEW]

# combs = [(r1,r2) for r1 in raters for r2 in raters]
combs = itertools.combinations(raters,2)

contigencyTables_to_xls(combs)

