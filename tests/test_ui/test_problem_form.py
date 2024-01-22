import os
import sys
import pytest
from bs4 import BeautifulSoup

VIEW_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "new_format", "website"))
WEBSITE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "new_format"))

sys.path.append(VIEW_PATH)
sys.path.append(WEBSITE_PATH)

from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_words(client):
    resp = client.get('/')
    soup = BeautifulSoup(resp.data, "html.parser")
    
    print(resp.content_type)
    assert False