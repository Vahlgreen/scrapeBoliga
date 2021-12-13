import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    #start_requests returns (via yield) a request object
    def start_requests(self):
        urls = [
            'https://www.imdb.com/chart/top/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):


        filename = 'top-250.txt'
        with open(filename, 'w') as f:
            tablerows = response.css("#main > div > span > div > div > div.lister > table > tbody > tr") #has 250 rows
            for index in range(1,len(tablerows)+1):
                title = response.css(f"#main > div > span > div > div > div.lister > table > tbody > tr:nth-child({index}) > td.titleColumn > a::text").get()
                f.write(f"Movie number {index} on the IMDB top 250 list is {title}\n")

        self.log(f'Saved file {filename}')