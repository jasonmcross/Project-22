import preprocessing as pp
import cluster_plot as cp
import vectorizer as vec
import predictor as pred
import pandas as pd
from pathlib import Path

def trainIt(data: pd.DataFrame, preproc, vect, cls):    

    df = data

    if preproc == "junk":
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lower_punc)
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.remove_stop)
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.remove_junk)
    elif preproc == "stem":
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lower_punc)
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.remove_stop)
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.stem)
    elif preproc == "tokenize":
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lower_punc)
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.remove_stop)
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.tokenize)
    elif preproc == "lemma":
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lower_punc)
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.remove_stop)
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lemma)
    elif preproc == "nouns_verbs":
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lower_punc)
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.remove_stop)
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.extract_nouns_verbs)
    elif preproc == "synonymize":
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lower_punc)
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.remove_stop)
        df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.synonymize)

    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lower_punc)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.remove_stop)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.remove_junk)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.stem)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.tokenize)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.lemma)    
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.extract_nouns_verbs)
    #df.iloc[:, 2] = df.iloc[:,2].astype(str).apply(pp.synonymize)    

    return df