'''
Created on Nov 25, 2017

@author: anand
'''
import json
import csv
import string
from os import listdir, linesep
from Levenshtein import ratio as Lev_Ratio
import sys; reload(sys); sys.setdefaultencoding("utf-8")
from pandas.tests.io.parser import quoting

global addrDict, addrList, githubDict
githubDict = {}; addrDict = None
 
def extract_and_consolidate_GITHUB(dataFile):
    print 'Processing : ', dataFile.split('\\')[-1]
    
    global githubDict
    
    with open(dataFile) as f:
        for line in f:
            if line == '': continue
            jsonObj = json.loads(line)
            githubDict.setdefault(jsonObj['url'], jsonObj)
            #===================================================================
            # if jsonObj['url'] not in githubDict:
            #     jsonObj['LinkedEntity'] = set( jsonObj['LinkedEntity'] ) 
            #     githubDict.setdefault(jsonObj['url'], jsonObj)
            # else:
            #     for link_url in jsonObj['LinkedEntity']:
            #         githubDict[ jsonObj['url']]['LinkedEntity'].add( link_url)
            #===================================================================

    
    print 'SIZE=',len(githubDict)                  


def writeBack(githubDict):
    
    opDir = 'C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\'
    
    j_jl_op = open(opDir+'Github.jl','wb')
    
    print 'Start'
    
    for k, jsonObj in githubDict.iteritems():        
        j_jl_op.write(json.dumps(jsonObj)+linesep)
    
    print 'END'
#############################################################################################################

rootDir = 'C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\extras\\github\\'

aggregatedFilesList = [ rootDir+hfile for hfile in listdir(rootDir)]


for dataFile in aggregatedFilesList:
    extract_and_consolidate_GITHUB(dataFile)

writeBack(githubDict)    
      
