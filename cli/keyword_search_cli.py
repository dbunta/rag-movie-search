import argparse
from lib.search_utils import *
from lib.keyword_search import *


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    subparsers.add_parser("build", help="")

    term_frequency_parser = subparsers.add_parser("tf", help="")
    term_frequency_parser.add_argument("document_id", type=int)
    term_frequency_parser.add_argument("term", type=str)

    idf_parser = subparsers.add_parser("idf", help="inverse document frequency")
    idf_parser.add_argument("term", type=str)

    test_parser = subparsers.add_parser("test", help="")

    args = parser.parse_args()

    documents = load_json_from_file("./data/movies.json") 


    match args.command:
        case "search":
            # print the search query here
            print(f"Searching for: {args.query}")
            ii = InvertedIndex()
            ii.load()
            search_results = search_movie_data(args.query, ii.index, ii.docmap, 5)
            print_movie_data(search_results)
        case "build":
            print(f"Buliding inverted index for {DATA_PATH}")
            ii = InvertedIndex()
            ii.build()
            ii.save()
        case "tf":
            ii = InvertedIndex()
            ii.load()
            count = ii.get_tf(args.document_id, args.term)
            print(count)
        case "idf":
            ii = InvertedIndex()
            ii.load()
            idf = ii.get_idf(args.term)
            print(f"Inverse document frequency of '{args.term}': {idf:.2f}")
        case "test":
            ii = InvertedIndex()
            ii.load()
            print(ii.index["brave"])
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


