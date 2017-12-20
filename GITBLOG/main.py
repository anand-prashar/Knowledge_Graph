'''
Created on Sep 9, 2017

@author: anand
'''

import scrapy.cmdline


if  __name__ =='__main__':
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'GITBLOG'])