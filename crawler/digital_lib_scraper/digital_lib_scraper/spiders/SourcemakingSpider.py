import scrapy
import json
import os

class SourcemakingSpider(scrapy.Spider):
    name = "sourcemaking"
    allowed_domains = ["sourcemaking.com"]
    start_urls = ["https://sourcemaking.com/design_patterns"]

    def parse(self, response):

        cat_links = response.xpath('//article/h3/a/@href').getall()

        for link in cat_links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_categories, meta={'result': cat_links})

    def parse_categories(self, response):

        categories = response.xpath("//article/h1")
        pat_links = response.xpath("//article/ul/li/a/@href").getall()

        for link in pat_links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_patterns, meta={"categories": categories})

    def parse_patterns(self, response):

        resp = response.xpath("//article")
        h1 = resp.xpath("//h1")#/strong/text()").get()#.xpath("string()").get()

        category = response.meta.get("categories")
        print(h1.xpath("string()").get().replace(" Design Pattern", ""))