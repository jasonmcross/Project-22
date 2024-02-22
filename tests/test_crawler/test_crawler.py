import os
import sys
import pytest
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

SPIDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "crawler", "digital_lib_scraper", "digital_lib_scraper", "spiders"))
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "crawler", "data"))

sys.path.append(SPIDER_PATH)

from SpringframeworkSpider import SpringframeworkSpider
from StackoverflowSpider import StackoverflowSpider

spider_modules = locals()

@pytest.fixture()
def crawler_runner():
    settings = get_project_settings()
    return CrawlerRunner(settings)

@pytest.mark.parametrize("spider_name", [name for name in spider_modules if name.endswith("Spider")])
@pytest.mark.asyncio
async def test_scrape(crawler_runner, spider_name):
    spider = spider_modules[spider_name]
    print(os.path.join(DATA_PATH, str(spider_name) + ".json"))

    crawler_instance = await crawler_runner.create_crawler(spider)
    await crawler_instance.crawl()
    
    result = crawler_runner.spider.data
    assert len(result) > 0

    assert os.path.exists(os.path.abspath(os.path.join(DATA_PATH, str(spider_name) + ".json")))