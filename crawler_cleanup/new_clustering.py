import pandas as pd
import os
import csv
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import re
import numpy as np

# Project main directory#os.path.abspath(os.path.join(__file__, '..', '..'))

def extract_nouns_verbs(data):
    tokens = word_tokenize(data)
    tagged = pos_tag(tokens)
#    remove_punc = lambda text: re.sub(r'[^\w\s]', '', text)
    nouns_verbs = [word for word, pos in tagged if (pos.startswith('V') or pos.startswith('N'))]
    return(list(set(nouns_verbs)))

def lemmatize_words(words):
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word, pos='v') for word in words]
    return(lemmas)

def synonymizer(words):
    synonyms = set()
    for word in words:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
    return(list(synonyms))

def preprocess(cat: list, desc: list, weight_df: pd.DataFrame):

    df_dict = {}
    #print(weight_df['Word'].apply(synonymizer))
    df_dict['cat'] = cat
    df_dict['desc'] = desc
    df = pd.DataFrame(df_dict)
    #df = data
    #print(type(df['Description']))
    df['tokens'] = df['desc'].apply(word_tokenize)
    df['nouns_verbs'] = df['desc'].apply(extract_nouns_verbs)
    df['lemmas'] = df['nouns_verbs'].apply(lemmatize_words)
    df['keywords'] = df['lemmas'].apply(synonymizer)
    return(df, set(keyword for sublist in df['keywords'] for keyword in sublist))

def plot_clusters(k, matrix):

    pca = PCA(n_components=2, random_state = 0)
    reduced_features = pca.fit_transform(matrix.toarray())
    reduced_cluster_centers = pca.transform(k.cluster_centers_)
    
    plt.scatter(reduced_features[:,0], reduced_features[:,1], c=k.labels_)
    plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
    plt.title("Pattern Clusters")
    plt.xlabel("PCA Feature 1")
    plt.ylabel("PCA Feature 2")
    plt.show()

def main():
    PATH = join_path(__file__, '..', '..')
    data_d = []
    data_c = []
    csv_files = []
    file_dir = join_path(PATH, 'crawler', 'data')
    for file in os.listdir(file_dir):
        with open(join_path(file_dir, file), 'r', encoding='utf-8') as crawl_data:
            csv_reader = csv.reader(crawl_data)
            for row in csv_reader:
                category = row[0].lower()
                description = row[2].lower()
                data_c.append(category)
                data_d.append(description)
        
        csv_files.append(pd.read_csv(join_path(file_dir, file), names=['Category', 'Pattern', 'Description']))
    
    comparison_df = pd.concat(csv_files, axis=0,)# ignore_index=False)
    #print(comparison_df.head())
    #comparison_df.index = ['Category', 'Pattern', 'Description'] 

    cluster_weights = {'create': 2, 'behavior': 2, 'relationship': 2}
    weight_df = pd.DataFrame(list(cluster_weights.items()), columns=['Word', 'Weigth'])


    # Preprocessing
    df, keywords = preprocess(data_c, data_d, weight_df)


    for lemma in df['lemmas'][0]:
        keywords.add(lemma)
    vocab = {word: ind for ind, word in enumerate(keywords)}
    #print(len(comparison_df))
    tfidf_vect = TfidfVectorizer(vocabulary=vocab, stop_words=['english'], ngram_range=(1,2))
    #print(df['desc'].apply(' '.join))
    tfidf_mtrx = tfidf_vect.fit_transform(df['lemmas'].apply(' '.join))# + df['keywords'].apply(' '.join))
    for word, weight in cluster_weights.items():
        word_ind = tfidf_vect.vocabulary_.get(word)
        if word_ind is not None:
            tfidf_mtrx[:, word_ind] *= weight
    kmeans = KMeans(n_clusters=3, random_state=0)
    feats = kmeans.fit(tfidf_mtrx)
    df['cluster'] = kmeans.labels_
    #plot_clusters(feats, tfidf_mtrx)
    
    designproblems = [
        "Design a drawing editor. A design is composed of the graphics (lines, rectangles and roses), positioned at precise positions. Each graphic form must be modeled by a class that provides a method draw(): void. A rose is a complex graphic designed by a black-box class component. This component performs this drawing in memory, and provides access through a method getRose(): int that returns the address of the drawing. It is probable that the system evolves in order to draw circles",
        "Design a DVD market place work. The DVD marketplace provides DVD to its clients with three categories: children, normal and new. A DVD is new during some weeks, and after change category. The DVD price depends on the category. It is probable that the system evolves in order to take into account the horror category",
        "Many distinct and unrelated operations need to be performed on node objects in a heterogeneous aggregate structure. You want to avoid 'polluting00' the node classes with these operations. And, you do not want to have to query the type of each node and cast the pointer to the appropriate type before performing the desired operation"
    ]
    #_, input_keywords = preprocess(designproblems, weight_df)
    #print(len(input_keywords))
    #input_tdidf = tfidf_vect.transform(designproblems)
    #cluster_data = pd.DataFrame({'point': range(len(comparison_df)), 'cluster': comparison_df['cluster']})
    #cluster_data[]
    #predictions = kmeans.predict(input_tdidf)
    #patterns = comparison_df[kmeans.labels_ == predictions]
    print(df.head())
    #print(len(input_tdidf))
    #cluster = kmeans.predict(input_tdidf)
    #print(cluster)
    #patterns = comparison_df[kmeans.labels_ == cluster]
    #similarities = cosine_similarity(input_tdidf, tfidf_vect.transform(patterns['Description'].values))
    #similar_ind = np.argmax(similarities)
    #similar_pattern = patterns.iloc[similar_ind]
    #print(similar_pattern['Category'], similar_pattern['Pattern'])
    #print(input_keywords)
    #plt.figure(figsize=(8, 6))
    #plt.scatter(feats[:,0], feats[:,1])
    #plt.show()
    #print(tfidf_mtrx)
    #dense = tfidf_mtrx.toarray()
    #np.save('matrix.npy', dense)
    comparison_df.to_csv('compare.csv', mode='w')
    df.to_csv('out.csv', index=False, header=False, mode='w')

def join_path(*args):
    return(os.path.abspath(os.path.join(*args)))

if __name__ == "__main__":
    main()