from pymongo import MongoClient
import pytest

@pytest.fixture
def database():
    client = MongoClient('ip_addr', 22222)
    db = client['database_name']
    data = {"Factory Pattern": "A creational pattern used in software development to create objects without specifying the exact class of the object that will be created. It provides an interface for creating objects but allows subclasses to alter the type of objects that will be instantiated."}
    return(db["collection_name"], data)

def test_insert(database):
    db, data = database
    res = db.insert_one(data)
    assert res

def test_delete(database):
    db, data = database
    res = db.delete_one(data)
    assert res