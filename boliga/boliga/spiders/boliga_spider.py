
import scrapy
import selenium
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import os
from selenium.common.exceptions import StaleElementReferenceException

##########################

### THIS FILE WAS REPLACED, SEE INSTEAD scrape.py

##########################



class BoligaSpider(scrapy.Spider):
    name = "boliga"
    start_urls = []

    for i in range(1,26280):
        start_urls.append(f"https://www.boliga.dk/salg/resultater?searchTab=1&page={i}&sort=date-d&salesDateMin=2004&saleType=1&fbclid=IwAR0lHCc_ewr2lQj4WdWZIB7p92G1FE0ql1pevEj0j5YVeOUXxRkU7_V86po")

    def parse(self, response):

        filename = 'historiske_salg.txt'
        with open(filename, 'a') as f:

            for i in range(1, 50):
                #houseprice
                price = response.css(
                    f"table > tbody > tr:nth-child({i}) > td:nth-child(2) > span::text").get()
                if price is not None:
                    price = price[:-4]

                #sold date
                sold_date=response.css(f"table > tbody > tr:nth-child({i}) > td:nth-child(3) > div > span:nth-child(1)::text").get()
                sqm = response.css(f"table > tbody > tr:nth-child({i}) > td:nth-child(4) > div > span:nth-child(1)::text").get()
                price_sqm = response.css(f"table > tbody > tr:nth-child({i}) > td:nth-child(4) > div > span.text-nowrap.mt-1::text").get()
                build_year = response.css(f"table > tbody > tr:nth-child({i}) > td:nth-child(6) > span::text").get()
                vejnavnnr = response.css(f"table > tbody > tr:nth-child({i}) > td.table-col.d-flex.align-items-center.address-cell > a::text").get()
                kommune = response.xpath(f"/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/app-sold-list-table/table/tbody/tr[{i}]/td[1]/a/text()[2]").get()


                f.write(f"{price};{sold_date};{sqm};{price_sqm};{build_year};{vejnavnnr};{kommune}\n")
        self.log(f'Saved file {filename}')
