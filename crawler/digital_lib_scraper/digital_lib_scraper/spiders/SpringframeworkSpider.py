import scrapy
import json
import os

class SpringframeworkSpider(scrapy.Spider):
    name = "springframework"
    allowed_domains = ["springframework.guru"]
    start_urls = ["https://springframework.guru/gang-of-four-design-patterns/"]

    def parse(self, response):
        
        data = {}

        content = response.xpath('//div[@class="entry-content" and @itemprop="text"]/ul')
        h3 = None

        for child in content.xpath('./li'):
            data[child.xpath('./a').xpath('string()').get()] = child.xpath('string()').get()
        
        with open(os.path.abspath(os.path.join(os.getcwd(), "../../../data/springframework.json")), "w") as file:
            json.dump(data, file)