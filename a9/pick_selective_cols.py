'''
Created on Nov 13, 2017

@author: anand
'''
import json

#===============================================================================
# fileName = 'hackerrank.jl'
# cols_to_pick = ['HR_Profile_URL','HR_Picture','HR_Location', 'HR_Name', 'HR_About_me']
# opFile = open('hr.jl','wb')
#===============================================================================

fileName = 'stackoverflow.json'
cols_to_pick = ['Name','Profile_URL','Location','Reference_URL']
opFile = open('sof.jl','wb')

with open(fileName) as f:
    for line in f:
        opDict = {}
        jsonObj = json.loads(line[:-2])
        
        for col in cols_to_pick:
            if col in jsonObj and jsonObj[col]!=None:
                opDict[col] = jsonObj[col]
        
        if opDict:
            opFile.write(json.dumps(opDict)+'\n')

opFile.close()
print 'Done'