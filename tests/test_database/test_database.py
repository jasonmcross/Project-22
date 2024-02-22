import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.curdir, '../..')))
from new_format.neon_python.userDB import DatabaseOperations

#@pytest.fixture
def test_database():
    db = DatabaseOperations()
    assert db
    db.add_user('test@pf.com', 'Pattern Finder', 'password')
    user = db.lookup_user('test@pf.com')
    assert user
    db.remove_user('test@pf.com')
    user = db.lookup_user('test@pf.com')
    assert user is None