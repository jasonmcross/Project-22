import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import nltk
import re
import string
from nltk.stem import WordNetLemmatizer

data = pd.read_csv('combined_patterns.csv', encoding='ISO-8859-1',
                   header=None, names=['Pattern', 'Description'])

tfidf = TfidfVectorizer()

X = tfidf.fit_transform(data['Description'])

y = data['Pattern']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = MultinomialNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)


def predict_design_pattern(description, top_n=3):
    transformed_description = tfidf.transform([description])

    probabilities = model.predict_proba(transformed_description)[0]

    top_indicies = np.argsort(probabilities)[-top_n:][::-1]
    top_patterns = [(model.classes_[i], probabilities[i])
                    for i in top_indicies]
    return top_patterns

# test_description = "Add responsibilities to objects dynamically"
# predicted_patterns = predict_design_pattern(test_description)
# for pattern, score in predicted_patterns:
#     print(f"Pattern: {pattern}, Score: {score}")
