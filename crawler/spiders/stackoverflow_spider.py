from pathlib import Path

import scrapy

class StackOverflowSpider(scrapy.Spider):
    name = "stackoverflow"
    start_urls = [# content after h3 element
        "https://stackoverflow.com/questions/1673841/examples-of-gof-design-patterns-in-javas-core-libraries",
        "https://stackoverflow.blog/2021/10/13/why-solve-a-problem-twice-design-patterns-let-you-apply-existing-solutions-to-your-code/" 
    ]

    def parse(self, response):
        pass