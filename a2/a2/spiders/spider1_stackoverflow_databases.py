'''
Created on Sep 9, 2017
@author: anand
'''

import scrapy
import logging

class stackof_database(scrapy.Spider):
    name = "spider_sof_dbschema"
    limit = 10
    saved_Count = 0
    
    def start_requests(self):
        
        urls = ["https://stackoverflow.com/questions/tagged/database-schema" ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse )
    
    def parse(self, response):
        #global fileSerial
        
        page = response.url.split("/")[4]   
        
        # add urls to queue
        if page == 'tagged':
            
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
                        
            questionID = response.xpath("//div[@id='question-header']/h1/a/@href").extract_first().split('/')[2]
            question = response.xpath("//div[@id='question-header']/h1/a/text()").extract_first()
            questionVotes = response.xpath("//div[@id='question']//td[@class='votecell']//span/text()").extract_first()
            questionTags =  response.xpath("//div[@id='question']//div[@class='post-taglist']//a/text()").extract()
            
            answerList_xpath = response.xpath("//div[@id='answers']//div[@class='answer' or @class='answer accepted-answer']")
            responders = []
            for answerObj in answerList_xpath:
                
                
                answerUpvotes = answerObj.xpath(".//td[@class='votecell']//span/text()").extract_first()
                answeredDate  = answerObj.xpath(".//td[@class='answercell']//div[@class='user-action-time']/span/text()").extract_first()
                personName = answerObj.xpath(".//td[@class='answercell']//div[@class='user-details']/a/text()").extract_first()
                personPic = answerObj.xpath(".//td[@class='answercell']//div[@class='user-gravatar32']//img/@src").extract_first()
                personURL = answerObj.xpath(".//td[@class='answercell']//div[@class='user-details']/a/@href").extract_first()
                personReputation = answerObj.xpath(".//td[@class='answercell']//div[@class='user-details']//span[@class='reputation-score']/text()").extract_first()
                badges = {'gold': 0, 'silver': 0, 'bronze':0}
                badgesObj= answerObj.xpath(".//td[@class='answercell']//div[@class='user-details']/div[@class='-flair']/span/@title").extract()
                for badgeText in badgesObj:
                    if 'reputation score' in badgeText : continue
                    bList = badgeText.split(" ")
                    if bList[1] in badges: badges[bList[1]] = int(bList[0])
                
                responders.append( (answerUpvotes, \
                                    {'Name': personName,
                                     'Pic':personPic,
                                     'UserLink':personURL,
                                     'Reputation': personReputation,
                                     'badges': badges,
                                     'tags': questionTags,
                                     'answeredOn': answeredDate}) )
            
            
            responders = sorted(responders, key = lambda x: int(x[0]), reverse = True)   
            scrappedDetail = {'Qid': questionID, 'QUpvotes':questionVotes, 'Question': question, 'QTags': questionTags, 'Responders': responders} 
            
            yield scrappedDetail         # save logic in main.py ( filename taken as parameter)    
        