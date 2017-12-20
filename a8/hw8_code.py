'''
Created on Nov 6, 2017

@author: anand
'''

import csv 
from jellyfish import jaro_winkler
from Levenshtein import ratio as Lev_Ratio


def readFile(fname):
    
    def phoneFormat(cellValue):
        
        retList=[]
        for cell in cellValue.split('^'):
            
            retList.append( unicode(cell.replace('/','-').replace(' ','')) )
            
        return retList    
    
    def cuisineFormat(cellValue):
        retList=[]
        for cell in cellValue.split('/'):
            retList.append( unicode(cell) )
            
        return retList
    
    retList = []
    with open(fname) as f:
        csvR = csv.reader(f, delimiter = ',', quotechar='"')
        header=True
        for row in csvR:
            if header: header = False; continue
            retList.append([[unicode(row[0].lower())], phoneFormat(row[1].lower()), cuisineFormat(row[2].lower()) ] )
            
    return retList

def stringSimilarity(zList, fList, threshold):
    
    def phone_equals(val1, val2):
        if val1 == val2:
            return 1
        elif val1[:8] == val2[:8]:
            return 0.75
        #=======================================================================
        # elif val1[:3] == val2[:3]:
        #     return 0.25
        #=======================================================================
        return 0
    
    def cell_to_cell_compare(method, file1_cellList, file2_cellList):
        
        maxMatchPercent=0
        
        for f1_val in file1_cellList:
            for f2_val in file2_cellList:
                calc_sim = method(f1_val, f2_val )
                if maxMatchPercent < calc_sim: maxMatchPercent = calc_sim
        
        return maxMatchPercent        
                
                
    
    columnWiseMatch_list = []
    
    
    
    for i1 in range(len(zList)):
        for i2 in range(len(fList)):

            match_address = cell_to_cell_compare( Lev_Ratio,    zList[i1][0], fList[i2][0])
            match_phone   = cell_to_cell_compare( phone_equals, zList[i1][1], fList[i2][1])
            match_cuisine = cell_to_cell_compare( jaro_winkler, zList[i1][2], fList[i2][2])
            
            overall_record_sim = 0.40 * match_address + 0.50 * match_phone+ 0.10 * match_cuisine
            if overall_record_sim < threshold and ( match_phone == 1): overall_record_sim = threshold 
                
            columnWiseMatch_list.append( [ (i1+1,i2+1), match_address, match_phone, match_cuisine, overall_record_sim ])
            
    columnWiseMatch_list = sorted( columnWiseMatch_list, key = lambda x: x[4], reverse = True)
    #columnWiseMatch_list = columnWiseMatch_list[:112]
    columnWiseMatch_list = [x for x in columnWiseMatch_list if x[4]>=threshold ]
    matched_rows_in_zList = set()
    matched_rows_in_fList = set()
    result = []
    
    
    for row in columnWiseMatch_list:
        if row[0][0] not in matched_rows_in_zList and row[0][1] not in matched_rows_in_fList:
            result.append(row)
            matched_rows_in_zList.add(row[0][0])
            matched_rows_in_fList.add(row[0][1])
            
    opFile = open('output.txt','wb')
    result = sorted(result, key = lambda x: x[0][0])
    for row in result:
        opFile.write('zagats.csv:'+str(row[0][0])+'\tfodors.csv:'+str(row[0][1])+'\n')
                
        
    opFile.close()
            
    print 'Done'

##############################################################


zList=readFile('zagats.csv')
fList=readFile('fodors.csv')
stringSimilarity(zList, fList, 0.78)