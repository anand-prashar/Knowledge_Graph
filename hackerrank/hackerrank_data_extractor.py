'''
Created on Oct 17, 2017

@author: anand
'''
import json
from lxml import html
from os import listdir, getcwd, linesep, path

    
def extract_to_json(htmlDirectory, outputJsonFile):
    
    fp = open(outputJsonFile, 'w')
    
    filesLeft = len(htmlDirectory)
    baseUrl = 'https://www.hackerrank.com/'
    errLog = open('ERROR.log','w')
    
    for htmlFile in htmlDirectory:
        try:
            
            JsonObject = {}
            domTree = html.parse( open(htmlFile) )
      
            
            hr_name = domTree.xpath("""//h3[@class="mlT msB"]/text()""")
            if hr_name: JsonObject['HR_Name'] = hr_name[0].strip()
            else: JsonObject['HR_Name'] = None
            
            JsonObject['HR_Profile_URL'] = baseUrl+domTree.xpath("""//h5/span[@itemprop="alternateName"]/text()""")[0].strip()
            
            JsonObject['HR_Picture']  = domTree.xpath("""//div[@class="avatar avatar-profile"]/img/@src""")[0].strip()
            
            JsonObject['HR_follower_count'] = domTree.xpath("""//span[@class="btn-data js-follow-count"]/text()""")[0].strip()
            
            hr_about_me = domTree.xpath("""//div[@class="mjR"]/p[@itemprop="description"]/text()""")
            if hr_about_me: JsonObject['HR_About_me'] = hr_about_me[0].strip()
            else: JsonObject['HR_About_me'] = None
            
            hr_job = domTree.xpath("""//li[@itemprop="worksFor"]/span/text()""")
            if hr_job: JsonObject['HR_Job'] = hr_job[0].strip()
            else: JsonObject['HR_Job'] = None
            
            hr_university = domTree.xpath("""//li[@itemprop="affiliation"]/span/text()""")
            if hr_university: JsonObject['HR_University'] = hr_university[0].strip()
            else: JsonObject['HR_University'] = None
            
            hr_location = domTree.xpath("""//li[@itemprop="address"]/span/text()""")
            if hr_location: JsonObject['HR_Location'] = hr_location[0].strip()
            else: JsonObject['HR_Location'] = None
            
            hr_blog = domTree.xpath("""//li[@itemprop="sameAs"]/a/@href""")
            if hr_blog: JsonObject['HR_Blog'] = hr_blog[0].strip()
            else:  JsonObject['HR_Blog'] = None
            
                
            hr_prog_lang = domTree.xpath("""//div/ul[@class="unstyled psT psB"]/li[last()]/text()""")
            if hr_prog_lang: JsonObject['HR_prog_lang_known'] = hr_prog_lang[0].strip().split(', ')
            else: JsonObject['HR_prog_lang_known'] = None
                        
            JsonObject['HR_Badges'] = {}
            badgeSubTrees = domTree.xpath("""//div[@id="profile-tab-badges"]""")[0]
            #if badge List is not empty
            if not badgeSubTrees.xpath(""".//div[@class="emptyState_container"]"""):
                badgeSubTrees = badgeSubTrees.xpath(""".//div[@class="badge_image_container"]""")
                
                for badge_n_detail in badgeSubTrees:
                    badgeName = badge_n_detail.xpath("""./img[1]/@data-original-title""")[0].strip()
                    badgeStar = len( badgeSubTrees[0].xpath("""./img""")[1:])   # 1st element was badge name itself
                    badgePercentile = int( badge_n_detail.xpath("""./div/text()""")[0].strip()[:-2])
                    
                    JsonObject['HR_Badges'][badgeName] = {'stars(of 4)':badgeStar, 'percentile': badgePercentile}
                    
                
            fp.write( json.dumps(JsonObject)+linesep )
            filesLeft-=1; print '--> Files left: '+str(filesLeft)
        
        except Exception as _: 
            print 'FAILED IN FILE : '+htmlFile
            errLog.write(htmlFile+'\n')
            
    fp.close()   
    errLog.close()
    
    print 'Extracted to: '+outputJsonFile 
   
#############################################################################################################

rootDir = getcwd()
#rootDir = 'C:\\Users\anand\\Hackerrank Saved Html'
currentDirList = [rootDir+'\\'+childDir for childDir in listdir(rootDir) if path.isdir(childDir) ]


for currentDir in currentDirList:
    #aggregatedFilesList = []
    aggregatedFilesList = [currentDir+'\\'+hfile for hfile in listdir(currentDir) if hfile.split('.')[-1]=='html']

    if aggregatedFilesList == []: continue
    currentDir = currentDir.split('\\')[-1]
    
    extract_to_json(aggregatedFilesList, 'Hackerrank_scrapped_'+currentDir+'.jl')
    