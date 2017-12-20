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
    
def extract_to_csv(htmlDirectory, csvfilename,recordLimit):
    
    csvOPfile = open(csvfilename,'wb')
    csvObject = csv.writer( csvOPfile, delimiter = ',', quoting = csv.QUOTE_ALL)
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

def prepare_input(fileName, targetFileName):
    
    prepared_input = []
    with open(fileName,'rb') as f:
        readerObj = csv.reader(f)
        for questionList in readerObj:
            for question in questionList[1:]:  #0 - ignore filename column
                if question != '':
                    question= question.lower()
                    wordList = word_tokenize(question)
                    wordList = [word for word in wordList if word not in punctuation]
                    word_pos_tuple = pos_tag(wordList, tagset='universal')
                    if word_pos_tuple == []: continue
                    
                    labelled_row=[tuple_to_str( (word_pos_tuple[0][0], str(word_pos_tuple[0][1].lower()),'irrelevant'))] # 1st word not of interest - o label
                    for index in range(1,len(word_pos_tuple)):
                        if word_pos_tuple[index-1][1] in ['DET','ADP','VERB','NOUN'] and word_pos_tuple[index][1] =='NOUN':
                            labelled_row.append ( tuple_to_str( (word_pos_tuple[index][0], str(word_pos_tuple[index][1].lower()),'TECH_TAG') ))
                        else:
                            labelled_row.append ( tuple_to_str( (word_pos_tuple[index][0], str(word_pos_tuple[index][1].lower()),'irrelevant') ))    
                    
                    prepared_input.append(labelled_row)
    
    with open(targetFileName,'wb') as f:
        writerObj = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
        for val in prepared_input:
            writerObj.writerow(val)
#            pickle.dump(val, f)

    print 'Created labelled File : '+targetFileName   
    
#############################################################################################################

        
currentDir = getcwd()

trainFiles = [currentDir+'\\train\\'+f for f in listdir(currentDir+'\\train') if f.split('.')[-1]=='html']
testFiles =  [currentDir+'\\test\\' +f for f in listdir(currentDir+'\\test') if  f.split('.')[-1]=='html']

extract_to_csv(trainFiles, 'train.csv', recordLimit = 500)
extract_to_csv(testFiles, 'test.csv',   recordLimit = 200)

prepare_input('train.csv','labelled_train.csv')
prepare_input('test.csv','labelled_test.csv')

    