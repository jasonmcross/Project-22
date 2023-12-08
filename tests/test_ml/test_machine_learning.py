import pytest
import os
import sys

cwd = os.path.dirname(__file__)
ml_path = os.path.abspath(os.path.join(cwd, "..", "..", "machinelearning"))
sys.path.append(ml_path)
os.chdir(ml_path)

import classifier

key = [
    ("Singleton Pattern", "A system needs to control access to a resource (like a database connection, a file, or a network resource) among multiple clients efficiently while ensuring that only one client accesses the resource at a time."),
    ("Strategy Pattern", "Design a system where components can be easily added, removed, or replaced without affecting the overall system functionality."),
    ("Factory Method Pattern", "Develop a graphical user interface (GUI) framework that allows users to create different types of UI elements (buttons, text fields, etc.) with custom behavior."),
    ("Command Pattern", "Create a feature that allows users to undo or redo their actions in an application.")
]

@pytest.mark.parametrize("pattern, description", key)
def test_return(pattern, description):
    # Returns a collection of pattern prediction
    resp = classifier.predict_design_pattern(description)
    assert 3 == len(resp)

@pytest.mark.parametrize("pattern, description", key)
def test_predict(pattern, description):
    # Returns a collection of pattern prediction
    resp = classifier.predict_design_pattern(description)
    assert pattern == resp[0][0]