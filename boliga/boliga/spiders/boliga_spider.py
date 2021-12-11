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
        #everything below is done for each response, and due to the yield keyword
        #its done before the next request is sent

        filename = 'boliga.txt'
        with open(filename, 'w') as f:
            table=response.css(f"app-sold-list-table") #has 50 rows
            vals = table.css("span.text-nowrap::text").get() #has 250 elements
            for index in range(len(vals)):
                if index%5==0:
                    f.write(f"{vals[index]},{vals[index-2]}\n")

        time.sleep(1)
        self.log(f'Saved file {filename}')