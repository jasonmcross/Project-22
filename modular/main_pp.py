import preprocessing as pp
import cluster_plot as cp
import vectorizer as vec
import predictor as pred
import trainer as train
import pandas as pd
from pathlib import Path

def main():
    filepath = Path(__file__).parent / "source_files/masterGOF.csv"
    df = pd.read_csv(filepath, encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])

    preproc = "input from website"
    vect = "input from website"
    cls = "input from website"
    input = "input from website"

    df = train.trainIt(df, preproc, vect, cls)
    pred.predictIt(input, df)
    
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lower_punc)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.remove_stop)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.remove_junk)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.stem)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.tokenize)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lemma)    
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.extract_nouns_verbs)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.synonymize)
    

    #features_default = vec.vectorize_default(df)
    #features_ngram = vec.vectorize_ngram(df)

    #cp.kmeans(features_default, df)
    #cp.kmeans(features_ngram, df)
    #cp.mbkmeans(features_default, df)
    #cp.mbkmeans(features_ngram, df)
    #cp.agglomerative(features_default, df)
    #cp.agglomerative(features_ngram, df)
    #cp.dbscan(features_default, df)
    #cp.dbscan(features_ngram, df)
    #cp.spectral(features_default, df)
    #cp.spectral(features_ngram, df)
    #cp.mean_shift(features_default, df)
    #cp.mean_shift(features_ngram, df)
    #cp.gaussion_mixture(features_default, df)
    #cp.gaussion_mixture(features_ngram, df)
    #cp.fuzzy_cmean(features_default, df)
    #cp.fuzzy_cmean(features_ngram, df)

if __name__ == "__main__":
    main()