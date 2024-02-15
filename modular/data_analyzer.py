import pandas as pd
import os
from collections import defaultdict
from nltk.tokenize import word_tokenize
import csv
from pathlib import Path

def main():
    filename = os.path.abspath(os.path.join(__file__, '..', 'masterGOF_stop.csv'))
    df = pd.read_csv(filename, header=None)
    df.columns = ['Category', 'Pattern', 'Text']    

    word_freq = defaultdict(lambda: defaultdict(int))
    for ind, row in df.iterrows():
        cat = row['Category']
        text = row['Text']
        words = word_tokenize(text.lower())
        for word in words:
            word_freq[cat][word] += 1

    with open('word_freq_master.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Category', 'Word', 'Frequency'])
        for cat, freqs in word_freq.items():
            for word, freq in freqs.items():
                csvwriter.writerow([cat, word, freq])

if __name__ == '__main__':
    main()