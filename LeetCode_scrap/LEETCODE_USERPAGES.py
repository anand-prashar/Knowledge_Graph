'''
Created on Nov 20, 2017
@author: anand
'''


global jsonFileObj, errorFileObj, jsonFile, errorFile
jsonFileObj = None; errorFileObj = None
jsonFile  = 'LeetCode_scrapped_result.jl'                 #<-------------
errorFile = 'LeetCode_scrapped_error.csv'

##########################################################################################
import sys; reload(sys); sys.setdefaultencoding("utf-8")
import csv
import json
from os import linesep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, ErrorInResponseException

##########################################################################################

def openBrowser():
    #try:
    #    driver = webdriver.Edge("C:/Program Files/selenium_webdriver/MicrosoftWebDriver.exe")
    #except Exception as _:
    #    print 'Alert: Switching to Chrome'
    driver = webdriver.Chrome("C:/Program Files/selenium_webdriver/chromedriver.exe")
    return driver

def scrapPage(url, driver ):
    
    def xpath_extractor(xpathString, driver, attribute="innerText"):
        try:
            return driver.find_element( By.XPATH, xpathString ).get_attribute(attribute).strip()
        except InvalidSelectorException as _:
            return ''
        except NoSuchElementException as _:
            return ''
        except AttributeError as _:
            return ''
    
    scrappedJson = {}
    driver.get(url)
    driver.implicitly_wait(2); #sleep(2)
    
    #throw 404 error pages
    if xpath_extractor("//h2/strong", driver) == 'Page Not Found':
        raise Exception
    
    scrappedJson['name'] = xpath_extractor("//h4[@class='realname']", driver)
    scrappedJson['url'] =  url
    scrappedJson['id'] =  url.split('/')[-2]
    scrappedJson['image'] = xpath_extractor("//img[@alt='user avatar']", driver, attribute= "src")
    scrappedJson['gitHub'] = xpath_extractor("//a[@id='github-connect']", driver, attribute= "href")
    scrappedJson['linkedIn'] = xpath_extractor("//a[@id='linkedin-connect']", driver, attribute= "href")
    scrappedJson['Country'] =    xpath_extractor("//ul[@class='list-group']/li[i[@class='fa fa-globe fa-fw']]/span", driver)
    scrappedJson['Occupation'] = xpath_extractor("//ul[@class='list-group']/li[i[@class='fa fa-users fa-fw']]/span", driver)
    scrappedJson['Education' ] = xpath_extractor("//ul[@class='list-group']/li[i[@class='fa fa-graduation-cap fa-fw']]/span", driver)
    scrappedJson['Program_quality' ] = xpath_extractor("//ul[@class='list-group ng-scope']/li[span[@class='badge progress-bar-info']]/span", driver)
    scrappedJson['Program_Language'] = xpath_extractor("//ul[@class='list-group']/a/span[@class='badge progress-bar-info']", driver)
    
    return scrappedJson

def saveToJsonLinesFile(scrappedJson):
    global jsonFileObj, jsonFile
    if not jsonFileObj:
        jsonFileObj = open(jsonFile, 'wb')
    jsonFileObj.write( json.dumps(scrappedJson)+ linesep )
        
def saveErrorToLog(errorList):
    global errorFileObj
    if not errorFileObj:
        errorFileObj = csv.writer(open(errorFile, 'wb'), delimiter = ',', quoting = csv.QUOTE_ALL )
        errorFileObj.writerow(['BASE_PAGE','RANK','USERID', 'ERROR'])
    errorFileObj.writerow( errorList )
        
##########################################################################################

driver = openBrowser()

# read leetCode_users.csv, and loop for scrapping

usersList = []
with open('leetCode_users.csv','rb') as cf:
    csvR = csv.reader(cf, delimiter=',', quoting = csv.QUOTE_ALL)
    next(csvR)
    for row in csvR:
        usersList.append(row)
    
    done=0    
    for row in usersList:
        if row==[]: continue
        try:
            print 'Processing rank: ', row[1], '. Remaining WebPages: ', len(usersList)-done
            url = 'https://leetcode.com/'+row[2]+'/'
            scrappedJson = scrapPage(url, driver )
            saveToJsonLinesFile( scrappedJson )
        except Exception as e:
            saveErrorToLog(row + [str(e)] )
        done+=1

driver.quit()
print 'Result File:', jsonFile
print 'Error File:', errorFile
