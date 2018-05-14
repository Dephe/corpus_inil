#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from crawlinil.items import CrawlinilItem
import re
import codecs
import justext
from bs4 import BeautifulSoup




class ExtraSpider(CrawlSpider):
    name = "extra"
    start_urls = [  'http://www.diarioextra.com/Seccion/deportes',
                    'http://www.diarioextra.com/Seccion/sucesos',
                    'http://www.diarioextra.com/Seccion/nacionales',
                    'http://www.diarioextra.com/Seccion/opinion']
    allow = re.compile('http://www.diarioextra.com/Noticia/.*')

    rules = (Rule(LinkExtractor(allow = allow), callback='parse_items', follow=True), )

    def parse_items(self, response):
        secciones = response.selector.xpath('/html/body/header/div[2]/div/span').extract()
        fecha_candidato1 = response.selector.xpath('/html/body/div[2]/main/div[1]/article/div/section/p[3]/span').extract()
        fecha_candidato2 = response.selector.xpath('/html/body/div[2]/main/div[1]/article/div/section/p[4]/span').extract()
        titulo = response.selector.xpath('/html/body/div[2]/main/div[1]/figcaption/h1').extract()
        subtitulo = response.selector.xpath('/html/body/div[2]/main/div[1]/figcaption/h3').extract()
        secciones = BeautifulSoup(secciones[0], 'lxml').text
        fecha_candidato1 = BeautifulSoup(fecha_candidato2[0], 'lxml').text
        fecha_candidato2 = BeautifulSoup(fecha_candidato2[0], 'lxml').text
        try:
            subtitulo = BeautifulSoup(subtitulo[0], 'lxml').text
        except IndexError:
            subtitulo = None
        try:
            titulo = BeautifulSoup(titulo[0], 'lxml').text
        except IndexError:
            titulo = response.selector.xpath('/html/body/div[2]/main/div[1]/article/h1').extract()
            titulo = titulo = BeautifulSoup(titulo[0], 'lxml').text

        if fecha_candidato1 == 'EMAIL':
            fecha = fecha_candidato2
        else:
            fecha = fecha_candidato1
        pagename = '/home/federico/Desktop/corpus_inil/crawler/crawler/crawlinil/datos_extra/' + 'Extra_' + secciones + '_' + titulo #+ re.findall(u'\S*\s\S*', titulo, re.UNICODE)[0] + '_' #+ re.findall(u'\d+\s\w+',fecha, re.UNICODE)[0] + '.txt'
        pagename = re.sub(' ', '_', pagename)
        if secciones in ['Nacionales', 'Sucesos', 'Deportes', 'Opinión']: 
            with codecs.open(pagename, mode ='w', encoding = 'UTF-8') as f:
                f.write(u'Sección: ' + secciones)
                f.write('\n')
                f.write('Fecha: ' + fecha)
                f.write('\n')
                f.write('Título: ' + titulo)
                f.write('\n')
                print str(subtitulo)
                
                if subtitulo is None:
                    autor = response.selector.xpath('/html/body/div[2]/main/div[1]/article/h6').extract()
                    autor = BeautifulSoup(autor[0], 'lxml').text
                    f.write('Autor: ' + autor)
                elif len(subtitulo) > 1:
                     f.write('Subtítulo: ' + subtitulo)
                f.write('\n')
                f.write('\n')
                texto = response.body
                paragraphs = justext.justext(texto, justext.get_stoplist("Spanish"))
                for paragraph in paragraphs:
                    if paragraph.cf_class == 'good' or paragraph.cf_class == 'neargood':
                        f.write(paragraph.text)
                        f.write('\n')
               
       
        


