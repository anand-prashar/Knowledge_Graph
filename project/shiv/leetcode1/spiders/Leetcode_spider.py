
import scrapy
import logging
from os import getcwd

class stackof_database(scrapy.Spider):
	name = "spider_leetcode"
    
	startPage = 1
	endPage = 30
	parse_method_url = 'https://leetcode.com'
	saved_Count = 0
	saveDir = getcwd()+'\\saved html\\' 
    
	def start_requests(self):
        
		baseUrl = "https://leetcode.com/contest/globalranking/1"
		#for index in range(self.startPage, self.endPage):
		yield scrapy.Request(url=baseUrl, callback=self.parse )
    
	def parse(self, response):
        #global fileSerial
        
		page = response.url.split("/")  
        
		for user_url in response.xpath("//a[@class='ranking-username']/@href").extract():
			yield response.follow( self.parse_method_url+user_url, callback= self.parse)
           
		with open('test.html','wb') as f:
			f.write( response.body)  
        #scrap data, save page

            
            #save file too
			with open(self.saveDir+page[3]+'.html','wb') as f:
				f.write( response.body)   
            
			self.saved_Count+=1
			self.log('***************************************************  SAVED == '+str(self.saved_Count))
            
             