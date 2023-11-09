import scrapy
import json


class SpringframeworkSpider(scrapy.Spider):
    name = "springframework"
    allowed_domains = ["springframework.guru"]
    start_urls = ["https://springframework.guru/gang-of-four-design-patterns/"]

    def parse(self, response):
        
        data = {}

        article_div = response.xpath('//*[@itemprop="text"]/*')
        #article_div = response.xpath('.//div[@class="parent"]')

        for child in article_div:
            if child.root.tag == "h3":
                h3 = child.xpath("string()").get()
                data[h3] = []
            elif child.root.tag == "ul":
                ul = child.xpath('//ul')
                li_ls = ul.xpath('.//li')
                for li in li_ls:
                    if li.xpath('a'):
                        data[h3].append({li.xpath('a//text()').get():li.xpath('string(.)').get()})
        
        print(data)