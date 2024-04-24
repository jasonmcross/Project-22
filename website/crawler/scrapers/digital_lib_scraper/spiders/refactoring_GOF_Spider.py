import scrapy
import csv
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
from database.designPatterns import DatabaseOperations

class refactoring_GOF_Spider(scrapy.Spider):
    name = "refactoring"
    allowed_domains = ["refactoring.guru"]
    start_urls = ["https://refactoring.guru/design-patterns/catalog"]

    def parse(self, response):
        print(type(response))
        pat_links = response.xpath('//div[@class="patterns-catalog"]/div/a/@href').getall()
        for link in pat_links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_patterns, meta={"link": link})

    def parse_patterns(self, response):
        category = response.xpath('//a[@class="type" and contains(@href, "creational") or contains(@href, "structural") or contains(@href, "behavioral")]').xpath("string()").get().replace(" Patterns", "")
        pattern = response.xpath('//h1[@class="title"]').xpath("string()").get()
        data = ""

        for text in response.xpath('//div[@class="section problem"]/p'):
            data += text.xpath("string()").get()

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
