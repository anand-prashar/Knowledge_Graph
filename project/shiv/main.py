import scrapy.cmdline

def main():
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'spider_leetcode'])

if  __name__ =='__main__':
    main()