'''
Created on Nov 30, 2017

@author: anand
'''

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

global tableau_technology_tp, tableau_projects_d, networkx_txt, tableau_address_cou, tableau_address_cty, tableau_technology_pt
tableau_technology_tp = {}; tableau_projects_d = {}; networkx_txt = [] ; tableau_address_cou = {}; tableau_address_cty = {}; tableau_technology_pt = {}

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
            rearrangeSet = set(['india','united states','united kingdom','canada'])
            for rowList in csvR:
                rowList[0] = rowList[0].lower()
                if rowList[1].lower() in rearrangeSet:
                    rowList[3] = rowList[1].lower()
                    rowList[1] = ''
                    
                addrDict[rowList[0]] = [rowList[1], rowList[3] ]   # city and country
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

def tableau_technology(techList, personUrl):
    global tableau_technology_pt, tableau_technology_tp
    for tech in techList:
        tableau_technology_tp.setdefault(tech,set())
        tableau_technology_tp[tech].add( personUrl)
    
    tableau_technology_pt.setdefault(personUrl, set())
    tableau_technology_pt[personUrl] = tableau_technology_pt[personUrl] | set(techList)

def print_network_analysis():
    global tableau_technology_pt, tableau_technology_tp
    
    #get 10 most popular tech
    tech_popularity_list = []
    for k,v in tableau_technology_tp.iteritems():
        tech_popularity_list.append([k, len(v) ])
    tech_popularity_list = sorted(tech_popularity_list, key = lambda x:x[1], reverse = True)
    
    for tech, _ in tech_popularity_list[:20]:
        other_tech_countDict = {}
        
        for personId in list( tableau_technology_tp[tech]):
            
            for found_tech in list(tableau_technology_pt[personId]):
                if found_tech == tech: continue
                
                other_tech_countDict.setdefault(found_tech,0)
                other_tech_countDict[found_tech]+=1
        
        other_tech_countList = []
        for k,v in other_tech_countDict.iteritems():
            other_tech_countList.append([k, v ])
        other_tech_countList = sorted(other_tech_countList, key = lambda x:x[1], reverse = True)       
        other_tech_countList = [ str(x[0]) for x in other_tech_countList[:12] ]   #<---------------------------------------------------------
        other_tech_countList = ', '.join(other_tech_countList )
        
        
        print tech, ': ', other_tech_countList
            
        
def tableau_projects(projectList, userUrl):
    global tableau_projects_d, networkx_txt
    
    for project in projectList:
        tableau_projects_d.setdefault(project,0)
        tableau_projects_d[project]+=1
        
        networkx_txt.append([userUrl, project])

def tableau_address(addressList):
    global tableau_address_cou, tableau_address_cty
    
    if addressList[0] != '':
        key = addressList[0]+','+addressList[1]
        tableau_address_cty.setdefault(key,0)
        tableau_address_cty[ key]+=1
    
    if addressList[1] != '':
        tableau_address_cou.setdefault(addressList[1],0)
        tableau_address_cou[ addressList[1]]+=1
        
def save_for_tableau():
    global tableau_technology_d, tableau_projects_d, networkx_txt, tableau_address_cou, tableau_address_cty
    
    with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\tableau\\tableau_technology.csv','wb') as f:
        csvW = csv.writer(f, delimiter = ',', quoting = csv.QUOTE_ALL)
        for k,v in tableau_technology_d.iteritems():
            csvW.writerow([k,v])
        print 'tech done'
    
    with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\tableau\\tableau_projects.csv','wb') as f:
        csvW = csv.writer(f, delimiter = ',', quoting = csv.QUOTE_ALL)
        for k,v in tableau_projects_d.iteritems():
            csvW.writerow([k,v])
        print 'projects done'
    
    with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\tableau\\tableau_address_cou.csv','wb') as f:
        csvW = csv.writer(f, delimiter = ',', quoting = csv.QUOTE_ALL)
        for k,v in tableau_address_cou.iteritems():
            csvW.writerow([k,v])
        print 'country done'
    
    with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\tableau\\tableau_address_cty.csv','wb') as f:
        csvW = csv.writer(f, delimiter = ',', quoting = csv.QUOTE_ALL)
        for k,v in tableau_address_cty.iteritems():
            csvW.writerow([k,v])
        print 'city done'  
        
    with open('C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\tableau\\networkx_projects.txt','wb') as f:
        for user, project in networkx_txt:
            f.write( user + ' '+ project+linesep)
        print 'networkx projects done'  
##################################################################################################################
##################################################################################################################


def standardize_github(dataList):
    
    print 'Formatting Github'
    count = 1
    for jsonObj in dataList:
        
        

        #tableau_address( getAddressList(jsonObj['address']))
        tableau_technology( map(string.lower, jsonObj['technology']) , jsonObj['url'].lower() )
        #tableau_projects( map(string.lower, jsonObj['projects']), jsonObj['url'].lower() )

        if count % 1000 == 0:
            print count ,'/', len(dataList)
        count+=1

def standardize_hackerrank(dataList):
    
    print 'Formatting Hackerrank'
    count = 1    
    for jsonObj in dataList:
        
        if count == 38673:
            pass
        tableau_address( getAddressList(jsonObj['HR_Location']))
        if not type(jsonObj['HR_prog_lang_known']) == list:
            if jsonObj['HR_prog_lang_known'] in ['',None] : jsonObj['HR_prog_lang_known'] = []
            else:
                jsonObj['HR_prog_lang_known'] = [ jsonObj['HR_prog_lang_known'] ]
        elif jsonObj['HR_prog_lang_known'] in [None, [''],[None] ]:
            jsonObj['HR_prog_lang_known'] = []
        try:
            tableau_technology( map(string.lower, jsonObj['HR_prog_lang_known'] ) )
        except Exception as _:
            pass
        
        if count % 1000 == 0:
            print count ,'/', len(dataList)
        count+=1

def standardize_leetcode(dataList):

    count = 1    
    print 'Formatting Leetcode'
    for jsonObj in dataList:

        tableau_address( getAddressList(jsonObj['Country']))
        tableau_technology( map(string.lower, [jsonObj['Program_Language']] ) )
        if count % 1000 == 0:
            print count ,'/', len(dataList)
        count+=1
            
def standardize_stackoverflow(dataList):
    
    print 'Formatting stackoverflow'
    count = 1
    for jsonObj in dataList:
        
        #if 'Location' not in jsonObj: jsonObj['Location'] = ''
        #tableau_address( getAddressList(jsonObj['Location']))
        
        if 'Skills' not in jsonObj: jsonObj['Skills'] = []
        tableau_technology( map(string.lower, jsonObj['Skills'] )  , jsonObj['Profile_URL'].lower())
        
        if count % 1000 == 0:
            print count ,'/', len(dataList)
        count+=1

def standardize_github_IO_blog(dataList):
    
    print 'Formatting github IO'
    for jsonObj in dataList:
        
                
        tableau_technology( map(string.lower, jsonObj['candidate_skills'] ) )



#############################################################################################################

ipDir = 'C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\extras\\'
opDir = 'C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\'

aggregatedFilesList = [(hfile.split('.')[0], ipDir+'\\'+hfile) for hfile in listdir(ipDir) \
                       if path.isfile(ipDir+'\\'+hfile) and hfile.split('.')[1]=='jl']

for fileSource, fileName in aggregatedFilesList:
    
    dataList = readFile(fileName)
    print '\n'
    print fileSource, 'data read'
    
    if fileSource == 'Github':
        standardizedList = standardize_github(dataList)
        del standardizedList
        continue
        
    if fileSource == 'Stackoverflow':
        standardizedList = standardize_stackoverflow(dataList)
        del standardizedList
        continue
    
    
#===============================================================================
#     if fileSource == 'Leetcode':
#         standardizedList = standardize_leetcode(dataList)
#         del standardizedList
#         continue
#     
#     if fileSource == 'Hackerrank':
#         standardizedList = standardize_hackerrank(dataList)
#         del standardizedList
#         continue
#     
#     if fileSource == 'Github_IO':
#         standardizedList = standardize_github_IO_blog(dataList)
#         writeFile(standardizedList, opDir+'GithubIO_c.jl')
#         del standardizedList
#         continue
# 
# save_for_tableau()
#===============================================================================

print_network_analysis()