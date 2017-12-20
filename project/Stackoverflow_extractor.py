'''
Created on Sep 28, 2017

@author: anand
'''

import json
from lxml import html
from os import listdir, getcwd, linesep

    
def extract_to_json(htmlDirectory, outputJsonFile):
    
    fp = open(outputJsonFile, 'w')
    fp.write('[')
    filesLeft = len(htmlDirectory)
    
    errLog = open('ERROR.log','w')
    
    for htmlFile in htmlDirectory:
        try:
            
            JsonObject = {}
            domTree = html.parse( open(htmlFile) )
      
            
            Name       = domTree.xpath("""//h2[@class="user-card-name"]/text()[1]""")
            profileURL = domTree.xpath("""//div[@class="avatar-card"]//a/@href""")[0]
            profileID  = profileURL.split('/')[-2]
            JsonObject['Name']=Name[0].strip()
            JsonObject['ID'] = profileID
            JsonObject['Profile_URL']= profileURL
            
            location  = domTree.xpath("""//div[@class="col-right col-4"]//li[svg/@class = "svg-icon iconLocation"]""")
            if location: 
                location = [address.strip() for address in location[0].xpath("./text()") if address.strip()!='']
                JsonObject['Location'] = location[0]
                
            twitterID = domTree.xpath("""//div[@class="col-right col-4"]//li[svg/@class = "svg-icon iconTwitter"]/a/@href""")
            if twitterID:
                JsonObject['Twitter'] = twitterID[0]
            
            githubID = domTree.xpath("""//div[@class="col-right col-4"]//li[svg/@class = "svg-icon iconGitHub"]/a/@href""")
            if githubID:
                JsonObject['Github'] = githubID[0]   
            
            blogURL  = domTree.xpath("""//div[@class="col-right col-4"]//li[svg/@class = "svg-icon iconLink"]/a/@href""")
            if blogURL:
                if 'github' in blogURL[0].lower() and 'Github' not in JsonObject:
                    JsonObject['Github'] = blogURL[0]
                else:
                    JsonObject['Reference_URL'] = blogURL[0]
                
            skillsSubTrees = domTree.xpath("""//div[@class="row g-column p-top-tags"]//div[@class="g-col g-row -tag-group"]""")
            for skillNode in skillsSubTrees:
                skillName  = skillNode.xpath(""".//div[@class="g-col fl-none ai-center"]/a/text()""")
                skillScore = skillNode.xpath(""".//div[@class="g-col ai-center g-row _gutters"][1]//span[2]/text()""")
                
                if skillName and skillScore:
                    JsonObject.setdefault('Skills',{})
                    JsonObject['Skills'][skillName[0] ] = skillScore[0]
            
            fp.write( json.dumps(JsonObject)+ ","+linesep );
            print profileID+'--> Files left: '+str(filesLeft); filesLeft-=1
        
        except Exception as e: 
            print 'FAILED TO OPEN : '+htmlFile
            errLog.write(htmlFile+'\n')
            
    fp.write('\n]')
    fp.close()   
    errLog.close()
    
    print 'Extracted to: '+outputJsonFile 
   
#############################################################################################################

currentDirList = [getcwd()]
#rootDir = 'C:\\Users\\anand\\Stackoverflow'
#currentDirList = [rootDir+'\\'+childDir for childDir in listdir(rootDir)]

aggregatedFilesList = []
for currentDir in currentDirList:
    aggregatedFilesList += [currentDir+'\\'+hfile for hfile in listdir(currentDir) if hfile.split('.')[-1]=='html']

if aggregatedFilesList == []: exit()
extract_to_json(aggregatedFilesList, 'Stackoverflow_scrap_1.json')

    