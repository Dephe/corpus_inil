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
from random import randint
import codecs
import justext
from bs4 import BeautifulSoup





class CrhoySpider(CrawlSpider):
    name = "crhoy"
    start_urls = ['https://www.crhoy.com/opinion/opinion-los-especialistas/desempleo-juvenil-pasantias-y-la-caja/']
    allow = re.compile('https://www.crhoy.com/(?!noticias-sobre)')


    rules = (Rule(LinkExtractor(allow = allow), callback='parse_items', follow=True), )
    
    def parse_items(self, response):
        reg_titulo = re.compile('</span>(.*)</|titulo">(.*)</h1>')
        titulo = response.selector.xpath('/html/body/div[1]/div[2]/section/div[4]/article/div[1]/h1').extract()
        titulo_opinion = response.selector.xpath('/html/body/div/section/div[4]/article/div[1]/h1').extract()
        fecha = response.selector.xpath('/html/body/div[1]/div[2]/section/div[4]/article/div[1]/div').extract()
        fecha_opinion = response.selector.xpath('/html/body/div/section/div[4]/article/div[1]/p').extract()
        seccion = response.selector.xpath('/html/body/div[1]/div[2]/section/div[4]/article/div[1]/h3[1]/a[1]').extract()
        sub_seccion = response.selector.xpath('/html/body/div[1]/div[2]/section/div[4]/article/div[1]/h3[1]/a[2]').extract()
        contenido = response.selector.xpath('/html/body/div[1]/div[2]/section/div[4]/article/div[3]').extract()
        contenido_opinion = response.selector.xpath('/html/body/div/section/div[4]/article/div[3]').extract()
        try:
            if len(titulo[0]) > 0:
                seccion = BeautifulSoup(seccion[0], 'lxml').text
                seccion = seccion.replace('\r', '').replace('\n', '').replace(' ', '')
                sub_seccion = BeautifulSoup(sub_seccion[0], 'lxml').text
                sub_seccion = sub_seccion.replace('\r', '').replace('\n', '').replace(' ', '')
                fecha = re.findall('\w*\s\w*,\s\w*\s*\w*', BeautifulSoup(fecha[0], 'lxml').text)[0]
                if seccion in ['Nacionales', 'Deportes', 'Opinión']:
                    if sub_seccion == 'Sucesos':
                        pagename = '/home/federico/Desktop/corpus_inil/crawler/crawler/crawlinil/datos_crhoy/Crhoy_Sucesos' + re.findall(u'\S*\s\S*', BeautifulSoup(titulo[0], 'lxml').text, re.UNICODE)[0] + '_' + fecha.replace(' ', '_').replace(',', '') 
                        seccion = 'Sucesos'
                    else:
                        pagename = '/home/federico/Desktop/corpus_inil/crawler/crawler/crawlinil/datos_crhoy/Crhoy' + '_' + seccion + '_' + re.findall(u'\S*\s\S*', BeautifulSoup(titulo[0], 'lxml').text, re.UNICODE)[0] + '_' + fecha.replace(' ', '_').replace(',', '')

                    with codecs.open(pagename, mode ='w', encoding = 'UTF-8') as f:
                        f.write('Sección: ' + seccion )
                        f.write('\n')
                        f.write('Fecha: ' + fecha)
                        f.write('\n')
                        titulo = BeautifulSoup(titulo[0], 'lxml').text
                        titulo = titulo.replace('\r', '').replace('\n', '')
                        f.write('Título: ' + titulo)
                        f.write('\n')
                        f.write('\n')
                        #for element in subtitulo:
                            #f.write(element)
                            #f.write('\n')
                        #f.write(BeautifulSoup(contenido[0], 'lxml').text)
                        #texto_regex = re.compile('Los comentarios expresados en las columnas de opinión.*', re.DOTALL)
                        #texto = re.sub(texto_regex, '', texto)
                        paragraphs = justext.justext(contenido[0], justext.get_stoplist("Spanish"))
                        for paragraph in paragraphs:
                            if paragraph.cf_class == 'good' or paragraph.cf_class == 'neargood':
                                f.write(paragraph.text)
                                f.write('\n')                       
        except IndexError:
            try: 
                if len(titulo_opinion[0]) > 0:
                    fecha = re.findall('\w*\s\w*,\s\w*\s*\w*', BeautifulSoup(fecha_opinion[0], 'lxml').text)[0]
                    pagename = '/home/federico/Desktop/corpus_inil/crawler/crawler/crawlinil/datos_crhoy/Crhoy_Opinion'  + '_' + re.findall(u'\S*\s\S*', BeautifulSoup(titulo_opinion[0], 'lxml').text, re.UNICODE)[0] + '_' + fecha.replace(' ', '_').replace(',', '')
                    with codecs.open(pagename, mode ='w', encoding = 'UTF-8') as f:
                        f.write('Seccion: Opinion')
                        f.write('\n')
                        f.write('Fecha: ')
                        f.write(fecha)
                        f.write('\n')
                        titulo = BeautifulSoup(titulo_opinion[0], 'lxml').text
                        titulo = titulo.replace('\r', '').replace('\n', '')
                        f.write('Título: ' + titulo)
                        f.write('\n')
                        f.write('\n')
                        paragraphs = justext.justext(contenido_opinion[0], justext.get_stoplist("Spanish"))
                        for paragraph in paragraphs:
                            if paragraph.cf_class == 'good' or paragraph.cf_class == 'neargood':
                                f.write(paragraph.text)
                                f.write('\n')
            except IndexError:
                pass
                   
           
            


