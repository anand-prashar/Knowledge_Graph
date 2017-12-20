
'''
Created on Sep 19, 2017

@author: anand
'''


import scrapy
import logging

class stackof_database(scrapy.Spider):
    name = "spider_sof_users"
    saveDir = 'C:\\Users\\anand\\Stackoverflow\\4.5 - 5M\\' 
    startPage = 450000
    endPage = 500000
    
    
    def start_requests(self):
        
        baseUrl = "https://stackoverflow.com/users/"
        for index in range(self.startPage, self.endPage):
            yield scrapy.Request(url=baseUrl+str(index), callback=self.parse )
    
    def parse(self, response):
        #global fileSerial
        
        page = response.url.split("/")  
        
        # add urls to queue
        if len(page) >= 6:            
            htmlName = page[4]+' '+page[5]+'.html'
            
        else:
            # code never comes here !
            htmlName = 'NF '+page[4]+'.html'
            
        with open(self.saveDir+htmlName,'wb') as f:
            f.write( response.body)
            self.log("SAVED FILE *******************************  "+page[4])      