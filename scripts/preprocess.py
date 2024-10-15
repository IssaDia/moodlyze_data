import os
import sys
sys.path.insert(0, os.path.abspath(".."))
import pandas as pd
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
from data.cleaning.cleaning import (
    clean_special_characters, remove_mentions, remove_urls, to_lowercase,
    remove_numbers, remove_extra_spaces, replace_emojis, correct_spelling, tokenize
)

def load_data(file_path):
    columns = ['ignore', 'id', 'date', 'query', 'user', 'tweet']
    df = pd.read_csv(file_path, header=None, names=columns, encoding='latin1', usecols=[1, 2, 4, 5])
    return df

def join_words(words):
    """Reconvertir une liste de mots en une chaîne de caractères."""
    return ' '.join(words)

def preprocess(df):
    df['tweet'] = df['tweet'].astype(str) 
    df['tweet'] = df['tweet'].apply(remove_mentions)
    df['tweet'] = df['tweet'].apply(remove_urls)
    df['tweet'] = df['tweet'].apply(clean_special_characters)
    df['tweet'] = df['tweet'].apply(to_lowercase)
    df['tweet'] = df['tweet'].apply(remove_numbers)
    df['tweet'] = df['tweet'].apply(remove_extra_spaces)
    df['tweet'] = df['tweet'].apply(replace_emojis)
    # df['tweet'] = df['tweet'].apply(join_words)  # Reconvertir la liste en chaîne de caractères
    # df['tweet'] = df['tweet'].apply(correct_spelling)
    df['tweet'] = df['tweet'].apply(tokenize)
   
    return df

if __name__ == "__main__":
    input_file_path = "raw/raw_tweets.csv"
    output_file_path = "processed/cleaned_tweets.csv"
    
    df = load_data(input_file_path)
    if df.empty:
        print(f"Erreur : Aucune donnée n'a été chargée depuis {input_file_path}. Veuillez vérifier le chemin du fichier.")
    else:
        print("Les données ont été chargées avec succès !")
        print(f"Taille du DataFrame : {df.shape}")
        print("Premières lignes du DataFrame :")
      #  print(df.head())
    
    ddf = dd.from_pandas(df, npartitions=4)
    with ProgressBar():
        ddf = ddf.map_partitions(preprocess, meta=df).compute(scheduler='processes')
    
    ddf.to_csv(output_file_path, index=False)
    print(f"Données nettoyées enregistrées sous : {output_file_path}")
