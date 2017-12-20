'''
Created on Nov 23, 2017

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


def readFile(fileName):
    
    dataList = []
    with open(fileName,'rb') as f:
        for row in f:
            if row=='': continue
            dataList.append( json.loads(row))
    
    return dataList

def writeFile(standardizedList, fileName):
    
    with open(fileName,'wb') as f:
        for row in standardizedList:
            if row=='': continue
            f.write( json.dumps(row)+linesep)
    
    print 'Written'
    
##################################################################################################################

def getAddressList(addrString):
    if addrString in [None,''] : return ['','','']
    
    addrString = addrString.lower().strip()
    global addrDict, addrList
    
    if not addrDict:
        addrDict = {}
        addrList = []
        with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\Reference\\locationFile_cleaned_OK.csv','rb') as f:
            index=0
            csvR = csv.reader(f, delimiter=',',quoting=csv.QUOTE_MINIMAL)
            for rowList in csvR:
                rowList[0] = rowList[0].lower()
                addrDict[rowList[0]] = rowList[1:4]
                addrList.append( (index, rowList[0]))
                index+=1
    
    if addrString in addrDict:
        return addrDict[addrString]
    addressSimList = [ (x[0], Lev_Ratio(unicode(addrString), unicode(x[1]))) for x in addrList ]
    addressSimList = sorted( addressSimList, key= lambda x:x[1], reverse=True)
    
    return addrDict [ addrList[addressSimList[0][0]][1]]

def getLinkedEntityList(url):
    if url in [None,''] : return []
    url = url.lower()
    
    global entityMappingDict
    
    if not entityMappingDict:
        # 1st hit run
        with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\gitHub_linking_mapper.csv','rb') as f:
            
            csvR = csv.reader(f, delimiter=',',quoting=csv.QUOTE_ALL)
            for rowList in csvR:
                rowList = [x.lower() for x in rowList if x!='']
                for row in rowList:
                    if 'https://leetcode.com' in row: row=row[:-1]  #ignore last /
                    entityMappingDict.setdefault(row, rowList)

    
    if url in entityMappingDict:
        return entityMappingDict[url]
    return []

def getCompany(lookupStr):
    if lookupStr in [None,''] : return ''
    
    global companyDict, companyList
    lookupStr = lookupStr.lower().strip()

    if not companyDict:

        with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\Reference\\locationFile_cleaned_OK.csv','rb') as f:
            csvR = csv.reader(f, delimiter=',',quoting=csv.QUOTE_MINIMAL)
            for rowList in csvR:
                rowList[0] = rowList[0].lower()
                rowList[1] = ''.join([ c for c in rowList[1] if ( 90<ord(c)<123 or ord(c)==32 or 47<ord(c)<58)])
            
                companyDict.setdefault(rowList[0], rowList[1])
                companyList.append(rowList[0])
                
    
    if lookupStr in companyDict:
        return companyDict[lookupStr]
    companySimList = [ (x, Lev_Ratio(unicode(lookupStr), unicode(x))) for x in companyList ]
    companySimList = sorted( companySimList, key= lambda x:x[1], reverse=True)
    
    return companyDict [ companySimList[0][0] ]  

def getUniversity(lookupStr):
    if lookupStr in [None,''] : return ''
    
    global universityDict, universityList   
    lookupStr = lookupStr.lower().strip()

    if not universityDict:

        with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\Reference\\universityFile_cleaned_OK.csv','rb') as f:
            
            csvR = csv.reader(f, delimiter=',',quoting=csv.QUOTE_ALL)
            for rowList in csvR:
                rowList[0] = rowList[0].lower()
                rowList[1] = ''.join([ c for c in rowList[1] if ( 90<ord(c)<123 or ord(c)==32 or 47<ord(c)<58)])
            
                universityDict.setdefault(rowList[0], rowList[1])
                universityList.append(rowList[0])
                
    
    if lookupStr in universityDict:
        return universityDict[lookupStr]
    univSimList = [ (x, Lev_Ratio(unicode(lookupStr), unicode(x))) for x in universityList ]
    univSimList = sorted( univSimList, key= lambda x:x[1], reverse=True)
    
    return universityDict [ univSimList[0][0] ]  

##################################################################################################################
##################################################################################################################


def standardize_github(dataList):
    
    print 'Formatting Github'
    count=0
    
    standardizedList = []
    for jsonObj in dataList:
        opJl = {}
        opJl['candidate_name'] = jsonObj['name'].lower()
        opJl['url'] = jsonObj['url'].lower()
        opJl['doc_id'] = 'ghub_'+jsonObj['url'][19:].lower()
        opJl['candidate_pic_url'] = ''
        opJl['candidate_occoupation'] = ''
        opJl['candidate_education'] = ''

        opJl['city_name'], opJl['state'], opJl['country'] = getAddressList(jsonObj['address'])
        opJl['candidate_skills'] = map(string.lower, jsonObj['technology'])
        opJl['candidate_linkedentity'] = getLinkedEntityList(jsonObj['url'])

        opJl['candidate_projects'] = map(string.lower, jsonObj['projects'])
        opJl['candidate_glance'] =   map(string.lower, jsonObj['keywords'])
        opJl['raw_content'] = '.'
        
        standardizedList.append(opJl)
        count+=1
        if count%1000==0: print count,' / ',len(dataList)
    
    return standardizedList


def standardize_hackerrank(dataList):
    
    print 'Formatting Hackerrank'
    count=0
    
    standardizedList = []
    for jsonObj in dataList:
        opJl = {}
        if jsonObj['HR_Name'] == None:
            opJl['candidate_name'] = ''
        else:
            opJl['candidate_name'] = jsonObj['HR_Name'].lower()
        opJl['url'] = jsonObj['HR_Profile_URL'].lower()
        opJl['candidate_pic_url'] = jsonObj['HR_Picture'].lower()
        
        opJl['doc_id'] = 'hr_'+jsonObj['HR_Profile_URL'][27:].lower()
        opJl['candidate_occoupation'] = getCompany( jsonObj['HR_Job'] )
        opJl['candidate_education'] = getUniversity(jsonObj['HR_University'])

        opJl['city_name'], opJl['state'], opJl['country'] = getAddressList(jsonObj['HR_Location'])
        
        if 'HR_prog_lang_known' in jsonObj and jsonObj['HR_prog_lang_known']!=None: 
            opJl['candidate_skills'] = map(string.lower, jsonObj['HR_prog_lang_known'])
        else: opJl['candidate_skills'] = []
        opJl['candidate_linkedentity'] = getLinkedEntityList(jsonObj['HR_Profile_URL'])
        
        opJl['candidate_projects'] = ['']
        
        glance_data = []
        if 'HR_About_me' in jsonObj and jsonObj['HR_About_me']!=None: glance_data.append(str( jsonObj['HR_About_me']).lower() )
        if 'HR_Badges' in jsonObj and jsonObj['HR_Badges']!=None: glance_data.append(str( jsonObj['HR_Badges']).lower() )
        opJl['candidate_glance'] =   glance_data
        opJl['raw_content'] = '.'
        
        standardizedList.append(opJl)
        count+=1
        if count%1000==0: print count,' / ',len(dataList)        
    
    return standardizedList    


def standardize_leetcode(dataList):
    
    print 'Formatting Leetcode'
    count=0
            
    standardizedList = []
    for jsonObj in dataList:
        opJl = {}
        opJl['candidate_name'] = jsonObj['name'].lower()
        opJl['url'] = jsonObj['url'][:-1].lower()
        opJl['candidate_pic_url'] = jsonObj['image'].lower()
        
        opJl['doc_id'] = 'lc_'+jsonObj['url'][21:-1].lower()
        opJl['candidate_occoupation'] = getCompany( jsonObj['Occupation'] )
        opJl['candidate_education'] = getUniversity(jsonObj['Education'])

        opJl['city_name'], opJl['state'], opJl['country'] = getAddressList(jsonObj['Country'])
        opJl['candidate_skills'] = map(string.lower, jsonObj['Program_Language'])
        opJl['candidate_linkedentity'] = getLinkedEntityList(jsonObj['url'])

        opJl['candidate_projects'] = ['']
        opJl['candidate_glance'] =   map(string.lower, [ str(jsonObj['Program_quality']) ] )
        opJl['raw_content'] = '.'
        
        standardizedList.append(opJl)
        count+=1
        if count%1000==0: print count,' / ',len(dataList)
    
    return standardizedList   

def standardize_stackoverflow(dataList):
    
    print 'Formatting stackoverflow'
    count=0
    
    standardizedList = []
    for jsonObj in dataList:
        opJl = {}
        opJl['candidate_name'] = jsonObj['Name'].lower()
        opJl['url'] = jsonObj['Profile_URL'].lower()
        opJl['candidate_pic_url'] = ''
        
        opJl['doc_id'] = 'sof_'+ '_'.join(jsonObj['Profile_URL'][32:].split('/'))
        opJl['candidate_occoupation'] =''
        opJl['candidate_education'] = ''

        if not( 'Location' in jsonObj and jsonObj['Location'] != None):
            jsonObj['Location'] = ''
        opJl['city_name'], opJl['state'], opJl['country'] = getAddressList(jsonObj['Location'])
        
        if not( 'Skills' in jsonObj and jsonObj['Skills'] != None):
            jsonObj['Skills'] = []
        opJl['candidate_skills'] = map(string.lower, jsonObj['Skills'])
        opJl['candidate_linkedentity'] = getLinkedEntityList(jsonObj['Profile_URL'])

        opJl['candidate_projects'] = ['']
        if 'Twitter' in jsonObj and jsonObj['Twitter'] != None:
            opJl['candidate_glance'] = [ jsonObj['Twitter'].lower() ]
        else: opJl['candidate_glance'] = []
        opJl['raw_content'] = '.'
        
        standardizedList.append(opJl)
        count+=1
        if count%1000==0: print count,' / ',len(dataList)
    
    return standardizedList 


def standardize_github_IO_blog(dataList):
    
    print 'Formatting github IO'
    count=0
    
    standardizedList = []
    for jsonObj in dataList:
        opJl = {}
        opJl['candidate_name'] = jsonObj['candidate_name'].lower()
        opJl['url'] = jsonObj['url'].lower()
        opJl['candidate_pic_url'] = ''
        
        opJl['doc_id'] = 'ghio_'+jsonObj['url'][8:-10].lower()
        opJl['candidate_occoupation'] = ''
        opJl['candidate_education'] = ''

        opJl['city_name'], opJl['state'], opJl['country'] = getAddressList('')
        opJl['candidate_skills'] = map(string.lower, jsonObj['candidate_skills'])
        opJl['candidate_linkedentity'] = getLinkedEntityList(jsonObj['url'])

        opJl['candidate_projects'] = ['']
        opJl['candidate_glance'] =   ['']
        opJl['raw_content'] = '.'
        
        standardizedList.append(opJl)
        count+=1
        if count%1000==0: print count,'/',len(dataList)
    
    return standardizedList 


#############################################################################################################

ipDir = 'C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\extras\\'
opDir = 'C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\'

aggregatedFilesList = [(hfile.split('.')[0], ipDir+'\\'+hfile) for hfile in listdir(ipDir) \
                       if path.isfile(ipDir+'\\'+hfile) and hfile.split('.')[1]=='jl']

for fileSource, fileName in aggregatedFilesList:
    
    dataList = readFile(fileName)
    print '\n'
    print fileSource, 'data read'
    #===========================================================================
    # if fileSource == 'Github':
    #     standardizedList = standardize_github(dataList)
    #     writeFile(standardizedList, opDir+'Github_c.jl')
    #     del standardizedList
    #     continue
    #===========================================================================
        
    if fileSource == 'Stackoverflow':
        standardizedList = standardize_stackoverflow(dataList)
        writeFile(standardizedList, opDir+'Stackoverflow_c.jl')
        del standardizedList
        continue
    
    #===========================================================================
    # if fileSource == 'Leetcode':
    #     standardizedList = standardize_leetcode(dataList)
    #     writeFile(standardizedList, opDir+'Leetcode_c.jl')
    #     del standardizedList
    #     continue
    #===========================================================================
    
    #===========================================================================
    # if fileSource == 'Hackerrank':
    #     standardizedList = standardize_hackerrank(dataList)
    #     writeFile(standardizedList, opDir+'Hackerrank_c.jl')
    #     del standardizedList
    #     continue
    #===========================================================================
    
    #===========================================================================
    # if fileSource == 'Github_IO':
    #     standardizedList = standardize_github_IO_blog(dataList)
    #     writeFile(standardizedList, opDir+'GithubIO_c.jl')
    #     del standardizedList
    #     continue
    #===========================================================================
         
