# Movie Vault CLI Tool 🎬

A command-line interface (CLI) utility to **search**, **add**, **list**, **remove**, and **view details** of movies using the [OMDb API](http://www.omdbapi.com/).  
Built for those who like their movie data fast, simple, and right at their fingertips.

---

## Features

- Search movies by title  
- Get detailed info about a specific movie by title and year  
- Add movies to your personal vault (saved locally)  
- List all movies in your vault with details  
- Remove movies from your vault by title  

---

## Prerequisites

- Python 3.7+  
- Internet connection (for API requests)  
- OMDb API key (free API key from [OMDb](http://www.omdbapi.com/apikey.aspx))  
- `requests` and `python-dotenv` packages

---

## Setup & Installation

1. Clone or download this repository.

2. Create a `.env` file in the project root with your OMDb API key:

   ```env
   API_KEY=your_omdb_api_key_here
    ```
3. Install dependencies:
     ```bash
    pip install -r requirement.txt
    ```
---

## Usage

Run the script with one of the following commands:

### Search movies by title

```bash
python movie_vault.py search --title "Inception"
```
Lists movies matching the title.

### View details of a movie by title and year

```bash
python movie_vault.py details --title "Inception" --year 2010
```
Displays detailed information about the movie.

### Add a movie to your vault

```bash
python movie_vault.py add --title "Inception" --year 2010
```
Adds the movie to your local collection.

### List all saved movies

```bash
python movie_vault.py list
```
Shows detailed info on all saved movies.

### Remove a movie from your vault by title

```bash
python movie_vault.py remove --title "Inception"
```
Removes the movie(s) matching the title from your collection.
---

## Data Persistence

- Saved movies are stored locally in a binary file called `movies.bin`.
- Movie data is retrieved live from the OMDb API when listing or getting details.

---

## Notes & Tips

- Year must match exactly when adding or viewing details.
- Removing by title removes all matching movies, so be cautious.
- API rate limits apply as per OMDb policy.
- This tool works best with a reliable API key and stable internet.

---

## License

This project is licensed under the MIT License — feel free to use, tweak, or improve it.

---