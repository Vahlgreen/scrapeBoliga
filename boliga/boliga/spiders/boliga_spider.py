import scrapy
import time

class BoligaSpider(scrapy.Spider):
    name = "boliga"

    #start_requests returns (via yield) a request object
    def start_requests(self):
        urls = [
            'https://www.boliga.dk/salg/resultater?sort=omregnings_dato-d&kode=3&fraPostnr=&tilPostnr=&minsaledate=2004&maxsaledate=today&kom=461&type=Villa&gade=&searchTab=1&page=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    #when start_request is called, scrapy.request returns a response object that is parsed to parse
    def parse(self, response):

        filename = 'boliga.txt'
        with open(filename, 'w') as f:

            for i in range(1,50):
                row = response.css(f"table > tbody > tr:nth-child({i}) > td:nth-child(2) > span::text").get()
                if row is not None:
                    row = row[:-4]
                f.write(f"{row}\n")

        self.log(f'Saved file {filename}')


