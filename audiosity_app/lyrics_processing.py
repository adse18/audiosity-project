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
    stripped = re.sub(r'.*\d+ Contributor',"", stripped)
    # remove song structure comments
    stripped = re.sub(r'\[.*?\]', '', stripped)
    # split song texts into lines by splitting at newline characters
    stripped = stripped.splitlines()
    # removing empty entries
    stripped = [line for line in stripped if line.strip()]
    # remove end of song artifacts
    stripped[0] = re.sub(r'.*?Lyrics', "", stripped[0])
    stripped[-1] = re.sub(r'You might also likeEmbed$', "", stripped[-1])
    stripped[-1] = re.sub(r'\d+Embed$', "", stripped[-1])
    stripped[-1] = re.sub(r'Embed', "", stripped[-1])

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
    print('Processing DataFrame for matches...')
    
    # Iterate over DataFrame rows
    for index, row in df.iterrows():
        chunks = row["content"]
        print("Processing row:", index)
        print("Chunks:", chunks)
        
        # Encode chunks and compute similarities
        embeddings = model.encode(chunks, normalize_embeddings=True)
        similarities = [cosine_similarity(input_vector, emb) for emb in embeddings]
        
        # Check if similarities list is non-empty
        if not similarities:
            continue
        
        # Find top N matches
        top_n = 3
        top_indices = heapq.nlargest(top_n, range(len(similarities)), key=similarities.__getitem__)
        
        # Ensure the 'matches' column exists
        if 'matches' not in df.columns:
            df['matches'] = pd.Series(index=df.index, dtype='object')
        
        # Assign top_indices to the 'matches' column
        df.at[index, "matches"] = top_indices
    
    return df

def lyrics_processing(query, songs):
    df_songs = pd.DataFrame(songs)
    df_songs["content"] = df_songs["content"].apply(chunking)   
    output = find_matches(df_songs, query).to_dict(orient='records')
    return output
