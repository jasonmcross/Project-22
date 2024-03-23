import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

class BertPredictor:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path, header=None)
        self.data.columns = ['Category', 'Name', 'Preprocessed_Description']
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.embeddings = self._compute_embeddings()

    def _compute_embeddings(self):
        embeddings = []
        for desc in self.data['Preprocessed_Description']:
            inputs = self.tokenizer(desc, return_tensors='pt', padding=True, truncation=True, max_length=128)
            outputs = self.model(**inputs)
            # Use the mean of the last hidden states as the sentence embedding
            sentence_embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
            embeddings.append(sentence_embedding)
        return embeddings


    def find_best_patterns(self, user_input):
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
    predictor = BertPredictor('../source_files/masterGOF.csv')
    while True:
        user_input = input("Enter your design problem: ")
        best_patterns = predictor.find_best_patterns(user_input)
        print("Best matching design patterns:")
        for pattern in best_patterns:
            print(f"Name: {pattern['Name']}, Category: {pattern['Category']}, Similarity Score: {pattern['Score']}")

if __name__ == "__main__":
    main()




#--------------------------------#

# import pandas as pd
# from transformers import BertTokenizer, BertModel
# import torch
# from sklearn.metrics.pairwise import cosine_similarity

# class BertCategoryPredictor:
#     def __init__(self, categories_path, patterns_path):
#         self.categories_data = pd.read_csv(categories_path, header=None)
#         self.categories_data.columns = ['Category', 'Preprocessed_Description']
#         self.patterns_data = pd.read_csv(patterns_path, header=None)
#         self.patterns_data.columns = ['Category', 'Name', 'Preprocessed_Description', 'Additional_Column']
#         self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#         self.model = BertModel.from_pretrained('bert-base-uncased')
#         self.category_embeddings = self._compute_embeddings(self.categories_data['Preprocessed_Description'])
#         self.pattern_embeddings = self._compute_embeddings(self.patterns_data['Preprocessed_Description'])

#     def _compute_embeddings(self, descriptions):
#         embeddings = []
#         for desc in descriptions:
#             inputs = self.tokenizer(desc, return_tensors='pt', padding=True, truncation=True, max_length=128)
#             outputs = self.model(**inputs)
#             sentence_embedding = outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
#             embeddings.append(sentence_embedding)
#         return embeddings

#     def _find_best_category(self, user_input):
#         user_inputs = self.tokenizer(user_input, return_tensors='pt', padding=True, truncation=True, max_length=128)
#         user_outputs = self.model(**user_inputs)
#         user_embedding = user_outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

#         similarity_scores = cosine_similarity([user_embedding], self.category_embeddings).flatten()
#         best_category_index = similarity_scores.argmax()
#         return self.categories_data.iloc[best_category_index]['Category']

#     # def find_best_patterns(self, user_input):
#     #     best_category = self._find_best_category(user_input)
#     #     print(f"Detected Design Pattern Category: {best_category}")

#     #     category_patterns = self.patterns_data[self.patterns_data['Category'] == best_category]
#     #     category_embeddings = [self.pattern_embeddings[i] for i in category_patterns.index]

#     #     user_inputs = self.tokenizer(user_input, return_tensors='pt', padding=True, truncation=True, max_length=128)
#     #     user_outputs = self.model(**user_inputs)
#     #     user_embedding = user_outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

#     #     similarity_scores = cosine_similarity([user_embedding], category_embeddings).flatten()
#     #     sorted_indices = similarity_scores.argsort()[::-1]
#     #     top_indices = sorted_indices[:3]

#     #     results = category_patterns.iloc[top_indices]
#     #     return results.to_dict('records')
#     def find_best_patterns(self, user_input):
#         best_category = self._find_best_category(user_input)
#         print(f"Detected Design Pattern Category: {best_category}")

#         category_patterns = self.patterns_data[self.patterns_data['Category'] == best_category]
#         category_embeddings = [self.pattern_embeddings[i] for i in category_patterns.index]

#         user_inputs = self.tokenizer(user_input, return_tensors='pt', padding=True, truncation=True, max_length=128)
#         user_outputs = self.model(**user_inputs)
#         user_embedding = user_outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

#         similarity_scores = cosine_similarity([user_embedding], category_embeddings).flatten()
#         sorted_indices = similarity_scores.argsort()[::-1]
#         top_indices = sorted_indices[:3]

#         results = category_patterns.iloc[top_indices]
#         results['Score'] = similarity_scores[top_indices]  # Add the similarity scores to the results
#         return results.to_dict('records')

# def main():
#     predictor = BertCategoryPredictor('../source_files/DP_cat.csv', '../source_files/masterGOF_junk.csv')
#     user_input = input("Enter your design problem: ")
#     best_patterns = predictor.find_best_patterns(user_input)
#     print("Best matching design patterns:")
#     for pattern in best_patterns:
#         print(f"Name: {pattern['Name']}, Category: {pattern['Category']}, Similarity Score: {pattern['Score']}")

# if __name__ == "__main__":
#     main()
