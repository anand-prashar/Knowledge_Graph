'''
Created on Nov 23, 2017

@author: anand
'''
import csv
from os import getcwd
import sys; reload(sys); sys.setdefaultencoding("utf-8")

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def readCsv(filename, getDict):
    if getDict:
        retList = [{}, {} ]
    else:    
        retList = []
    with open(filename,'rb') as f:
        csvObj = csv.reader(f, delimiter=',', quoting = csv.QUOTE_MINIMAL)
        for row in csvObj:
            if getDict:
                retList[0].setdefault(row[2].lower(),row[1].lower())  # ca -> california
                retList[1].setdefault(row[1].lower(),row[1].lower())  # california -> california
            else:    
                retList.append(row)
    print 'read: ', filename
    return retList

def writeCsv(filename, opList):
    
    with open(filename,'wb') as f:
        csvObj = csv.writer(f, delimiter=',', quoting = csv.QUOTE_ALL)
        for row in opList:
            csvObj.writerow( row)
    print 'written: ', filename
    

######################################################################

# address
def cleanAddressFile():
    
    LocationFileList = readCsv( getcwd()+'//ref_data2//locationFile_cleaned.csv', False)
    UScodeDict =     readCsv( getcwd()+'//ref_data2//usa_code.csv', True)
    canadaCodeDict = readCsv( getcwd()+'//ref_data2//canada_code.csv', True)
    
    exportFile = getcwd()+'//ref_data2//locationFile_cleaned_OK.csv'
    
    for rowList in LocationFileList:
        for id in range(1, len(rowList)):
            if not is_ascii(rowList[id]): 
                rowList[id] = ''
                
        if  rowList[2] in UScodeDict[0] or rowList[2] in UScodeDict[1] : 
            if rowList[2] in UScodeDict[0]:
                rowList[2] = UScodeDict[0][ rowList[2]]
            rowList[3] = 'united states'
        elif rowList[2] in canadaCodeDict[0] or rowList[2] in canadaCodeDict[1] :  
            if rowList[2] in canadaCodeDict[0]:
                rowList[2] = canadaCodeDict[0][ rowList[2]]
            rowList[3] = 'canada'
        
    
    writeCsv(exportFile, LocationFileList)   
    
###########################################################################

def clean_othercsvFiles():
    
    def cleanIt(fileList):
        for rowList in fileList:
            for id in range(1, len(rowList)):
                if not is_ascii(rowList[id]): 
                    rowList[id] = ''
    
    fileList = readCsv( getcwd()+'//ref_data2//companyFile_cleaned.csv', False)
    exportFile = getcwd()+'//ref_data2//companyFile_cleaned_OK.csv'
    cleanIt(fileList)
    writeCsv(exportFile, fileList) 
    
    fileList = readCsv( getcwd()+'//ref_data2//universityFile_cleaned.csv', False)
    exportFile = getcwd()+'//ref_data2//universityFile_cleaned_OK.csv'
    cleanIt(fileList)
    writeCsv(exportFile, fileList) 
    
    

###########################################################################  
     
cleanAddressFile()
clean_othercsvFiles()            
    