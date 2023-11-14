import scrapy
import json


class SpringframeworkSpider(scrapy.Spider):
    name = "springframework"
    allowed_domains = ["springframework.guru"]
    start_urls = ["https://springframework.guru/gang-of-four-design-patterns/"]

    def parse(self, response):
        
        data = {}

        #content = response.xpath('//article[@class="post-737 page type-page status-publish has-post-thumbnail hentry"]/*')
        #content = content.xpath('//div[@class="entry-content"')
        content = response.xpath('//div[@class="entry-content" and @itemprop="text"]/ul')#//*[@id="post-737"]/div[@class="entry-content"]//*')#
        h3 = None
        #print(content.extract())

        for child in content.xpath('./li'):
            #print(child.xpath('./a').xpath('string()').get())
            data[child.xpath('./a').xpath('string()').get()] = child.xpath('string()').get()
            #print(child)
            #if child.root.tag == "h3":
            #    h3 = child.xpath("string()").get()
            #    #print(child)
            ##s    data[h3] = []
            #if h3 != None and child.root.tag == "ul":
            #    #print(child)
            #    #if child.root.tag == "li":
            #    #    print(child)
            #    ul = child.xpath('//ul')
            #    li_ls = ul.xpath('.//li')
            #    #for li in li_ls:
            #        #data[]
            #        #print(li)
            #        #if li.xpath('a'):
            #        #    data[h3].append({li.xpath('a//text()').get():li.xpath('string(.)').get()})
            #    h3 = None
        
        #print(data) #//*[@id="post-737"]/div[1] /html/body/div[3]/div[2]/div/div/div/article/div[1]
        with open("../data/springframework.json", "w") as file:
            json.dump(data, file)