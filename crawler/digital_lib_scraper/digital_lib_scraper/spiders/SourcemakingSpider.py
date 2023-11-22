import scrapy
import json
import os

class SpringframeworkSpider(scrapy.Spider):
    name = "sourcemaking"
    allowed_domains = ["sourcemaking.com"]
    start_urls = ["https://sourcemaking.com/design_patterns"]

    def parse(self, response):
        
        data = {}

        content = response.xpath('//article/ul/li[a and br]')

        for elements in content:
            # Gets element string, strips, and split the strings into a list on newline characters
            # 0 - Pattern Title, 1 -  Pattern Description
            strls = elements.xpath("string()").get().strip().splitlines()
            title = strls[0]
            descr = strls[1]
            data[title] = descr.strip()

        with open(os.path.abspath(os.path.join(os.getcwd(), "../../../data/sourcemaking.json")), "w") as file:
            json.dump(data, file)
        