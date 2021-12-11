import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.boliga.dk/salg/resultater?sort=omregnings_dato-d&kode=3&fraPostnr=&tilPostnr=&minsaledate=2004&maxsaledate=today&kom=461&type=Villa&gade=&iPostnr=5000&searchTab=1'
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)