import scrapy
import csv
import os

class RefactoringSpider(scrapy.Spider):
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
            "Data": data
        }

        self.write_to_csv(out_data)

    def write_to_csv(self, data):
        with open(os.path.abspath(os.path.join(os.getcwd(), "../../../data/refactoring.csv")), "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Category", "Pattern", "Data"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data)