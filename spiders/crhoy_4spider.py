# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import codecs 
import re
from BeautifulSoup import BeautifulSoup
import unicodedata
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from crawlinil.items import CrawlinilItem
import justext
from bs4 import BeautifulSoup
import random


import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, webpage, tag):
    driver.get(webpage)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)        
    html_source = driver.page_source
    html_source = unicodedata.normalize('NFKD', html_source).encode('ascii','ignore')
    driver.quit()
    if tag != 'opinion':
        links_to_return = list(set(re.findall('https://www.crhoy.com/' + tag + '/.*?/', html_source)))
    elif tag == 'opinion':
        links_to_return = list(set(re.findall('https://www.crhoy.com/opinion/.*?/.*?/', html_source)))
    return links_to_return, tag
    


class ExtraSpider(CrawlSpider):
    name = "cr4"
    urls_nacionales = lookup(init_driver(), 'https://www.crhoy.com/site/dist/seccion-nacionales.html#', 'nacionales')
    urls_sucesos = lookup(init_driver(), 'https://www.crhoy.com/site/dist/seccion-nacionales.html#/sucesos', 'Sucesos')
    urls_deporte = lookup(init_driver(), 'https://www.crhoy.com/site/dist/seccion-deportes.html', 'deportes')
    #urls_opinion = lookup(init_driver(), 'https://www.crhoy.com/site/dist/seccion-opinion.html', 'opinion')
    start_urls =  list(set(urls_deporte[0] + urls_sucesos[0] + urls_nacionales[0]))
    

    def parse(self, response):
        titulo = response.selector.xpath('/html/body/div[1]/div[2]/section/div[4]/article/div[1]/h1').extract()
        fecha = response.selector.xpath('/html/body/div[1]/div[2]/section/div[4]/article/div[1]/div').extract()
        seccion = response.selector.xpath('/html/body/div[1]/div[2]/section/div[4]/article/div[1]/h3[1]/a[2]').extract()
        pagename = '/home/federico/Desktop/corpus_inil/crawler/crawler/crawlinil/datos_crhoy/' + str(random.randint(1,1000))
        titulo = BeautifulSoup(titulo[0], 'lxml').text
        titulo = titulo.rstrip('\n')
        fecha = BeautifulSoup(fecha[0], 'lxml').text
        fecha = re.findall('\w*\s\w*,\s\w*', fecha)[0]
        seccion = BeautifulSoup(seccion[0], 'lxml').text
        #macrosecciones
        if seccion in ['Fútbol', 'Atletismo', 'Baloncesto', 'Tennis', 'Motores', 'Natación', 'Ciclismo', 'Surf', 'Voleibol', 'Otros', 'Destino Rusia']:
            seccion = 'Deportes'
        if seccion in ['Clima', 'Educación', 'Gobierno', 'Política', 'Salud', 'Transportes', 'Servicios']:
            seccion = 'Nacionales'
        if seccion in = ['Sucesos']:
            seccion = 'Sucesos'
        if seccion in = ['Columnas'. 'Especialistas', 'Lector opina', 'Aclaraciones']:
            seccion = 'Opinión'
        with codecs.open(pagename, mode='w', encoding='utf-8') as f:
            f.write('Seccion: ' + seccion + '\n' )
            f.write('Titulo: ' + titulo + '\n')
            f.write('Fecha: ' + fecha + '\n')
            paragraphs = justext.justext(response.body, justext.get_stoplist("Spanish"))
            for paragraph in paragraphs:
                if paragraph.cf_class == 'good' or paragraph.cf_class == 'neargood':
                    if paragraph.text.startswith('Los comentarios expresados en'):
                        break
                    else:
                        f.write(paragraph.text)
                        f.write('\n')



            