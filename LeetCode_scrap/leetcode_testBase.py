'''
Created on Nov 18, 2017

@author: anand
'''

import sys; reload(sys)
sys.setdefaultencoding("utf-8")
from time import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# Google Chrome 
driver = webdriver.Chrome("C:/Program Files/chromedriver_win32/chromedriver.exe")


# ------------------------------
# The actual test scenario: Test the codepad.org code execution service.

# Go to codepad.org
t=time()
driver.get('https://leetcode.com/koolzz/')#'http://codepad.org')
#driver.implicitly_wait(7)




v= driver.find_element(By.XPATH, "//div[@class='ranking-row']//div[@class='username']")# "//h4[@class='realname']")# "//a[@id='github-connect']")
print v.get_attribute("innerText")#"href")

#find_element_by_xpath("//h4[@class='realname']/text()")#//a[@id='github-connect']/@href")
# Close the browser!
driver.quit()

print time()-t