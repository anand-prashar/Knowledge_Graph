'''
Created on Nov 29, 2017

@author: anand
'''
import csv
from os import linesep
uniqueLinks = set()

with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\gitHub_linking_mapper.csv','rb') as f:
    csvR = csv.reader(f, delimiter=',',quoting=csv.QUOTE_ALL)
    for rowList in csvR:
        for cell in rowList:
            uniqueLinks.add(cell)


print len(uniqueLinks), 'unique links found'

# export as txt to desktop

with open('C:\\Users\\anand\\Desktop\\gloss\\linkedentity.txt','wb') as f:
    for url in sorted( list( uniqueLinks)):
        f.write(url+linesep)
        
print 'Done'