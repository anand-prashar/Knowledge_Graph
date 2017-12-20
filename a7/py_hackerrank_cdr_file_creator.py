'''
Created on Oct 23, 2017
@author: anand
'''
import json
from lxml import html
from os import listdir, getcwd, linesep, path, stat

    
def extract_to_json(htmlDirectory, outputJsonFile):
    
    fp = open(outputJsonFile, 'wb')
    
    filesLeft = len(htmlDirectory)
    baseUrl = 'https://www.hackerrank.com/'
    errLog = open('ERROR.log','wb')
    
    for htmlFile in htmlDirectory:
        try:
            
            JsonObject = {}
            with open(htmlFile,'rb') as rh:
                JsonObject['raw_content'] = rh.read()
                
            domTree = html.parse( open(htmlFile) )
      
            JsonObject['doc_id'] = domTree.xpath("""//h5/span[@itemprop="alternateName"]/text()""")[0].strip()
            JsonObject['url'] = baseUrl+JsonObject['doc_id']
            
            
#            hr_name = domTree.xpath("""//h3[@class="mlT msB"]/text()""")
#            if hr_name: JsonObject['HR_Name'] = hr_name[0].strip()
#            else: JsonObject['HR_Name'] = None
              
#            hr_location = domTree.xpath("""//li[@itemprop="address"]/span/text()""")
#            if hr_location: JsonObject['HR_Location'] = hr_location[0].strip()
#            else: JsonObject['HR_Location'] = None
 
                 
            fp.write( json.dumps(JsonObject)+linesep )
            #filesLeft-=1; print '--> Files left: '+str(filesLeft)
        
        except Exception as _: 
            print 'FAILED IN FILE : '+htmlFile
            errLog.write(htmlFile+'\n')
            
    fp.close()   
    errLog.close()
    
    print 'Extracted to: '+outputJsonFile 
   
#############################################################################################################


currentDirList = ['C:\\Users\\anand\\Hackerrank Saved Html\\1-5000']

for currentDir in currentDirList:
    #aggregatedFilesList = []
    aggregatedFilesList = [currentDir+'\\'+hfile for hfile in listdir(currentDir) \
                            if hfile.split('.')[-1]=='html' and stat(currentDir+'\\'+hfile).st_size/1024 > 170]

    if aggregatedFilesList == []: continue
    
    if len(aggregatedFilesList) >100: aggregatedFilesList=aggregatedFilesList[:100]
    
    currentDir = currentDir.split('\\')[-1]
    
    extract_to_json(aggregatedFilesList, 'Hackerrank_Shiv_cdr_'+currentDir+'.jl')
    