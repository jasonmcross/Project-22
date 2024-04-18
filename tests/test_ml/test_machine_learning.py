import pytest
import csv
import os
import sys
import itertools
from pathlib import Path
import pandas as pd
import pickle

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DRIVER_PATH = os.path.join("website", "Strategy")

sys.path.append(PROJECT_PATH)
sys.path.append(DRIVER_PATH)

from website.Strategy.BertPredictor import BertPredictor
from website.Strategy.test import run_test

# Reads CSV file for problems and answers
def read_csv():
    filepath = Path(__file__).parent / "answer_key.csv"
    data = []
    with open(filepath, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append((row['problem'], row['Answer']))
    return data

# Tests Bert predictor
def test_bert_accuracy():
    # Read answer key
    answer_key = read_csv() # Adjust file name accordingly
    
    filepath = Path(__file__).parent.parent.parent / "website/Strategy/source_files/masterGOF.csv"
    pred = BertPredictor(filepath)

    total_questions = len(answer_key)
    
    # Read system output
    system_output = [] 
    for i in range(total_questions):
        system_output.append(pred.predict(answer_key[i][0]))
    
    # Calculate accuracy
    correct_answers = 0
    csv_entries = []
    for i in range(total_questions):
        csv_entries.append({answer_key[i][1]: system_output[i]})
        if answer_key[i][1] == system_output[i][0]["Name"]:
            correct_answers += 1
        elif answer_key[i][1] == system_output[i][1]["Name"]:
            correct_answers += 0.66
        elif answer_key[i][1] == system_output[i][2]["Name"]:
            correct_answers += 0.33
        
    accuracy = (correct_answers / total_questions) * 100
    print(f"System accuracy is {accuracy}%, which is below 60%.")
    
    # Assert if accuracy meets the desired threshold
    assert accuracy >= 60 #, f"System accuracy is {accuracy}%, which is below 60%."

@pytest.mark.parametrize("vector, clusterer", itertools.product(range(1, 2), range(1, 3)))#range(1, 3), range(1, 9)))
def test_custom_accuracy(vector, clusterer):
    preprocess = [1, 1, 1, 1, 0, 0, 0, 0]

    answer_key = read_csv() # Adjust file name accordingly
    total_questions = len(answer_key)
    system_output = [] #read_csv(system_output_file)
    for i in range(total_questions):
        system_output.append(run_test(preprocess, vector, clusterer, answer_key[i][0]))

    print(len(system_output))

    # Calculate accuracy
    correct_answers = 0
    csv_entries = []
    for i in range(total_questions):
        csv_entries.append({answer_key[i][1]: system_output[i]})
        if answer_key[i][1] == system_output[i][0]:
            correct_answers += 1
        elif answer_key[i][1] == system_output[i][1]:
            correct_answers += 0.66
        elif answer_key[i][1] == system_output[i][2]:
            correct_answers += 0.33
        
    accuracy = (correct_answers / total_questions) * 100
    print(f"System accuracy is {accuracy}%, which is below 60%.")
    
    # Assert if accuracy meets the desired threshold
    assert accuracy >= 60 #, f"System accuracy is {accuracy}%, which is below 60%."
