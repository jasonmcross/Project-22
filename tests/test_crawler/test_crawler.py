import os
import sys
import pytest
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import defer

SPIDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "website", "crawler", "scrapers", "digital_lib_scraper", "spiders"))
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "website", "crawler", "data"))

sys.path.append(SPIDER_PATH)

from refactoring_GOF_Spider import refactoring_GOF_Spider
from sourcemaking_GOF_Spider import sourcemaking_GOF_Spider

spider_modules = locals()

@pytest.fixture()
def crawler_runner():
    settings = get_project_settings()
    return CrawlerRunner(settings)

@pytest.mark.parametrize("spider_name", [name for name in spider_modules if name.endswith("Spider")])
@pytest.mark.twisted
async def test_scrape(crawler_runner, spider_name):
    deferred = crawler_runner.crawl(spider_name)

    def check_response(results):
        # Access the data produced by the spider
        spider_output = [item for item in results if isinstance(item, dict)]

        # Ensure data was yielded
        assert len(spider_output) > 0  
        # Check for a status key
        assert "status" in spider_output[0]  
        # Verify HTTP status is 200
        assert spider_output[0]["status"] == 200  
        return results

    deferred.addCallback(check_response)
    return deferred