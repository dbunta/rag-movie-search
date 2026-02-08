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
            ii = InvertedIndex()
            ii.load()
            search_results = search_movie_data(args.query, ii.index, ii.docmap)
            # search_results = search_movie_data(args.query, documents["movies"])
            print_movie_data(search_results)
        case "build":
            print(f"Buliding inverted index for {DATA_PATH}")
            ii = InvertedIndex()
            ii.build()
            ii.save()
            # docs = ii.get_documents("merida")
            # print(f"First document for term 'merida' = {docs[0]}")
        case "test":
            ii = InvertedIndex()
            ii.load()
            # test = ii.get_documents("merida")
            # print(ii.index)
            # print('merida' in ii.index)
            # if 'merida' in ii.index:
            #     print(sorted(ii.index['merida']))
            # print(ii.index)
            print(ii.index["brave"])
            # for t in ii.index:
            #     print(t)
            pass
        case _:
            parser.print_help()

def test() -> None:
    pass

def print_movie_data(items:list):
    sorted_movies = sorted(items, key=lambda x: x["id"])
    # for d in sorted_movies[:5]:
    for d in sorted_movies:
        print(f"{d["id"]}: {d["title"]}")


if __name__ == "__main__":
    main()


