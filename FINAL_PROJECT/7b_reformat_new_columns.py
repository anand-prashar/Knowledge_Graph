'''
Created on Dec 4, 2017

@author: anand
'''


import json
import csv
import string
from os import listdir, linesep, path
from Levenshtein import ratio as Lev_Ratio
import sys; reload(sys); sys.setdefaultencoding("utf-8")

global addrDict, addrList, githubDict, entityMappingDict, companyDict, companyList, universityDict, universityList
githubDict = {}; addrDict = None; entityMappingDict = {}; companyDict = {}; companyList=[]
universityDict={}; universityList  =[]
global gloss_linkedentt, gloss_tech
gloss_linkedentt = set(); gloss_tech= set()

def readFile(fileName):
    
    dataList = []
    with open(fileName,'rb') as f:
        for row in f:
            if row=='': continue
            row = json.loads(row)
            separate_linkedEntities( row )  # <-------------
            dataList.append( row )
    
    return dataList

def writeFile(standardizedList, fileName):
    
    with open(fileName,'wb') as f:
        for row in standardizedList:
            if row=='': continue
            #row.pop('workedon')
            f.write( json.dumps(row)+linesep)
    
    print 'Written'
    
##################################################################################################################

#===============================================================================
# def getLinkedEntityList(url):
#     if url in [None,''] : return []
#     url = url.lower()
#     
#     global entityMappingDict
#     
#     if not entityMappingDict:
#         # 1st hit run
#         with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\gitHub_linking_mapper.csv','rb') as f:
#             
#             csvR = csv.reader(f, delimiter=',',quoting=csv.QUOTE_ALL)
#             urls = 1
#             for rowList in csvR:
#                 rowList = [x.lower() for x in rowList if x!='']
#                 for row in rowList:
#                     urls+=1
#                     if 'https://leetcode.com' in row: row=row[:-1]  #ignore last /
#                     entityMappingDict.setdefault(row, rowList)
#                 if urls > 25000:   #<-------------------------------------------------------------------------
#                     break
# 
# 
#     
#     if url in entityMappingDict:
#         return entityMappingDict[url]
#     return []
#===============================================================================

def separate_linkedEntities(opJl):
    def attach(receivedURL, opJl ):
        if sourcename == 'github.com':
            opJl['link_github'] = receivedURL
        elif sourcename == 'stackoverflow.com':
            opJl['link_stackoveflow'] = receivedURL
        elif sourcename == 'hackerrank.com':
            opJl['link_hackerrank'] = receivedURL
        elif sourcename == 'leetcode.com':
            opJl['link_leetcode'] = receivedURL
        elif sourcename == 'github.io':
            opJl['link_blog'] = receivedURL        
        
    
        #opJl['linkedentity'] = getLinkedEntityList(jsonObj['url'])
    opJl['link_github'] = ''; opJl['link_stackoveflow'] = ''; opJl['link_etc']=''; 
    opJl['link_hackerrank']=''; opJl['link_leetcode']=''
        
    for url in opJl['linkedentity']:
        addToBlog = True
        for sourcename in ['github.com','stackoverflow.com','hackerrank.com','leetcode.com','github.io']:
            if sourcename in url:
                if sourcename not in opJl['url']:
                    attach( url, opJl)
                else:
                    attach( opJl['url'], opJl)
                addToBlog = False
        
        if addToBlog:
                opJl['link_etc']= url
    
    opJl.pop('linkedentity')
##################################################################################################################
##################################################################################################################



ipDir = 'C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\FOR_DIG\\Old\\'
opDir = 'C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\FOR_DIG\\'

aggregatedFilesList = [(hfile.split('.')[0], ipDir+'\\'+hfile) for hfile in listdir(ipDir) \
                       if path.isfile(ipDir+'\\'+hfile) and hfile.split('.')[1]=='jl']

for fileSource, fileName in aggregatedFilesList:
    
    dataList = readFile(fileName)
    print '\n'
    print fileSource, 'data read'
    if fileSource == 'Github':
        #standardizedList = standardize_github(dataList)
        writeFile(dataList, opDir+'Github_c.jl')
        del dataList
        continue
        
    if fileSource == 'Stackoverflow':
        #standardizedList = standardize_stackoverflow(dataList)
        writeFile(dataList, opDir+'Stackoverflow_c.jl')
        del dataList
        continue
    
    if fileSource == 'Leetcode':
        #standardizedList = standardize_leetcode(dataList)
        writeFile(dataList, opDir+'Leetcode_c.jl')
        del dataList
        continue
    
    if fileSource == 'Hackerrank':
        #standardizedList = standardize_hackerrank(dataList)
        writeFile(dataList, opDir+'Hackerrank_c.jl')
        del dataList
        continue
    
    if fileSource == 'GithubIO':
        #standardizedList = standardize_github_IO_blog(dataList)
        writeFile(dataList, opDir+'GithubIO_c.jl')
        del dataList
        continue