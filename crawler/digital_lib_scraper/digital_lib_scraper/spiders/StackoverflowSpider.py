import scrapy
import json
import os

class StackoverflowSpider(scrapy.Spider):
    name = "stackoverflow"
    allowed_domains = ["stackoverflow.blog"]
    start_urls = [# content after h3 element
        #"https://stackoverflow.com/questions/1673841/examples-of-gof-design-patterns-in-javas-core-libraries",
         "https://stackoverflow.blog/2021/10/13/why-solve-a-problem-twice-design-patterns-let-you-apply-existing-solutions-to-your-code/"
    ]

    def parse(self, response):
        
        data = {}

        parse_str = '//div[@itemprop="articleBody"]/'

        content = response.xpath(parse_str + "h2 | " + parse_str + "h3 | " + parse_str + "p")
        h3 = None

        for child in content:
            if child.root.tag == "h3":
                h3 = child.xpath("string()").get()
                data[h3] = []
            elif h3 and child.root.tag == "p":
                data[h3].append(child.xpath("string()").get())
            else:
                h3 = None

        with open(os.path.abspath(os.path.join(os.getcwd(), "../../../data/stackoverflow.json")), "w") as file:
            json.dump(data, file)