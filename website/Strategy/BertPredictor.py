import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import re

class BertPredictor:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path, header=None)
        self.data.columns = ['Category', 'Name', 'Description']
        self.data['Preprocessed_Description'] = self.data['Description'].apply(self.preprocess)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.embeddings = self._compute_embeddings()

    def preprocess(self, text):
        text = text.lower()
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _compute_embeddings(self):
        embeddings = []
        for desc in self.data['Preprocessed_Description']:
            inputs = self.tokenizer(desc, return_tensors='pt', padding=True, truncation=True, max_length=128)
            outputs = self.model(**inputs)
            sentence_embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
            embeddings.append(sentence_embedding)
        return embeddings


    def predict(self, user_input):
        user_inputs = self.tokenizer(user_input, return_tensors='pt', padding=True, truncation=True, max_length=128)
        user_outputs = self.model(**user_inputs)
        user_embedding = user_outputs.last_hidden_state.mean(dim=1).detach().numpy()
        user_embedding = user_embedding.reshape(1, -1)  # Reshape to 2D array

        # Reshape each embedding in self.embeddings to a 2D array
        reshaped_embeddings = [emb.reshape(1, -1) for emb in self.embeddings]

        similarity_scores = [cosine_similarity(user_embedding, emb).flatten()[0] for emb in reshaped_embeddings]

        results = pd.DataFrame({
            'Score': similarity_scores,
            'Name': self.data['Name'],
            'Category': self.data['Category']
        })

        sorted_results = results.sort_values(by='Score', ascending=False).drop_duplicates(subset=['Name', 'Category'])

        return sorted_results.head(3).to_dict('records')


def main():
    predictor = BertPredictor('sourceFiles/masterGOF.csv')
    while True:
        user_input = input("Enter your design problem: ")
        best_patterns = predictor.predict(user_input)
        print("Best matching design patterns:")
        for pattern in best_patterns:
            print(f"Name: {pattern['Name']}, Category: {pattern['Category']}, Similarity Score: {pattern['Score']}")

if __name__ == "__main__":
    main()