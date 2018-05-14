#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
import scrapy
from scrapy_splash import SplashRequest
import codecs
import random
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashJsonResponse, SplashTextResponse, SplashResponse


class MySpider(CrawlSpider):
    name = 'cr3'
    start_urls = ["https://www.crhoy.com/nacionales/hombre-muere-tras-atropello-de-trailer-en-pococi/"]
    allow = [re.compile('https://www.crhoy.com/.*')]
    rules = (Rule(LinkExtractor(allow = allow), callback='parse_items', follow=True), )


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='render.html',
                args={'wait': 20},
            )

    def parse_items(self, response):
        pagename = '/home/federico/Desktop/corpus_inil/crawler/crawler/crawlinil/datos_crhoy/' + str(randint(1,1000)) 
        with codecs.open(pagename, mode ='w', encoding = 'UTF-8') as f:
            f.write(response.body)