import os
import sys
import pytest
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

SPIDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "crawler", "digital_lib_scraper", "digital_lib_scraper", "spiders"))
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "crawler", "data"))

sys.path.append(SPIDER_PATH)

from SpringframeworkSpider import SpringframeworkSpider
from StackoverflowSpider import StackoverflowSpider
from SourcemakingSpider import SourcemakingSpider

spiders_module = locals()

@pytest.fixture()
def crawler_runner():
    settings = get_project_settings()
    return CrawlerRunner(settings)

@pytest.mark.parametrize("spider_name", [name for name in spiders_module if name.endswith("Spider")])
def test_scrape(crawler_runner, spider_name):
    spider = spiders_module[spider_name]
    runner = crawler_runner
    print(os.path.join(DATA_PATH, str(spider_name) + ".json"))

    crawler_instance = runner.create_crawler(spider)
    runner.crawl(crawler_instance)
    
    assert os.path.exists(os.path.abspath(os.path.join(DATA_PATH, str(spider_name).rstrip("Spider").lower() + ".json")))