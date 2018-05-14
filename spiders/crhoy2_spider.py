#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
from scrapy import *
import scrapy
from scrapy_splash import SplashRequest
from random import randint
import codecs 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import random
import urllib
import justext
from scrapy.selector import HtmlXPathSelector


class MySpider(CrawlSpider):
    name = 'cr2'
    allow = [re.compile('https://www.crhoy.com/nacionales/.*')]
    start_urls = ['http://localhost:8050/info?wait=0.5&images=1&expand=1&timeout=90.0&url=https%3A%2F%2Fwww.crhoy.com%2Fsite%2Fdist%2Fseccion-nacionales.html%23%2Fsucesos&lua_source=function+main%28splash%2C+args%29%0D%0A++assert%28splash%3Ago%28args.url%29%29%0D%0A++assert%28splash%3Await%280.5%29%29%0D%0A++return+%7B%0D%0A++++html+%3D+splash%3Ahtml%28%29%2C%0D%0A++++png+%3D+splash%3Apng%28%29%2C%0D%0A++++har+%3D+splash%3Ahar%28%29%2C%0D%0A++%7D%0D%0Aend']

    def process_links(links):
    	for link in links:
        	link.url = "http://localhost:8050/render.html?" + urllib.urlencode({ 'url' : link.url })
    	return links

    rules = (
        Rule(LinkExtractor(allow=allow), callback='parse_item', process_links=process_links),
    )

    def process_links(self, links):
    	for link in links:
        	link.url = "http://localhost:8050/render.html?" + urlencode({ 'url' : link.url })
    	return links

    def parse_item(self, response):
        pagename = '/home/federico/Desktop/corpus_inil/crawler/crawler/crawlinil/datos_crhoy/' + str(randint(1,1000)) 
        with codecs.open(pagename, mode ='w', encoding = 'UTF-8') as f:
            f.write(response.body)
        
	        