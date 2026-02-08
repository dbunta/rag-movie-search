import pickle
from lib.search_utils import tokenize_text, load_json_from_file, load_text_from_file, DATA_PATH, CACHE_DIR, INDEX_PATH, DOCMAP_PATH, STOPWORDS_PATH
import os

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}
        self.stopwords = load_text_from_file(STOPWORDS_PATH)

    def __add_document(self, doc_id:int, text:str):
        tokens = tokenize_text(text, self.stopwords)
        for token in tokens:
            if token in self.index:
                if doc_id not in self.index[token]:
                    self.index[token].append(doc_id)
            else:
                self.index[token] = [doc_id]

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
    
    def load(self):
        if not os.path.exists(INDEX_PATH):
            raise(f"File does not exist: {INDEX_PATH}")
        if not os.path.exists(DOCMAP_PATH):
            raise(f"File does not exist: {DOCMAP_PATH}")

        with open(INDEX_PATH, 'rb') as f1:
            self.index = pickle.load(f1)
        with open(DOCMAP_PATH, 'rb') as f2:
            self.docmap = pickle.load(f2)
