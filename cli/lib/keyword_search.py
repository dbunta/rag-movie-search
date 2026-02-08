import math
import pickle
from typing import Counter
from lib.search_utils import *
import os

class InvertedIndex:
    def __init__(self):
        self.index: dict[str, dict] = {}
        self.docmap: dict[int, dict] = {}
        # term_frequencies is a dictionary with document id as key, and a counter object as value
        # the counter object is like a dictionary with term as key and count of term within doucment as value
        self.term_frequencies: dict[int, Counter] = {} 
        self.stopwords = load_text_from_file(STOPWORDS_PATH)

    def __add_document(self, doc_id:int, text:str):
        tokens = tokenize_text(text, self.stopwords)
        self.term_frequencies[doc_id] = Counter(tokens)
        for token in tokens:
            if token in self.index:
                if doc_id not in self.index[token]:
                    self.index[token].append(doc_id)
            else:
                self.index[token] = [doc_id]

    def get_tf(self, doc_id:int, term:str) -> int:
        tokens = tokenize_text(term, self.stopwords)
        if len(tokens) > 1:
            raise "Unexpected number of tokens"
        counter = self.term_frequencies[doc_id]
        if tokens[0] not in counter:
            return 0
        return counter[tokens[0]]

    def get_idf(self, term:str):
        tokens = tokenize_text(term, self.stopwords)
        if len(tokens) > 1:
            raise "Unexpected number of tokens"
        total_doc_count = len(self.docmap)
        term_match_doc_count = len(self.index[tokens[0]])
        return math.log((total_doc_count + 1) / (term_match_doc_count + 1))

    def get_tfidf(self, doc_id:int, term:str):
        return self.get_tf(doc_id, term) * self.get_idf(term)

    def get_bm25_idf(self, term:str) -> float:
        # log((N - df + 0.5) / (df + 0.5) + 1)
        # N = total number of documents 
        # df = document frequency
        tokens = tokenize_text(term, self.stopwords)
        if len(tokens) > 1:
            raise "Unexpected number of tokens"
        N = len(self.docmap)
        df = len(self.index[tokens[0]])
        return math.log((N - df + 0.5) / (df + 0.5) + 1)

    def get_documents(self, term:str):
        term = term.lower()
        if term in self.index:
            return sorted(self.index[term])
        return []

    def build(self):
        documents = load_json_from_file(DATA_PATH)["movies"]
        total = len(documents)

        for i,doc in enumerate(documents, 1):
            print(f"Indexing {i} of {total}", end="\r")
            self.__add_document(doc["id"], f"{doc["title"]} {doc["description"]}")
            self.docmap[doc["id"]] = doc
        print()

    def save(self):
        if not os.path.exists(CACHE_DIR):
            os.mkdir(CACHE_DIR)
        
        with open(INDEX_PATH, 'wb') as f1:
            pickle.dump(self.index, f1)
        with open(DOCMAP_PATH, 'wb') as f2:
            pickle.dump(self.docmap, f2)
        with open(TERM_FREQUENCIES_PATH, 'wb') as f3:
            pickle.dump(self.term_frequencies, f3)
    
    def load(self):
        if not os.path.exists(INDEX_PATH):
            raise(f"File does not exist: {INDEX_PATH}")
        if not os.path.exists(DOCMAP_PATH):
            raise(f"File does not exist: {DOCMAP_PATH}")
        if not os.path.exists(TERM_FREQUENCIES_PATH):
            raise(f"File does not exist: {TERM_FREQUENCIES_PATH}")

        with open(INDEX_PATH, 'rb') as f1:
            self.index = pickle.load(f1)
        with open(DOCMAP_PATH, 'rb') as f2:
            self.docmap = pickle.load(f2)
        with open(TERM_FREQUENCIES_PATH, 'rb') as f3:
            self.term_frequencies = pickle.load(f3)
