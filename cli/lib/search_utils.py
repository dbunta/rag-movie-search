import json
import os
import string

from nltk.stem import PorterStemmer

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, "data", "stopwords.txt")
CACHE_DIR = os.path.join(PROJECT_ROOT, "cache")
INDEX_PATH = os.path.join(CACHE_DIR, "index.pkl")
DOCMAP_PATH = os.path.join(CACHE_DIR, "docmap.pkl")

def search_movie_data(search_term:str, movies:list):
    stopwords = load_text_from_file(DATA_PATH)
    search_tokens = tokenize_text(search_term, stopwords)
    results = []
    for m in movies:
        movie_tokens = tokenize_text(m['title'], stopwords)
        for st in search_tokens:
            if any(st in mt for mt in movie_tokens):
                results.append(m)
                break
    return results

def tokenize_text(text:str, stopwords:list) -> set:
    # preprocess text
    text = text.lower()
    punctuation_trans = text.maketrans(dict.fromkeys(string.punctuation, ''))
    text = text.translate(punctuation_trans)

    # tokenize
    words = text.split()
    tokens = [word for word in words if word not in stopwords] 
    ps = PorterStemmer()
    tokens = [ps.stem(token) for token in tokens]

    return tokens


def load_json_from_file(path:str) -> dict:
    with open(path, "r") as file:
        file_contents = json.load(file)
        # retval = movies_json["movies"]
    return file_contents

def load_text_from_file(path:str) -> dict:
    with open(path, "r") as file:
        file_contents = file.read().splitlines()
    return file_contents