'''
Created on Nov 19, 2017

@author: anand
'''

from selenium import webdriver

driver = webdriver.Chrome("C:/Program Files/chromedriver_win32/chromedriver.exe")

# Go to codepad.org
driver.get('http://codepad.org')

# Select the Python language option
python_link = driver.find_elements_by_xpath("//input[@name='lang' and @value='Python']")[0]
python_link.click()

# Enter some text!
text_area = driver.find_element_by_id('textarea')
text_area.send_keys("print 'Hello,' + ' World!'")

# Submit the form!
submit_button = driver.find_element_by_name('submit')
submit_button.click()

# Make this an actual test. Isn't Python beautiful?
assert "Hello, World!" in driver.page_source

# Close the browser!
driver.quit()