'''
Created on Sep 9, 2017

@author: anand
'''

import scrapy.cmdline

def main():
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'spider_sof_users'])

if  __name__ =='__main__':
    main()