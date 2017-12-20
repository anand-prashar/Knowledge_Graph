'''
Created on Nov 26, 2017

@author: anand
'''
import csv

of = open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\gitHub_linking_mapper2.csv','wb')
csvOp = csv.writer(of, delimiter=',', quoting=csv.QUOTE_ALL)

with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\gitHub_linking_mapper.csv','rb') as f:
    csvR = csv.reader(f, delimiter=',',quoting=csv.QUOTE_ALL)
    for row in csvR:
        opList = []
        for cell in row:
            if '.github.io' in cell:
                left = cell.split('.github.io')[0]
                if 'http://' in left:
                    cell = 'https://' + left.split('http://')[1] + '.github.io'
                elif 'http://' not in left:
                    cell = 'https://' + left + '.github.io'
            opList.append(cell)
        
        csvOp.writerow(opList)

print 'Done'        