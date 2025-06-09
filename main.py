import os
import requests
import argparse
from dotenv import load_dotenv
import pickle

load_dotenv()
api_key = os.getenv("API_KEY")
url = "http://www.omdbapi.com/"
FILE = "movies.bin" 

def load_movies():
    try:
        with open(FILE, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

def save_movies(ids):
    with open(FILE, 'wb') as file:
        pickle.dump(ids, file)

def details_title(title):
    params = {'s': title, 'apikey': api_key}
    response = requests.get(url, params=params)
    return response.json()
    
def details_id(imdb_id):
    params = {'i': imdb_id, 'apikey': api_key}
    response = requests.get(url, params=params)
    return response.json()

def search_movies(title):
    response = details_title(title)
    if response.get('Response') == 'False':
        print(f"No results found for '{title}'")
        return 

    for i, result in enumerate(response["Search"], start=1):
        print(f"{i}.\tTitle: {result['Title']} \n\tYear: {result['Year']}")
    return 


def get_movie_details(imdb_id):
    response = details_id(imdb_id)
    if response.get('Response') == 'False':
        print(f"Could not fetch details for ID {imdb_id}")
        return

    print("\n🎬 Movie Details:\n")
    print(f"Title       : {response.get('Title', 'N/A')}")
    print(f"Year        : {response.get('Year', 'N/A')}")
    print(f"Director    : {response.get('Director', 'N/A')}")
    print(f"IMDb Rating : {response.get('imdbRating', 'N/A')}")
    print(f"Genre       : {response.get('Genre', 'N/A')}")
    print(f"Plot        : {response.get('Plot', 'N/A')}\n")


def get_movie(title, year):
    response = details_title(title)
    if response.get('Response') == 'False':
        print("No results found")
        return

    for result in response['Search']:
        if result['Year'] == year:
            get_movie_details(result['imdbID'])
            return


def add_movie(title, year):
    response = details_title(title)
    if response.get('Response') == 'False':
        print("No results found for that title")
        return

    saved_ids = load_movies()
    for result in response['Search']:
        if result['Year'] == year:
            if result['imdbID'] in saved_ids:
                print("Movie already exists in your collection")
            else:
                saved_ids.append(result['imdbID'])
                save_movies(saved_ids)
                print("Added successfully")
            return
    print("No movie found matching that exact year")

def remove_movie(title):
    response = details_title(title)
    if response.get('Response') == 'False':
        print("No results found for that title")
        return

    saved_ids = load_movies()
    initial_count = len(saved_ids)
    
    # Remove all movies matching the title (there might be multiple)
    removed_ids = [result['imdbID'] for result in response.get('Search', [])]
    saved_ids = [id for id in saved_ids if id not in removed_ids]
    
    if len(saved_ids) < initial_count:
        save_movies(saved_ids)
        print(f"Removed {initial_count - len(saved_ids)} movie(s)")
    else:
        print("No matching movies found in your collection")
   

def list_movies():
    saved_ids = load_movies()
    if not saved_ids:
        print("Your movie collection is empty")
        return

    for i, imdb_id in enumerate(saved_ids, start=1):
        print(f"\nMovie #{i}:")
        get_movie_details(imdb_id)


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
    parser_add.add_argument("--title", required=True, help="Title of movie")
    parser_add.add_argument("--year", required=True, help="Year of release of movie")

    # 'list' command
    sub_parser.add_parser("list", help="List all saved movies")

    # 'remove' command
    parser_remove = sub_parser.add_parser("remove", help="Remove a saved movie")
    parser_remove.add_argument("--title", required=True, help="Title of movie to remove")

    args = parser.parse_args()

    match(args.command):
        case "search":
            search_movies(args.title)
        case "details":
            get_movie(args.title, args.year)
        case "add":
            add_movie(args.title, args.year)
        case "list":
            list_movies()
        case "remove":
            remove_movie(args.title)

if __name__ == "__main__":
    main()