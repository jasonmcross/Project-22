import scrapy


class RefactoringSpider(scrapy.Spider):
    name = "refactoring"
    allowed_domains = ["refactoring.guru"]
    start_urls = ["https://refactoring.guru/design-patterns/catalog"]

    def parse(self, response):
        print(type(response))
        for link in response.xpath('//div[@class="patterns-catalog"]/div/a/@href').getall():
            #print(type(link))
            #response.urljoin(link)
            yield scrapy.Request(response.urljoin(link), callback=self.parse_link)

    def parse_link(self, response):
        data = {}
        #print("butt")
        #try:
        #    print("Passed\t" + response.xpath('//h1[@class="title"]').get())
        data[response.xpath('//h1[@class="title"]').get()] = "".join([p for p in response.xpath('//article/div/p').getall()])
        #except:
        #    print("Failed\t" + response.xpath('//h1[@class="title"]').get())
        #    pass
        #print(data)
        #self.logger.info(data)
        yield data