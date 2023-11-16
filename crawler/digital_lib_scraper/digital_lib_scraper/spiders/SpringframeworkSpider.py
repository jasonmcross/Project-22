import scrapy
import json


class SpringframeworkSpider(scrapy.Spider):
    name = "springframework"
    allowed_domains = ["springframework.guru"]
    start_urls = ["https://springframework.guru/gang-of-four-design-patterns/"]

    def parse(self, response):
        
        data = {}

        content = response.xpath('//div[@class="entry-content" and @itemprop="text"]/ul')#//*[@id="post-737"]/div[@class="entry-content"]//*')#
        h3 = None

        for child in content.xpath('./li'):
            data[child.xpath('./a').xpath('string()').get()] = child.xpath('string()').get()
        
        with open("../data/SpringframeworkSpider.json", "w") as file:
            json.dump(data, file)