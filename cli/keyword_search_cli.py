import argparse
from lib.search_utils import *
from lib.keyword_search import *


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="")

    test_parser = subparsers.add_parser("test", help="")

    args = parser.parse_args()

    documents = load_json_from_file("./data/movies.json") 


    match args.command:
        case "search":
            # print the search query here
            print(f"Searching for: {args.query}")
            search_results = search_movie_data(args.query, documents["movies"])
            print_movie_data(search_results)
        case "build":
            print(f"Buliding inverted index for {DATA_PATH}")
            ii = InvertedIndex()
            ii.build()
            ii.save()
            docs = ii.get_documents("merida")
            print(f"First document for term 'merida' = {docs[0]}")
        case "test":
            ii = InvertedIndex()
            ii.load()
            # test = ii.get_documents("merida")
            print('merida' in ii.index)
            if 'merida' in ii.index:
                print(sorted(ii.index['merida']))
            # print(ii.index)
            # for t in ii.index:
            #     print(t)
            pass
        case _:
            parser.print_help()

def test() -> None:
    pass
    # print(stopwords)
    # title = "Faster, Pussycat! Kill! Kill!"
    # preprocessed = preprocess_text(title)
    # print(preprocessed)
    # tokens = tokenize_text(preprocessed)
    # print(tokens)

# def preprocess_text(text:str) -> str:
#     text = text.lower()
#     punctuation_trans = text.maketrans(dict.fromkeys(string.punctuation, ''))
#     text = text.translate(punctuation_trans)
#     return text

# def tokenize_text(text:str, stopwords:list) -> set:
#     words = text.split()
#     tokens = [word for word in words if word not in stopwords] 
#     ps = PorterStemmer()
#     tokens = [ps.stem(token) for token in tokens]
#     return tokens

# def load_json_from_file(path:str) -> dict:
#     with open(path, "r") as file:
#         file_contents = json.load(file)
#         # retval = movies_json["movies"]
#     return file_contents

# def load_text_from_file(path:str) -> dict:
#     with open(path, "r") as file:
#         file_contents = file.read().splitlines()
#     return file_contents

# def search_movie_data(search_term:str, movies:list):
#     stopwords = load_text_from_file("./data/stopwords.txt")
#     search_tokens = tokenize_text(preprocess_text(search_term), stopwords)
#     results = []
#     for m in movies:
#         movie_tokens = tokenize_text(preprocess_text(m['title']), stopwords)
#         for st in search_tokens:
#             if any(st in mt for mt in movie_tokens):
#                 results.append(m)
#                 break
#     return results


def print_movie_data(items:list):
    sorted_movies = sorted(items, key=lambda x: x["id"])
    for i,d in enumerate(sorted_movies[:5]):
        print(f"{i+1}. {d["title"]}")


if __name__ == "__main__":
    main()
