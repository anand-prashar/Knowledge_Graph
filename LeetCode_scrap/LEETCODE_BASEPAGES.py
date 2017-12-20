'''
Created on Nov 19, 2017
@author: anand
'''
lowBase = 1
highBase = 5
errorLog = 'basePageErrorLog.csv'
userIdsFile = 'leetCode_users.csv'

##########################################################################################
import sys; reload(sys); sys.setdefaultencoding("utf-8")
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidSelectorException

f_e = open(errorLog,'wb')
csvObj_e= csv.writer( f_e, delimiter = ',', quoting = csv.QUOTE_ALL)
csvObj_e.writerow(['BASE','USERURL','ERROR'])

f_u = open(userIdsFile,'wb')
csvObj_u= csv.writer( f_u, delimiter = ',', quoting = csv.QUOTE_ALL)
csvObj_u.writerow(['BASE_PAGE','RANK','USERID'])

##########################################################################################

#try:
#    driver = webdriver.Edge("C:/Program Files/selenium_webdriver/MicrosoftWebDriver.exe")
#except Exception as _:
#    print 'Alert: Switching to Chrome'
driver = webdriver.Chrome("C:/Program Files/selenium_webdriver/chromedriver.exe")

#LOGIN PAGE
driver.get('https://leetcode.com/accounts/login/')
userIdField = driver.find_element_by_id('id_login')
passwdField = driver.find_element_by_id('id_password')
userIdField.send_keys('appa1221')
passwdField.send_keys('test1234')


# Select the Python language option
python_link = driver.find_elements_by_xpath("//button[@type='submit']")[0]
python_link.click()
driver.implicitly_wait(10)

# Go to codepad.org
for basePageNumber in range(lowBase, highBase+1):
    url = 'https://leetcode.com/contest/globalranking/'+str(basePageNumber)+'/'
    try:
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL+'t')
        driver.get(url)
        driver.implicitly_wait(4)
        sleep(4)
        
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL+'W')
        
        #scrap all userIds
        leftXpath       = "//div[@class='ranking-row']["
        rightXpathUname = "]//div[@class='username']"
        rightXpathRank  = "]//div[@class='ranking col']"
        for itr in range(1,26):
            try:
                uname = driver.find_element(By.XPATH, leftXpath+str(itr)+rightXpathUname  ).get_attribute("innerText")
                rank  = driver.find_element(By.XPATH, leftXpath+str(itr)+rightXpathRank ).get_attribute("innerText")
                print 'page - ',basePageNumber, ' , - rank ', rank
                csvObj_u.writerow([str(basePageNumber), rank, uname])
            except InvalidSelectorException as e:
                pass
        

    except Exception as e:
        print 'Error: ', basePageNumber
        csvObj_e.writerow([str(basePageNumber), url, str(e)])
        
driver.quit()

##########################################################################################
print 'SEE FILE: ', userIdsFile
f_e.close()        
f_u.close()