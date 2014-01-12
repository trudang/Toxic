import numpy as np
import xlwt
import xlrd

labels = ['SD < toxic', 'SD == toxic +- 5%', 'SD > toxic']

workbook_input = xlrd.open_workbook('tweet_comparison_total.xls')
sheet_input = workbook_input.sheet_by_index(0)

toxic = [sheet_input.cell_value(row, 1) for row in xrange(1, sheet_input.nrows)]

tru = [sheet_input.cell_value(row, 2) for row in xrange(1, sheet_input.nrows)]

mike = [sheet_input.cell_value(row, 3) for row in xrange(1, sheet_input.nrows)]

def namestr(obj, namespace = globals()):
    return [name for name in namespace if namespace[name] is obj][0]

def contigencyTable(x, y, workbook):
	new_x = x[:]
	new_y = y[:]
	dic = {}
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

	sheetName = namestr(x)+'-'+namestr(y)
	sheet = workbook.add_sheet(sheetName)

	style = xlwt.easyxf('font: bold 1')

	for i in xrange(len(labels)):
		sheet.write(i+1, 0, labels[i], style)
	for j in xrange(len(labels)):
		sheet.write(0, j+1, labels[j], style)

	for row,col in dic:
		sheet.write(row+2, col+2, dic[row,col])

def contigencyTables_to_xls(combs):
	workbook = xlwt.Workbook()
	for x,y in combs:
		contigencyTable(x,y, workbook)
	workbook.save("tweet_comparison_contigency.xls")

raters = [toxic, tru, mike]

combs = [(r1,r2) for r1 in raters for r2 in raters]

contigencyTables_to_xls(combs)

