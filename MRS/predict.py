import pandas as pd
import numpy as np
from .preprocessing import get_preprocessed_data, cleaning
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize
import logging  # Setting up the loggings to monitor gensim

logging.basicConfig(filename='prediction_logs.log', format="%(levelname)s - %(asctime)s: %(message)s",
                    datefmt='%H:%M:%S', level=logging.INFO)



def predict(lyrics, model_path='C:/TextAI/recommendation system/vishwang/MRS/models/d2v.model'):
    lyrics = cleaning(lyrics)
    song_details = pd.read_csv('C:/TextAI/recommendation system/vishwang/MRS/preprocessed_data.csv')
    model = Doc2Vec.load(model_path)
    # to find the vector of a document which is not in training data
    # sample = str(dfen.sample()['combined'].values)
    # print(f'sample: {sample}')
    test_data = word_tokenize(lyrics.lower())
    v1 = model.infer_vector(test_data)
    # print("V1_infer", v1)
    #print(song_details['tags'].head(2))
    sims = model.dv.most_similar([v1])
    #print(sims)
    most_similar_songs = pd.DataFrame()
    for tag, percentage in sims:
        #print(type(tag))
       #print(type(song_details['tags'].iloc[0]))
        found = pd.DataFrame(song_details[song_details['tags'] == int(tag)])
        most_similar_songs = pd.concat([most_similar_songs,found])
        t_name = found['track_name']
        # print(found)
        print(
            f"Song: {t_name.values[0]} by {found['track_artist'].values[0]} from album : {found['track_album_name'].values[0]} with similarity percentage: {percentage}")
    return most_similar_songs



