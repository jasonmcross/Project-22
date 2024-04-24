import scrapy
import csv
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
from database.designPatterns import DatabaseOperations
from pathlib import Path

class sourcemaking_GOF_Spider(scrapy.Spider):
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

        sections = ("Intent", "Problem", "Motivation", "Discussion")
        resp = response.xpath("//article")
        elements = resp.xpath("//h3 | //p | //ul")

        category = response.meta.get("categories").xpath("string()").get().replace(" patterns", "")
        pattern = resp.xpath("//h1").xpath("string()").get().replace(" Design Pattern", "") 
        data = ""
        h3 = False

        for element in elements:
            if element.xpath("name()").extract_first() == "h3":
                h3 = any(element.xpath("string()").get() == section for section in sections)
            elif h3:
                if element.xpath("name()").extract_first() == "ul":
                    for li in element.xpath("./li"):
                        data += li.xpath("string()").get()
                elif element.xpath("name()").extract_first() == "p":
                    data += element.xpath("string()").get()
        
        out_data = {
            "Category": category,
            "Pattern": pattern,
            "Data": data.replace("\n", " ").replace("’", "'").replace(",", ""),
            "Library": self.name.capitalize(),
            "Collection": "GOF"
        }

        self.write_to_csv(out_data)

    def write_to_csv(self, data):
        db_ops = DatabaseOperations()
        db_ops.delete_rows_by_combination("refactoring", "GOF")
        path = "data/MasterSpider.csv"
        filepath = Path(__file__).parent.parent.parent.parent / path
        with open(filepath, "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Category", "Pattern", "Data", "Library", "Collection"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data)
