from scrapy import cmdline
import time

while 1:
    cmdline.execute('scrapy crawl youyou'.split())
    time.sleep(60*60*3)