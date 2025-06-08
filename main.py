import os
import requests
import argparse
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("API_KEY")
url = "http://www.omdbapi.com/"
FILE = "movies.bin"
imdb_ids = []

def load_movies():
    try:
        with open(FILE) as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        with open(FILE, 'w') as file:
            return []

def search_movies(title):
    params = {'s': title, 'apikey': api_key}
    response = requests.get(url, params=params).json()

    if response.get("Response") == "True":
        for i, result in enumerate(response["Search"], start=1):
            print(f"{i}.\tTitle: {result['Title']} \n\tYear: {result['Year']}")
            imdb_ids.append(result["imdbID"])
    else:
        print(f"No results found for '{title}'")

def get_movie_details(imdb_id):
    params = {'i': imdb_id, 'apikey': api_key}
    response = requests.get(url, params=params).json()

    if response.get("Response") == "True":
        print("\n🎬 Movie Details:\n")
        print(f"Title       : {response.get('Title', 'N/A')}")
        print(f"Year        : {response.get('Year', 'N/A')}")
        print(f"Director    : {response.get('Director', 'N/A')}")
        print(f"IMDb Rating : {response.get('imdbRating', 'N/A')}")
        print(f"Genre       : {response.get('Genre', 'N/A')}")
        print(f"Plot        : {response.get('Plot', 'N/A')}\n")
    else:
        print(f"Could not fetch details for ID {imdb_id}")

def get_movie(title, year):
    params = {'s': title, 'apikey': api_key}
    response = requests.get(url, params=params).json()

    if response.get("Response") == "True":
        for result in response['Search']:
            if (result['Year'] == year):
                get_movie_details(result['imdbID'])



def main():
    parser = argparse.ArgumentParser(
        description="🎥 CLI tool to search and fetch movie data from IMDb (via OMDb API)"
    )
    sub_parser = parser.add_subparsers(dest="command", required=True)

    # 'search' command
    parser_search = sub_parser.add_parser("search", help="Search for movies by title")
    parser_search.add_argument("--title", required=True, help="Movie title to search")
 
    # 'details' command
    parser_details = sub_parser.add_parser("details", help="view details of movie")
    parser_details.add_argument("--title", required=True, help="Title of movie")
    parser_details.add_argument("--year", required=True, help="Year of release of movie")

    # 'add' command
    parser_add = sub_parser.add_parser("add", help="Add movie to vault")
    parser_add.add_argument("--title", required=True)
    parser_add.add_argument("--director", required=True)

    # 'list' command
    parser_list = sub_parser.add_parser("list", help="List all saved movies")

    # 'view' command
    parser_view = sub_parser.add_parser("view", help="View info of saved movie")
    parser_view.add_argument("--title", required=True)

    # 'remove' command
    parser_remove = sub_parser.add_parser("remove", help="Remove a saved movie")
    parser_remove.add_argument("--title", required=True)

    args = parser.parse_args()
    imdb_ids = load_movies()

    if args.command == "search":
        search_movies(args.title)

    elif args.command == "details":
        get_movie(args.title, args.year)


if __name__ == "__main__":
    main()
