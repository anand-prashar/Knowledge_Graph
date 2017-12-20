'''
Created on Oct 23, 2017
@author: anand
'''
import json
from lxml import html
from os import listdir, getcwd, linesep, stat

    
def extract_to_json(htmlDirectory, outputJsonFile):
    
    fp = open(outputJsonFile, 'wb')
    filesLeft = len(htmlDirectory)
    
    errLog = open('ERROR.log','wb')
    
    for htmlFile in htmlDirectory:
        try:
            
            JsonObject = {}
            with open(htmlFile,'rb') as rh:
                JsonObject['raw_content'] = rh.read()
            
            domTree = html.parse( open(htmlFile) )
      
            
            #JsonObject['Name']=domTree.xpath("""//h2[@class="user-card-name"]/text()[1]""")[0].strip()
            JsonObject['doc_id'] = domTree.xpath("""//div[@class="avatar-card"]//a/@href""")[0].split('/')[-2]
            JsonObject['url']= domTree.xpath("""//div[@class="avatar-card"]//a/@href""")[0]
            
#            location  = domTree.xpath("""//div[@class="col-right col-4"]//li[svg/@class = "svg-icon iconLocation"]""")
#            if location: 
#                location = [address.strip() for address in location[0].xpath("./text()") if address.strip()!='']
#                JsonObject['Location'] = location[0]
                 

             
#            githubID = domTree.xpath("""//div[@class="col-right col-4"]//li[svg/@class = "svg-icon iconGitHub"]/a/@href""")
#            if githubID:
#                JsonObject['Github'] = githubID[0]   
             
#            blogURL  = domTree.xpath("""//div[@class="col-right col-4"]//li[svg/@class = "svg-icon iconLink"]/a/@href""")
#            if blogURL:
#                if 'github' in blogURL[0].lower() and 'Github' not in JsonObject:
#                    JsonObject['Github'] = blogURL[0]

                
            
            fp.write( json.dumps(JsonObject)+linesep )
            print '--> Files left: '+str(filesLeft); filesLeft-=1
        
        except Exception as _: 
            print 'FAILED TO OPEN : '+htmlFile
            errLog.write(htmlFile+'\n')
            
    fp.close()   
    errLog.close()
    
    print 'Extracted to: '+outputJsonFile 
   
#############################################################################################################

currentDirList = ['C:\\Users\\anand\\Stackoverflow\\0-1M']

for currentDir in currentDirList:
    #aggregatedFilesList = []
    aggregatedFilesList = [currentDir+'\\'+hfile for hfile in listdir(currentDir) \
                            if hfile.split('.')[-1]=='html' and stat(currentDir+'\\'+hfile).st_size/1024 > 80]

    if aggregatedFilesList == []: continue
    
    if len(aggregatedFilesList) >100: aggregatedFilesList=aggregatedFilesList[200:300]
    
    currentDir = currentDir.split('\\')[-1]
    
    extract_to_json(aggregatedFilesList, 'Stackoveflow_Extras_cdr'+'.jl')