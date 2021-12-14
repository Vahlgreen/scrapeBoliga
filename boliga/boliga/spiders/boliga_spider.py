
import scrapy

class BoligaSpider(scrapy.Spider):
    name = "boliga"
    start_urls = []
    for i in range(1,261):
        start_urls.append(f"https://www.boliga.dk/salg/resultater?sort=omregnings_dato-d&kode=3&fraPostnr=&tilPostnr=&minsaledate=2004&maxsaledate=today&kom=&type=Villa&gade=&searchTab=1&page={i}")




    #['https://www.boliga.dk/salg/resultater?sort=omregnings_dato-d&kode=3&fraPostnr=&tilPostnr=&minsaledate=2004&maxsaledate=today&kom=&type=Villa&gade=&searchTab=1&page=1']
    #,"https://www.boliga.dk/salg/resultater?sort=omregnings_dato-d&kode=3&fraPostnr=&tilPostnr=&minsaledate=2004&maxsaledate=today&kom=461&type=Villa&gade=&searchTab=1&page=2",
    #   "https://www.boliga.dk/salg/resultater?sort=omregnings_dato-d&kode=3&fraPostnr=&tilPostnr=&minsaledate=2004&maxsaledate=today&kom=461&type=Villa&gade=&searchTab=1&page=3"]


    def parse(self, response):

        filename = 'boliga.txt'
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
