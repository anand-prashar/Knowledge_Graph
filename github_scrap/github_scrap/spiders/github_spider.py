
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

class stackof_database(scrapy.Spider):
    name = "github_scrap"
    jlFileOut=open('Github_scrapped__POSSIBLE_valid.jl','wb')
    errorFile = open('ERROR.txt','wb')
    count=0
    entity_link_dict = {}
    
    start=150000
    stop =225000
    
    def start_requests(self):
        
        dataFileList = []
        with open('possibleGithubUsers.csv') as f:  #<-------------------------------------------
            csvR = csv.reader(f, delimiter = ',', quoting = csv.QUOTE_ALL)
            for row in csvR:
                dataFileList.append(row)
            
            for row in dataFileList[self.start:self.stop]:
                if row == []: continue
                
                self.entity_link_dict[ row[0] ] = row[1]
                yield scrapy.Request(url=row[0]+'?tab=repositories', callback=self.parse )

    def parse(self, response):
        
        def xpath_extract(response,xpath):
            try: return response.xpath(xpath).extract()[0].strip().lower()
            except Exception as _: 
                return ''
        
        try:   
            jsonObj = {}
            jsonObj['url'] = response.url[:-17]
            jsonObj['name']= xpath_extract(response,"//span[@class='p-name vcard-fullname d-block']/text()")
            jsonObj['address']= xpath_extract(response,"//li[@itemprop='homeLocation']/span/text()")
            jsonObj['LinkedEntity'] = [ self.entity_link_dict[jsonObj['url']]]
            jsonObj['projects'] = []
            jsonObj['technology'] = set()
            jsonObj['keywords'] = set()
            
            
            for repoRootNode in response.xpath("//div[@id='user-repositories-list']/ul/li"):
                jsonObj['projects'].append('https://github.com' + xpath_extract(repoRootNode,".//h3/a/@href"))
                jsonObj['technology'].add( xpath_extract(repoRootNode,".//span[@itemprop='programmingLanguage']/text()"))
                
                nltk_tagged = nltk.pos_tag( nltk.word_tokenize(xpath_extract(repoRootNode,".//p[@itemprop='description']/text()")))
                extract=''
                for word, tag in nltk_tagged:
                    if tag!='NN':
                        if extract!='':
                            jsonObj['keywords'].add( extract[1:])
                            extract = ''
                            continue
                    else: 
                        extract+=' '+word
                if extract!='': jsonObj['keywords'].add( extract)
            
            if '' in jsonObj['technology']: jsonObj['technology'].remove('')
            jsonObj['technology'] = list(jsonObj['technology'])
            jsonObj['keywords'] = map(string.strip, list(jsonObj['keywords']) )
            
            self.jlFileOut.write(json.dumps(jsonObj)+linesep)
        except:
            self.errorFile.write(jsonObj['url']+linesep)
            print 'ERROR:', self.jsonObj['url']
        self.count+=1
        print 'Done count: ', self.count#, ' . Left:',27464-self.count
        