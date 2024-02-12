import preprocessing as pp
import cluster_plot as cp
import vectorizer as vec
import pandas as pd
from pathlib import Path

def main():
    filepath = Path(__file__).parent / "source_files/masterGOF.csv"
    df = pd.read_csv(filepath, encoding='ISO-8859-1',
                   header=None, names=['Category', 'Pattern', 'Description'])

    df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lower_punc)
    df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.remove_stop)
    df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.stem)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lemma)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.tokenize)

    #features_default = vec.vectorize_default(df)
    features_ngram = vec.vectorize_ngram(df)

    #cp.kmeans(features_default, df)
    cp.kmeans(features_ngram, df)
    #cp.mbkmeans(features_default, df)
    cp.mbkmeans(features_ngram, df)

if __name__ == "__main__":
    main()