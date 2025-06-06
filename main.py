import os
import requests
import argparse
from dotenv import load_dotenv



def main():

    load_dotenv()
    api_key = os.getenv("API_KEY")
    
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
    




if __name__ =="__main__":
    main()