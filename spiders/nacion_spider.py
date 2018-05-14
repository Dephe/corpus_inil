#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlinil.items import CrawlinilItem
import re
import codecs
import justext
from random import randint


class NacionSpider(CrawlSpider):
    name = "nacion"
    start_urls = [  'https://www.nacion.com/sucesos/',
                    'https://www.nacion.com/puro-deporte/',
                    'https://www.nacion.com/el-pais/',
                    'https://www.nacion.com/opinion/']
    allow = re.compile('https://www.nacion.com/')

    rules = (Rule(LinkExtractor(allow = allow), callback='parse_items', follow=True), )
    
    def parse_items(self, response):
        reg_subtitulo = re.compile('="subheadline">(.*?)</p>')
        reg_fecha = re.compile('datePublished":"(\d*\W\d*\W\d*)')
        reg_seccion = re.compile('href="https://www.nacion.com/([\w -]*)/')
        reg_titlo = re.compile('"og:title"\scontent=(.*?)/>')
        prueba = False
        try:
            seccion = re.findall(reg_seccion, response.body)[0]
            prueba = True
            if seccion == 'el-pais':
                seccion = 'nacionales'
            elif seccion == 'puro-deporte':
                seccion = 'deportes'
        except IndexError:
            pass
        try:
            fecha = re.findall(reg_fecha, response.body)[0]
        except IndexError:
            pass
        try:
            titulo = re.findall(reg_titlo, response.body)[0]
        except IndexError:
            pass
        try: 
            subtitulo = re.findall(reg_subtitulo, response.body)[0]
        except:
            pass
        if prueba == True:
            if seccion in ('sucesos', 'nacionales', 'opinion', 'deportes'):
                pagename = '/home/federico/Desktop/corpus_inil/crawler/crawler/crawlinil/datos_nacion/' + 'Nacion_' + seccion + '_' + re.findall(u'\S*\s\S*', titulo, re.UNICODE)[0] + '_' + fecha 
                with codecs.open(pagename, mode ='w', encoding = 'UTF-8') as f:
                    texto = response.body
                    try:
                        f.write('Sección: ' + seccion.title())
                    except IndexError:
                        pass
                    f.write('\n')

                    try:
                        fecha = re.findall(reg_fecha, texto)[0]
                        f.write('Fecha: ' + fecha)
                    except IndexError:
                        pass
                    f.write('\n')
                    
                    try:
                        f.write('Título: ' + str(titulo))
                    except IndexError:
                        pass
                    f.write('\n')
                    try:
                        f.write('Subtítulo: ' + subtitulo)
                    except IndexError:
                        pass

                    f.write('\n')
                    f.write('\n')

                    paragraphs = justext.justext(texto, justext.get_stoplist("Spanish"))
                    for paragraph in paragraphs:
                        if paragraph.cf_class == 'good' or paragraph.cf_class == 'neargood':
                            f.write(paragraph.text)
                            f.write('\n')
                       
           
            


