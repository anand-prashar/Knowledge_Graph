'''
Created on Oct 17, 2017

@author: anand
'''
import json
import csv
from os import listdir, linesep
import sys; reload(sys); sys.setdefaultencoding("utf-8")

global blogDict, githubDict, technologyDict, companyDict, locationDict, universityDict, possibleGitUsersDict, SOF, HRRK, LTCD
blogDict={}; githubDict={}; technologyDict={}; companyDict={}; locationDict={}; universityDict={}
possibleGitUsersDict={}

SOF = {}; HRRK = {}; LTCD = {}
    
def extract_and_consolidate_hackerrank(dataFile):
    print 'Processing in hackerrank: ', dataFile.split('\\')[-1]
    
    global blogDict, githubDict, technologyDict, companyDict, locationDict, universityDict, HRRK
    edgeCases = set(['', None])
    
    def get_correct_github_url(someGitUrl):
        temp = someGitUrl.lower()
        if len( temp.split('https://github.com/'))==2:
            return someGitUrl, True
        
        if len(someGitUrl.split('github.com/'))==2:
            return 'https://github.com/' + someGitUrl.split('github.com/')[1], True
        return someGitUrl, False
    
    with open(dataFile) as f:
        for line in f:
            if line == '': continue
            jsonObj = json.loads(line)
            
            # github, blog save
            if ('HR_Blog' in jsonObj) and jsonObj['HR_Blog'] not in edgeCases:
                jsonObj['HR_Blog'], isGitURL = get_correct_github_url(jsonObj['HR_Blog'])
                if isGitURL:
                    githubDict.setdefault(jsonObj['HR_Blog'], [])
                    githubDict [jsonObj['HR_Blog']].append( jsonObj['HR_Profile_URL'])
                else:
                    blogDict.setdefault(jsonObj['HR_Blog'], [])
                    blogDict [jsonObj['HR_Blog']].append( jsonObj['HR_Profile_URL'])
            else:
                probableGitUrl = 'https://github.com/'+ jsonObj['HR_Profile_URL'].split('https://www.hackerrank.com/')[1]
                possibleGitUsersDict.setdefault( probableGitUrl,[ jsonObj['HR_Profile_URL']] )
                    
            #technology save
            if ('HR_prog_lang_known' in jsonObj) and jsonObj['HR_prog_lang_known'] != None:
                for tech in jsonObj['HR_prog_lang_known']:
                    technologyDict.setdefault(tech, [])
                    #technologyDict [tech].append( jsonObj['HR_Profile_URL'])   <---------------------------------
            
            #job save
            if ('HR_Job' in jsonObj) and jsonObj['HR_Job'] not in edgeCases:
                companyDict.setdefault(jsonObj['HR_Job'], [])
                #companyDict [jsonObj['HR_Job']].append( jsonObj['HR_Profile_URL'])
                
            #University save
            if ('HR_University' in jsonObj) and jsonObj['HR_University'] not in edgeCases:
                universityDict.setdefault(jsonObj['HR_University'], [])
                #universityDict [jsonObj['HR_University']].append( jsonObj['HR_Profile_URL'])
                
            #location save
            if ('HR_Location' in jsonObj) and jsonObj['HR_Location'] not in edgeCases:
                locationDict.setdefault(jsonObj['HR_Location'], [])
                #locationDict [jsonObj['HR_Location']].append( jsonObj['HR_Profile_URL'])
                
            #HRRK.setdefault(jsonObj['HR_Profile_URL'], jsonObj)  #<-------------------------------------------------------------
                
    print 'Done '

###########################################
def extract_and_consolidate_stackoverflow(dataFile):
    
    print 'Processing in Stackoverflow: ', dataFile.split('\\')[-1]
    
    global blogDict, githubDict, technologyDict, locationDict, SOF
    
    def get_correct_github_url(someGitUrl):
        temp = someGitUrl.lower()
        if len( temp.split('https://github.com/'))==2:
            return someGitUrl, True
        elif len( temp.split('github.com/'))==2:
            return 'https://github.com/' + someGitUrl.split('github.com/')[1]  , True
        else:
            return someGitUrl, False  
        
    edgeCases = set(['', None])
    
    with open(dataFile) as f:
        for line in f:
            #if line in ['',']']: continue
            #line = line.strip()
            try:
                #if line[0]=='[':line=line[1:-1]
                #else: line = line[:-1]
            
                jsonObj = json.loads(line)
                
                if jsonObj['Profile_URL'] == 'https://stackoverflow.com/users/88868/enriquein':
                    pass
                
            except Exception as _:
                print line
                continue   
            #github save    
            isGitProfile = False    
            if ('Github' in jsonObj) and jsonObj['Github'] not in edgeCases: 
                    jsonObj['Github'], isGitProfile = get_correct_github_url(jsonObj['Github'])        
                    if isGitProfile:
                        githubDict.setdefault(jsonObj['Github'], [])
                        githubDict [jsonObj['Github']].append( jsonObj['Profile_URL'])  
                    
            # blog save
            if not isGitProfile:
                if 'Github' in jsonObj:
                    blogDict.setdefault(jsonObj['Github'], [])
                    blogDict [jsonObj['Github']].append( jsonObj['Profile_URL'])  
                
                probableGitUrl = 'https://github.com/'+ jsonObj['Profile_URL'].split('/')[-1]
                possibleGitUsersDict.setdefault( probableGitUrl,[ jsonObj['Profile_URL']] )
                
            if ('Reference_URL' in jsonObj) and jsonObj['Reference_URL'] not in edgeCases:
                blogDict.setdefault(jsonObj['Reference_URL'], [])
                blogDict [jsonObj['Reference_URL']].append( jsonObj['Profile_URL'])
                    
            #technology save
            if ('Skills' in jsonObj) and jsonObj['Skills'] not in ( None,[]):
                for tech in list(jsonObj['Skills']):
                    technologyDict.setdefault(tech, [])
                    #technologyDict [tech].append( jsonObj['HR_Profile_URL'])   <---------------------------------
 
            #location save
            if ('Location' in jsonObj) and jsonObj['Location'] not in edgeCases:
                locationDict.setdefault(jsonObj['Location'], [])
                ###############################################locationDict [jsonObj['HR_Location']].append( jsonObj['HR_Profile_URL'])
            
            #SOF.setdefault(jsonObj['Profile_URL'], jsonObj)  #<------------------------------------------------------------------
    print 'Done '

###########################################

def extract_and_consolidate_Leetcode(dataFile):
    print 'Processing in Leetcode: ', dataFile.split('\\')[-1]
    
    global blogDict, githubDict, technologyDict, companyDict, locationDict, universityDict, LTCD
    edgeCases = set(['', None])
    
    with open(dataFile) as f:
        for line in f:
            if line == '': continue
            jsonObj = json.loads(line)
            
            
            
            # github, blog save
            if ('gitHub' in jsonObj) and jsonObj['gitHub'] not in edgeCases:
                githubDict.setdefault(jsonObj['gitHub'], [])
                githubDict [jsonObj['gitHub']].append( jsonObj['url'])

            else:
                probableGitUrl = 'https://github.com/'+ jsonObj['url'][21:][:-1]
                possibleGitUsersDict.setdefault( probableGitUrl,[ jsonObj['url']] )
                    
            #technology save
            if ('Program_Language' in jsonObj) and jsonObj['Program_Language'] != None:
                technologyDict.setdefault(jsonObj['Program_Language'], [])
                #technologyDict [tech].append( jsonObj['HR_Profile_URL'])   <---------------------------------
            
            #job save
            if ('Occupation' in jsonObj) and jsonObj['Occupation'] not in edgeCases:
                companyDict.setdefault(jsonObj['Occupation'], [])
                #companyDict [jsonObj['Occupation']].append( jsonObj['url'])
                
            #University save
            if ('Education' in jsonObj) and jsonObj['Education'] not in edgeCases:
                universityDict.setdefault(jsonObj['Education'], [])
                #universityDict [jsonObj['Education']].append( jsonObj['url'])
                
            #location save
            if ('Country' in jsonObj) and jsonObj['Country'] not in edgeCases:
                locationDict.setdefault(jsonObj['Country'], [])
                #locationDict [jsonObj['HR_Location']].append( jsonObj['HR_Profile_URL'])
                
            
            #LTCD.setdefault(jsonObj['url'], jsonObj)  #<------------------------------------------------------------------------
                
    print 'Done '
    
###########################################

def save_results_to_csv(opDir):
    global blogDict, githubDict, technologyDict, companyDict, locationDict, universityDict, possibleGitUsersDict
    
    mapping = {'blogFile.csv': blogDict, 'technologyFile.csv': technologyDict, 'githubFile.csv': githubDict,\
               'companyFile.csv': companyDict, 'locationFile.csv': locationDict, 'universityFile.csv': universityDict,
               'possibleGithubUsers.csv': possibleGitUsersDict }
    
    for saveFileName, globalDict in mapping.iteritems():
        print 'Writing File: ', saveFileName
        f=open(opDir+'\\'+saveFileName,'wb')
        csvObj = csv.writer( f, delimiter = ',', quoting=csv.QUOTE_ALL)
        
        for key, valList in globalDict.iteritems():
            if type(valList) != list: valList = [valList]
            csvObj.writerow([key]+valList)

        f.close()


#===============================================================================
# def merge_data_files():
#     global HRRK, LTCD, SOF
#     with open('Hackerrank.jl','wb') as fp:
#         for k,v in HRRK.iteritems():
#             fp.write( json.dumps(v)+linesep )
#     print 'HR DONE'
#     with open('Leetcode.jl','wb') as fp:
#         for k,v in LTCD.iteritems():
#             fp.write( json.dumps(v)+linesep )
#     print  'LEETCODE DONE'
#     with open('Stackoverflow.jl','wb') as fp:
#         for k,v in SOF.iteritems():
#             fp.write( json.dumps(v)+linesep )
#      
#     print 'FILES MERGED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
#===============================================================================
    
#############################################################################################################

rootDir = 'C:\\Users\\anand\\Google Drive\\Class - Knowledge Graph\\Project\\DATA\\'

aggregatedFilesList = [(hfile.split('.')[0], rootDir+'\\'+hfile) for hfile in listdir(rootDir)]

opDir = rootDir+'\\Reference\\'

for fileSource, dataFile in aggregatedFilesList:
    if fileSource == 'Hackerrank':
        extract_and_consolidate_hackerrank(dataFile)
    if fileSource == 'Stackoverflow':
        extract_and_consolidate_stackoverflow(dataFile)
    if fileSource == 'Leetcode':
        extract_and_consolidate_Leetcode(dataFile)
        
        

save_results_to_csv(opDir)

#merge_data_files()