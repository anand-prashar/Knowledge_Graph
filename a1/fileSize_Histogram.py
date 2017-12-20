'''
Created on Sep 10, 2017

@author: anand
'''

import os, csv

cwd = os.getcwd()
filenames = next(os.walk(cwd))[2]

sizeDict = {}
for file in filenames:
    if file.split('.')[-1]=='html':
        fileSize = int(os.path.getsize(file)/1024)
        if fileSize not in sizeDict:
            sizeDict[fileSize] = [file]
        else:
            sizeDict[fileSize].append( file)    

sortedFilesCount = []
for size, filesList in sizeDict.items():
    sortedFilesCount.append([size,len(filesList)]) 

sortedFilesCount = sorted( sortedFilesCount, key = lambda x: x[0], reverse = True)

fname = 'HTML files summary.csv'
ofile  = open(fname, 'wb')
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(['File Size(in KB)','No. of Files'])
    
for sizeInfo in sortedFilesCount:
    writer.writerow(sizeInfo)
ofile.close()    

print 'Summarized : '+fname