import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import argparse
import random, re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import warnings
warnings.filterwarnings("ignore")

# setting default parameters
random.seed(42)
plt.rcParams['figure.figsize'] = (30, 20)


# setting up arguments for file, type of vectorizer
# Preprocessing steps:
# 1. load the database of songs and clean and create tags
# 1. clean text
# 2. tokinize and create clean document


def cleaning(text):
    """
    function to clean the data for the model
    args:
        text: text to clean
    return: cleaned_data
    """
    text = re.sub("[^a-zA-Z0-9]", " ", text)
    text = text.lower()
    text = text.split()
    # stops = set(stopwords.words("english"))
    # text = [w for w in text if not w in stops]
    text = " ".join(text)
    return text


def load_songs(path='C:/TextAI/recommendation system/vishwang/MRS/MRS/training_data/spotify_songs.csv'):
    """
    function to preprocess the data and generate the database for the recommendation engine
    the csv needs to have the same columns as given.
    args:
        path : (optional) the path to the csv file
    returns:
        dfen: the preprocessed dataframe

    """
    df = pd.read_csv(path)
    dfen = df[df['language'] == 'en']
    dfen.dropna(inplace=True, axis=0)
    dfen['lyrics'].replace(
        'Lyrics for this song have yet to be released. Please check back once the song has been released.', None,
        inplace=True)
    dfen.dropna(axis=0, inplace=True)
    dfen['track_album_release_date'] = pd.to_datetime(dfen['track_album_release_date'])
    return dfen


def get_preprocessed_data():
    """
    function to tag the documents and create the final csv for the recommendation engine. this function is the one that
    needs to be called when starting a new instance of the recommendation engine, or when the songs need to be updated

    saves the final csv in the same folder as 'preprocessed_data.csv'
    """
    dfen = load_songs()
    dfen['lyrics'] = dfen['lyrics'].apply(cleaning)
    tagged_data = [TaggedDocument(words=word_tokenize(str(_d).lower()), tags=[str(i)]) for i, _d in
                   enumerate(dfen['lyrics'].tolist())]
    song_details = dfen[['track_name', 'track_artist', 'track_album_name', 'track_id','lyrics']]
    song_details['tags'] = np.zeros(song_details.shape[0])
    for i, t_data in enumerate(tagged_data):
        song_details['tags'].iloc[i] = t_data.tags[0]
    song_details.to_csv('preprocessed_data.csv',index=False)
