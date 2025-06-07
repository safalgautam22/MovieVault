import os
import requests
import argparse
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


def movie_search(title):
    url = "http://www.omdbapi.com/"
    params = { 's':title, 'apikey': api_key }
    response = requests.get(url, params=params)
    response = response.json()
    imdb_ids = []
    for respond in response["Search"]:
        print(f"Title: {respond['Title']} Year: {respond['Year']}")
        imdb_ids.append(respond['imdbID'])
    print(imdb_ids)
    #  print(json.dumps(response, indent=4))

def main():

    
    
    parser = argparse.ArgumentParser(description = "It is a CLI based programme to fetch movie data from IMDB data base and store them in vault")

    sub_parser = parser.add_subparsers(dest="command", required=True)

    # 'search' command
    parser_search = sub_parser.add_parser("search", help="search data in database")
    parser_search.add_argument("--title", required=True, help="Title of movie")

    # 'add' command
    parser_add = sub_parser.add_parser("add", help="Add movie to vault")
    parser_add.add_argument("--title", required=True, help="Title of movie")
    parser_add.add_argument("--director", required=True, help="Director's name")

    # 'list' command
    parser_list = sub_parser.add_parser("list", help="List all saved movies")

    # 'view' command
    parser_view = sub_parser.add_parser("view", help="View info of saved movie")
    parser_view.add_argument("--title", required=True, help="Title of movie")

    # 'remove' command
    parser_remove = sub_parser.add_parser("remove", help="Remove a saved movie")
    parser_remove.add_argument("--title", required=True, help="Title of movie")

    args = parser.parse_args()

    if args.command == 'search':
            movie_search(args.title)
    




if __name__ =="__main__":
    main()