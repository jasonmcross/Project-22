#data = pd.read_csv('../source_files/masterGOF_junk.csv', header=None)
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the preprocessed data
data = pd.read_csv('../source_files/masterGOF_junk.csv', header=None)
data.columns = ['Category', 'Name', 'Preprocessed_Description', 'Additional_Column']

# Convert the descriptions to TF-IDF vectors
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(data['Preprocessed_Description'])

# Function to find the best matching design patterns
def find_best_patterns(user_input):
    # Convert the user input to a TF-IDF vector
    user_vector = vectorizer.transform([user_input])

    # Calculate cosine similarity between user input and all descriptions
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix)[0]

    # Create a DataFrame with similarity scores, names, and categories
    results = pd.DataFrame({
        'Score': similarity_scores,
        'Name': data['Name'],
        'Category': data['Category']
    })

    # Sort the results by score in descending order and remove duplicates
    sorted_results = results.sort_values(by='Score', ascending=False).drop_duplicates(subset=['Name', 'Category'])

    # Return the top 3 unique matching design patterns and their scores
    return sorted_results.head(3).to_dict('records')

# Main function to interact with the user
def main():
    user_input = input("Enter your design problem: ")
    best_patterns = find_best_patterns(user_input)
    print("Best matching design patterns:")
    for pattern in best_patterns:
        print(f"Name: {pattern['Name']}, Category: {pattern['Category']}, Similarity Score: {pattern['Score']}")

if __name__ == "__main__":
    main()
