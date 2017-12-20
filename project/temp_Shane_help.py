'''
Created on Sep 28, 2017

@author: anand
'''
'''
Created on Sep 25, 2017

@author: anand
'''

import csv
from os import listdir, getcwd
from lxml import html
from nltk import word_tokenize, pos_tag
from string import punctuation
punctuation = set(punctuation)

import sys; reload(sys)
sys.setdefaultencoding('utf8')

def tuple_to_str(tpl):
    str = ''
    for val in tpl:
        str+=val+','
    if str !='': return str[:-1]
    return str
    
def extract_to_json(htmlDirectory, outputFileName):
    
    #csvOPfile = open(csvfilename,'wb')
    #csvObject = csv.writer( csvOPfile, delimiter = ',', quoting = csv.QUOTE_ALL)
    opList = []
    for htmlFile in htmlDirectory:
        try: 
            domTree = html.parse( open(htmlFile) )
        except Exception as e: print 'FAIL: '+htmlFile    
        
        extractedQuestions = domTree.xpath("//div[@class='row post-container']/a/text()")
        for i in range(len(extractedQuestions)):
            extractedQuestions[i] = extractedQuestions[i].encode("ascii", "ignore")
            
        hFname = htmlFile.split('\\')[-1]
        opList.append( [int(hFname.split(' ')[0]), hFname ] + extractedQuestions )
        
    opList = sorted( opList, key = lambda x: x[0])
    for listLine in opList:
        prevLimit = recordLimit
        recordLimit = recordLimit - len(listLine[2:])
        if recordLimit >= 0:
            csvObject.writerow(listLine[1:])
        else:
            csvObject.writerow(listLine[1:prevLimit+2])    
            break
        
    csvOPfile.close()
    print 'Saved File: '+csvfilename


    print 'Created labelled File : '+targetFileName   
    
#############################################################################################################

        
currentDir = getcwd()

trainFiles = [currentDir+'\\train\\'+f for f in listdir(currentDir+'\\train') if f.split('.')[-1]=='html']
testFiles =  [currentDir+'\\test\\' +f for f in listdir(currentDir+'\\test') if  f.split('.')[-1]=='html']

extract_to_csv(trainFiles, 'train.csv', recordLimit = 500)
extract_to_csv(testFiles, 'test.csv',   recordLimit = 200)

prepare_input('train.csv','labelled_train.csv')
prepare_input('test.csv','labelled_test.csv')

    