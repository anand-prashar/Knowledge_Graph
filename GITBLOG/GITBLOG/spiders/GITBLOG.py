
'''
Created on Sep 19, 2017
@author: anand
'''


import scrapy
from os import linesep
import csv
import json
import nltk
import string

class GITBLOG(scrapy.Spider):
    name = "GITBLOG"
    jlFileOut=open('Git_IO_Blog.jl','wb')
    errorFile = open('ERROR.txt','wb')
    count=0
    entity_link_dict = {}
    techDict = set()
    
    def start_requests(self):
        
        dataFileList = []
        
        print 'HERE!!'
        
        #prepare technology set for lookup
        with open('technologyFile.csv','rb') as f:
            csvR = csv.reader(f, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
            for row in csvR:
                if 'http' != row[0][:4]:
                    row[0]='http://'+row[0]
                self.techDict.add( row[0])
        
        with open('blogFile.csv','rb') as f:  #<-------------------------------------------
            csvR = csv.reader(f, delimiter = ',', quoting = csv.QUOTE_ALL)
            for row in csvR:
                if row==[] or '.github.io' not in row[0] :continue
                dataFileList.append(row)
            
            print 'URLS', len(dataFileList)
            for row in dataFileList:
                self.entity_link_dict[ row[0] ] = row[1]
                yield scrapy.Request(url=row[0].strip(), callback=self.parse )

    def parse(self, response):
        
        def xpath_extract(response,xpath):
            try: 
                retList = []
                extracts= response.xpath(xpath).extract()
                for phrase in extracts:
                    phrase= phrase.strip()
                    if phrase !='': retList.append(phrase.lower())
                return retList
            
            except Exception as _: 
                return ['']
        jsonObj = {}
        try:   
            
            jsonObj['candidate_name'] = ''
            jsonObj['candidate_pic_url'] = ''
            jsonObj['candidate_occoupation']=''
            jsonObj['candidate_education']=''
            jsonObj['city_name']=''
            jsonObj['state']=''
            jsonObj['country']=''
            jsonObj['candidate_projects']=''
            
            jsonObj['candidate_linkedentity'] = [ self.entity_link_dict[ response.url ] ]
            
            jsonObj['url'] = response.url
            p= jsonObj['url'].split('.github.io')
            jsonObj['url']='https://'+p[0].split('/')[-1]+'.github.io'
            
            textList_extracted = xpath_extract(response, '//text()')
            jsonObj['raw_content']= ' '.join(textList_extracted)
            
            text_blob = nltk.word_tokenize( jsonObj['raw_content'])
            nltk_tagged = nltk.pos_tag( text_blob )
            
            jsonObj['candidate_skills']=set()
            for word in text_blob:
                if word in self.techDict:
                    jsonObj['candidate_skills'].add(word)
            jsonObj['candidate_skills'] = list(jsonObj['candidate_skills'])
            
            extract=''
            jsonObj['candidate_glance'] = set()
            for word, tag in nltk_tagged:
                if tag!='NN':
                    if extract!='':
                        jsonObj['candidate_glance'].add( extract[1:])
                        extract = ''
                        continue
                else: 
                    extract+=' '+word
            jsonObj['candidate_glance'].add( extract)
            jsonObj['candidate_glance'] = list(jsonObj['candidate_glance'])
            
                
            self.jlFileOut.write(json.dumps(jsonObj)+linesep)
        except Exception as e:
            print 'ERROR'
            self.errorFile.write(str(e)+linesep)
        self.count+=1
        print 'Done2 count: ', self.count#, ' . Left:',27464-self.count
        