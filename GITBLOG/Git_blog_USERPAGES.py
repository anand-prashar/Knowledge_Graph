'''
Created on Nov 20, 2017
@author: anand
'''


global jsonFileObj, errorFileObj, jsonFile, errorFile, entity_link_dict, techDict
entity_link_dict={}; techDict = set()
jsonFileObj = None; errorFileObj = None
jsonFile  = 'Git_IO_Blog.jl'                 #<-------------
errorFile = 'ERROR.csv'

##########################################################################################
import sys; reload(sys); sys.setdefaultencoding("utf-8")
import csv
import json
import nltk
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
    global entity_link_dict, techDict
    
    def xpath_extractor(xpathString, driver, attribute="innerText"):
        try:
            return driver.find_element( By.XPATH, xpathString ).get_attribute(attribute).strip()
        except InvalidSelectorException as _:
            return ''
        except NoSuchElementException as _:
            return ''
        except AttributeError as _:
            return ''
    
    def is_ascii(s):
        return all(ord(c) < 128 for c in s)
    
    jsonObj = {}
    driver.get(url)
    driver.implicitly_wait(3); #sleep(2)
    
    jsonObj['candidate_name'] = ''
    jsonObj['candidate_pic_url'] = ''
    jsonObj['candidate_occoupation']=''
    jsonObj['candidate_education']=''
    jsonObj['city_name']=''
    jsonObj['state']=''
    jsonObj['country']=''
    jsonObj['candidate_projects']=''
    ##################################################
    jsonObj['candidate_linkedentity'] = [ entity_link_dict[ url ] ]
            
    jsonObj['url'] = url
    p= jsonObj['url'].split('.github.io')
    jsonObj['url']='https://'+p[0].split('/')[-1]+'.github.io'
    jsonObj['doc_id'] = 'githubio'+p[0].split('/')[-1]
    text_extracted = xpath_extractor('//html', driver).lower()
    
    jsonObj['raw_content']= text_extracted #' '.join(textList_extracted)
            
    text_blob = [ word for word in nltk.word_tokenize( jsonObj['raw_content']) if word.strip()!='' and is_ascii(word)]
                                                       
    nltk_tagged = nltk.pos_tag( text_blob )
            
    jsonObj['candidate_skills']=set()
    for word in text_blob:
        if word in techDict:
            jsonObj['candidate_skills'].add(word)
    jsonObj['candidate_skills'] = list(jsonObj['candidate_skills'])

    jsonObj['candidate_glance'] = ''            
    #extract=''
    #jsonObj['candidate_glance'] = set()
    #for word, tag in nltk_tagged:
    #    if tag!='NN':
    #        if extract!='':
    #            jsonObj['candidate_glance'].add( extract[1:])
    #            extract = ''
    #            continue
    #        else: 
    #            extract+=' '+word
    #    jsonObj['candidate_glance'].add( extract)
    #jsonObj['candidate_glance'] = list(jsonObj['candidate_glance'])
    
    return jsonObj

def saveToJsonLinesFile(scrappedJson):
    global jsonFileObj, jsonFile
    if not jsonFileObj:
        jsonFileObj = open(jsonFile, 'wb')
    jsonFileObj.write( json.dumps(scrappedJson)+ linesep )
        
def saveErrorToLog(errorList):
    global errorFileObj
    if not errorFileObj:
        errorFileObj = csv.writer(open(errorFile, 'wb'), delimiter = ',', quoting = csv.QUOTE_ALL )
    errorFileObj.writerow( errorList )
        
##########################################################################################

driver = openBrowser()

# read leetCode_users.csv, and loop for scrapping

usersList = []

#prepare technology set for lookup
with open('technologyFile.csv','rb') as f:
    csvR = csv.reader(f, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
    for row in csvR:
        techDict.add( row[0].strip() )

with open('blogFile.csv','rb') as cf:
    csvR = csv.reader(cf, delimiter=',', quoting = csv.QUOTE_ALL)
    
    for row in csvR:
		if not row==[] and '.github.io'  in row[0]:
			usersList.append(row)
    
    done=0    
    for row in usersList:
        if row==[] or '.github.io' not in row[0]:
            ignore+=1; continue
        if 'http' != row[0][:4]: row[0]='http://'+row[0]
        entity_link_dict[ row[0]]= row[1]
            
        try:
            print '. Remaining WebPages: ', len(usersList)-done, '. url = ', row[0]
            scrappedJson = scrapPage( row[0].strip(), driver )
            saveToJsonLinesFile( scrappedJson )
        except Exception as e:
            saveErrorToLog(row + [str(e)] )
        done+=1

driver.quit()
print 'Result File:', jsonFile
print 'Error File:', errorFile
