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

    form =  soup.find("form")
    assert form is not None

    problem_input = form.find("input", {"id": "problem"})
    assert problem_input is not None
    problem_input["value"] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget est nec ligula volutpat congue. Quisque vel tellus ac elit iaculis tincidunt. Phasellus tristique, velit vitae eleifend luctus, orci mauris dignissim justo, eu euismod est quam vitae elit. Fusce aliquet velit at nisi aliquam, vitae vulputate justo rhoncus. Duis sed ex vel urna ullamcorper commodo eget vel massa. Nam id nisl at nunc condimentum scelerisque. Sed malesuada turpis a risus tristique, vel ultrices augue facilisis. Integer auctor elit a mauris sagittis, sit amet ultrices purus interdum. Integer accumsan fermentum elit, vel semper eros dignissim et. Ut ac turpis id ipsum scelerisque malesuada eget ac metus. Vestibulum eget felis vel elit ullamcorper congue. Duis convallis odio id orci tristique rhoncus. Vivamus auctor, odio eu convallis iaculis, elit sem fermentum libero, ut congue felis metus non risus. Integer vestibulum, velit non suscipit volutpat, libero elit ultricies justo, eget facilisis justo tellus vitae risus. Suspendisse vel efficitur sem. Nam tincidunt odio eu malesuada feugiat. Suspendisse hendrerit, lacus eu bibendum volutpat, dui elit dictum ligula, vitae sollicitudin turpis libero id mi. Ut ut mauris sed nisi aliquam posuere vel eu justo. Sed vel turpis ut tortor sollicitudin dictum. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Morbi nec nisl ac sapien blandit bibendum. Donec ac lorem vitae neque imperdiet feugiat id nec felis. Quisque varius elit eu justo bibendum, a hendrerit arcu suscipit. Sed tincidunt efficitur urna, sit amet volutpat mauris gravida eu. Nunc id lectus justo. Maecenas vitae laoreet metus. Fusce id risus non metus fermentum hendrerit eu sit amet urna. Fusce tristique, justo et sagittis bibendum, libero leo tincidunt arcu, vel suscipit libero justo ac elit. Sed eu sodales sapien. Curabitur euismod ex a nunc accumsan bibendum. Sed varius, felis in ultrices convallis, metus sem malesuada quam, ac consectetur urna augue vel quam. In hac habitasse platea dictumst. Proin scelerisque sapien vel urna tristique bibendum. Pellentesque volutpat risus ac libero efficitur, nec sodales mi gravida. Vivamus ac ultrices lacus. Morbi at purus metus. Vivamus hendrerit risus ut est aliquet, id varius erat malesuada. Integer tincidunt sapien eu augue malesuada, at ultricies lectus feugiat. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Fusce aliquet purus quam, eu auctor nunc bibendum ac. Integer euismod feugiat volutpat. Curabitur nec fringilla massa. In hac habitasse platea dictumst. Etiam auctor laoreet diam ac congue. Quisque quis felis vel orci fermentum hendrerit. Morbi rhoncus ipsum ut urna congue, et egestas purus fermentum. Nullam facilisis turpis eget tortor ultrices, vel dignissim mauris eleifend. Aenean ut eleifend tortor. Sed bibendum tristique sagittis. Nullam eu mi vel libero facilisis feugiat. Vestibulum et velit a elit commodo interdum et ut turpis. In hac habitasse platea dictumst. Fusce sagittis turpis non arcu interdum, in fermentum lectus vulputate. Integer varius, eros eu imperdiet vulputate, justo mi feugiat elit, at consequat nisi orci vel mauris. Nunc id urna sit amet velit suscipit auctor. Suspendisse potenti. Proin at justo sed massa luctus lacinia. Integer vel convallis elit, ut blandit tellus. Etiam vel dolor et odio condimentum pellentesque a et tortor. Sed pulvinar orci at libero tempus, et euismod justo tristique. Integer non urna nec orci euismod malesuada. Duis ac mauris ut urna elementum imperdiet nec ac elit. Nunc ullamcorper sem non odio cursus, eu luctus ex bibendum."

    collection_select = soup.find("select", {"id": "collection"})
    assert collection_select is not None

    collection_option = soup.find("option", {"value": "All"})
    collection_option["selected"] = True

    

    print(soup)
    assert False