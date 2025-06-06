import requests
import os
from dotenv import load_dotenv


load_dotenv()

class MovieAPI:
    BASE_URL = "http://www.omdbapi.com/"

    def __init__(self, api_key):
        self.api_key = api_key

    def search_movies(self, title):
        params = {"s": title, "apikey": self.api_key}
        resp = requests.get(self.BASE_URL, params=params)
        data = resp.json()
        if data.get("Response") == "False":
            return []
        return data.get("Search", [])

    def get_movie_details(self, imdb_id):
        params = {"i": imdb_id, "apikey": self.api_key}
        resp = requests.get(self.BASE_URL, params=params)
        return resp.json()

class MovieVault:
    def __init__(self):
        self.movies = []

    def add_movie(self, movie):
        # Avoid duplicates by imdbID
        if any(m['imdbID'] == movie['imdbID'] for m in self.movies):
            print("⚠️ Movie already in vault.")
            return False
        self.movies.append(movie)
        return True

    def list_movies(self):
        return self.movies

class MovieApp:
    def __init__(self):
        api_key = os.getenv("OMDB_API_KEY")
        if not api_key:
            raise EnvironmentError("❌ OMDB_API_KEY not set in .env file.")
        self.api = MovieAPI(api_key)
        self.vault = MovieVault()

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    def run(self):
        while True:
            self.clear()
            print("🎬 MovieVault – Object-Oriented Edition\n")
            print("1. Search movies")
            print("2. Add verified movie")
            print("3. View vault")
            print("4. Exit")
            choice = input("\nChoose option (1-4): ").strip()

            match choice:
                case "1":
                    self.search_movies_flow()
                case "2":
                    self.add_movie_flow()
                case "3":
                    self.view_vault()
                case "4":
                    self.clear()
                    print("👋 Goodbye!")
                    break
                case _:
                    print("❌ Invalid choice. Try again.")
                    input("Press Enter to continue...")

    def search_movies_flow(self):
        self.clear()
        title = input("Enter movie title to search: ").strip()
        results = self.api.search_movies(title)
        if not results:
            print("❌ No results found.")
            input("Press Enter to return to menu...")
            return

        for idx, m in enumerate(results, 1):
            print(f"{idx}. {m['Title']} ({m['Year']}) [{m['Type'].capitalize()}]")

        try:
            choice = int(input("\nEnter number to see details: "))
            if not (1 <= choice <= len(results)):
                print("❌ Invalid number.")
                input("Press Enter to continue...")
                return
        except ValueError:
            print("❌ Must enter a number.")
            input("Press Enter to continue...")
            return

        selected = results[choice - 1]
        details = self.api.get_movie_details(selected["imdbID"])
        self.clear()
        self.print_movie_details(details)
        input("\nPress Enter to return to menu...")

    def add_movie_flow(self):
        self.clear()
        title = input("Enter movie title to add: ").strip()
        director_input = input("Enter director's name for verification: ").strip().lower()

        results = self.api.search_movies(title)
        if not results:
            print("❌ No results found.")
            input("Press Enter to return to menu...")
            return

        print("\nMatches found:")
        for idx, m in enumerate(results, 1):
            print(f"{idx}. {m['Title']} ({m['Year']}) [{m['Type'].capitalize()}]")

        try:
            choice = int(input("Select correct movie (number): "))
            if not (1 <= choice <= len(results)):
                print("❌ Invalid selection.")
                input("Press Enter to continue...")
                return
        except ValueError:
            print("❌ Enter a number.")
            input("Press Enter to continue...")
            return

        selected = results[choice - 1]
        details = self.api.get_movie_details(selected["imdbID"])

        director_api = details.get("Director", "").lower()
        if director_input in director_api:
            added = self.vault.add_movie(details)
            if added:
                print("✅ Movie added to vault!")
            else:
                print("⚠️ Movie already in vault.")
        else:
            print(f"❌ Director mismatch.\nIMDb Director: {details.get('Director')}")
        input("Press Enter to return to menu...")

    def view_vault(self):
        self.clear()
        movies = self.vault.list_movies()
        if not movies:
            print("📭 Vault is empty.")
            input("Press Enter to return to menu...")
            return
        for idx, m in enumerate(movies, 1):
            print(f"{idx}. {m['Title']} ({m['Year']}) - Directed by {m['Director']} [IMDb Rating: {m.get('imdbRating', 'N/A')}]")
        input("\nPress Enter to return to menu...")

    @staticmethod
    def print_movie_details(details):
        print("🎞️ Movie Details\n" + "-"*50)
        print(f"Title     : {details.get('Title')}")
        print(f"Year      : {details.get('Year')}")
        print(f"Director  : {details.get('Director')}")
        print(f"Genre     : {details.get('Genre')}")
        print(f"Cast      : {details.get('Actors')}")
        print(f"Plot      : {details.get('Plot')}")
        print(f"IMDb Rate : {details.get('imdbRating')}")
        print(f"Runtime   : {details.get('Runtime')}")
        print(f"Language  : {details.get('Language')}")
        print(f"Country   : {details.get('Country')}")
        print("-"*50)


if __name__ == "__main__":
    app = MovieApp()
    app.run()
