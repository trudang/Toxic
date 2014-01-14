import numpy as np
import xlwt
import xlrd

a = np.random.randint(-1,2,900)
b = np.random.randint(-1,2,900)

labels = ['= -1', '= 0', '= 1']

def namestr(obj, namespace = globals()):
    return [name for name in namespace if namespace[name] is obj][0]

def contigencyTable(x, y, workbook):
	dic = {}
	for num_x in [-1,0,1]:
		for num_y in [-1,0,1]:
			dic[num_x,num_y] = 0
	for i in range(len(a)):
		dic[x[i], y[i]] += 1

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
	workbook.save("test_randint_contigency2.xls")

combs = [(a,a), (a,b), (b,a), (b,b)]

contigencyTables_to_xls(combs)
