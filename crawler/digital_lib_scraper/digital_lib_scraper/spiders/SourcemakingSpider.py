import scrapy
import json


class SpringframeworkSpider(scrapy.Spider):
    name = "sourcemaking"
    allowed_domains = ["sourcemaking.com"]
    start_urls = ["https://https://sourcemaking.com/design_patterns"]

    def parse(self, response):
        
        data = {}

        content = response.xpath('//*[@itemprop="articleBody"]/*')
        h3 = None

        for child in content:
            if child.root.tag == "h3":
                h3 = child.xpath("string()").get()
                data[h3] = []
            elif h3 and child.root.tag == "p":
                data[h3].append(child.xpath("string()").get())
            else:
                h3 = None
        
        with open("../data/StackoverflowSpider.json", "w") as file:
            json.dump(data, file)