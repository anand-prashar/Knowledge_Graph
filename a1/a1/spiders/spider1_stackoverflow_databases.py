'''
Created on Sep 9, 2017
@author: anand
'''

import scrapy,sys
reload(sys)
sys.setdefaultencoding("utf-8")


class stackof_database(scrapy.Spider):
    name = "spider_sof_dbschema"
    limit = 1000
    saved_Count = 0
    #DOWNLOAD_DELAY = 0.5    # done in settings.py
    
    def start_requests(self):
        urls = ["https://stackoverflow.com/questions/tagged/database-schema?sort=newest&pagesize=50" ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse )
           
    def parse(self, response): 
        doc_id = response.url.split("/")[4]   
        
        # add urls to queue from base pages
        if doc_id == 'tagged':
            
            #copy all 50 urls(default) of targeted page-types
            for questionURL in response.xpath("//div[@id='questions']/div//div[@class='summary']/h3/a/@href").extract(): #response.css("div.question-summary"):
                if questionURL is not None:
                    if self.limit >0:
                        self.limit-=1
                        yield response.follow( questionURL, callback= self.parse)
            
            # refer to seed, another base url
            nextBasePageURL = response.xpath("//div[@class='pager fl']//a[@rel='next']/@href" ).extract_first()
            if nextBasePageURL is not None:
                    yield response.follow( nextBasePageURL, callback= self.parse)  

        #scrap data, save page
        else:
            self.saved_Count+=1
            self.log('***************************************************  COUNTER == '+str(self.saved_Count))
            
            save_line = { 'doc_id': hash(response.url),
                          'timestamp_crawl': response.headers['Date'],
                          'url': response.url,
                          'raw_content': response.body.replace('\r\n', ' ')
                        }
            
            # yield for save to file using command parameters
            yield save_line
            
            #save file too
            saveFile = '%s.html' % hash(response.url)
            with open(saveFile,'wb') as f:
                f.write( response.body)
            self.log("SAVED FILE >>>>>>>>  "+str(saveFile))            