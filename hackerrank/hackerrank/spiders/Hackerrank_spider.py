
'''
Created on Sep 19, 2017

@author: anand
'''


import scrapy
import logging

class stackof_database(scrapy.Spider):
    name = "spider_hr"
    saved_Count = 0
    saveDir = 'C:\\Users\\anand\\Hackerrank Saved Html\\5000-10000\\' 
    startBase = 5000
    endBase = 10000
    parse_method_url = 'https://www.hackerrank.com'
    curr_base = '1'
    
    def start_requests(self):
        
        urlLeft = "https://www.hackerrank.com/leaderboard?level=1&page="
        urlRight= "&practice=algorithms"
        for index in range(self.startBase, self.endBase):
            yield scrapy.Request(url=urlLeft+str(index)+urlRight, callback=self.parse )

    def parse(self, response):
        #global fileSerial
        
        page = response.url.split("/")[-1].split('?')
        
        # add urls to queue from base pages
        if page[0] == 'leaderboard':
            
            #copy all 10 urls(default) of targeted page-types
            for user_url in response.xpath("//a[@class='backbone cursor leaderboard-hackername table-root']/@href").extract():
                if user_url is not None:
                    yield response.follow( self.parse_method_url+user_url, callback= self.parse)
            
            self.curr_base = page[1].split('&')[1]

        #scrap data, save page
        else:
            
            #save file too
            with open(self.saveDir+page[0]+'.html','wb') as f:
                f.write( response.body)   
            
            self.saved_Count+=1
            self.log('***************************************************  SAVED == '+str(self.saved_Count)+' / '+self.curr_base)
                