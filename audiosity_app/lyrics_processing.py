import sqlite3
import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer
import heapq

model = SentenceTransformer("all-MiniLM-L6-v2")


def chunking(lyrics):
    # remove start of song artifacts
    stripped = re.sub(r'.*?Contributors.*?\[.*?\]', '', lyrics)
    # remove song structure comments
    stripped = re.sub(r'\[.*?\]', '', stripped)
    # split song texts into lines by splitting at newline characters
    stripped = stripped.splitlines()
    # removing empty entries
    stripped = [line for line in stripped if line.strip()]
    # remove end of song artifacts
    stripped[-1] = re.sub(r'\d+Embed$', "", stripped[-1])
    return stripped



def cosine_similarity(x, y):
    
    # Ensure length of x and y are the same
    if len(x) != len(y) :
        return None
    
    # Compute the dot product between x and y
    dot_product = np.dot(x, y)
    
    # Compute the L2 norms (magnitudes) of x and y
    magnitude_x = np.sqrt(np.sum(x**2)) 
    magnitude_y = np.sqrt(np.sum(y**2))
    
    # Compute the cosine similarity
    cosine_similarity = dot_product / (magnitude_x * magnitude_y)
    
    return cosine_similarity


def find_matches(df, input_phrase):

    input_vector = model.encode(input_phrase)
    print('Mauer')
    print(df)
    for index, row in df.iterrows():
        chunks = row["content"]
        print(chunks)
        embeddings = model.encode(chunks, normalize_embeddings=True)    
        similarities = []
        for i in embeddings:
            similarities.append(cosine_similarity(input_vector, i))
            

        max_similarity_index = similarities.index(max(similarities))  # Find index of max similarity
        most_similar_line = chunks[max_similarity_index]  # Get the corresponding line
        print(index, row)
        print("Most similar line:", most_similar_line)
        print("Cosine similarity:", max(similarities))

        top_n = 3  
        top_indices = heapq.nlargest(top_n, range(len(similarities)), key=similarities.__getitem__)
        print(top_indices)
        df.at[index, "matches"] = top_indices
    return df


def processing(query, songs):
    df_songs = pd.DataFrame(songs)
    df_songs["content"] = df_songs["content"].apply(chunking)   
    output = find_matches(df_songs, query).to_dict(orient='records')
    return output


