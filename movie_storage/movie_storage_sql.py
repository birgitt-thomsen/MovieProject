"""
Script handles all actions made to the movie database.
"""

from sqlalchemy import create_engine, text
from MovieProject.api import omdb_api as api_data
from utils.utilities import color_text

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL)#, echo=True)

# Create the movies table if it does not exist
with engine.begin() as connection:
    connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT UNIQUE NOT NULL,
            user_rating REAL DEFAULT " - ",
            user_note TEXT DEFAULT "No thoughts yet...",
            imdbID TEXT UNIQUE NOT NULL
            )
            """))


def list_movies():
    """Retrieve all movies from the database."""
    with engine.begin() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}


def add_movie(title):
    """Add a new movie to the database."""
    with engine.begin() as connection:
        try:
            movie_data = api_data.search_movies(title)

            if movie_data is None:
                print(color_text(
                    f"No movie found matching '{title}'.",
                    "ERROR"
                ))
                return

            title_api, year_api, rating_api, poster_api, imdbID_api = movie_data

            connection.execute(
                text("""
                     INSERT INTO movies
                         (title, "year", rating, poster_url, imdbID)
                     VALUES (:title, :year, :rating, :poster, :imdbID)
                     """),
                {
                    "title": title_api,
                    "year": year_api,
                    "rating": rating_api,
                    "poster": poster_api,
                    "imdbID": imdbID_api
                }
            )
            print(color_text(f"Success! '{title}' was added.", "SUCCESS"))
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :title"),
                               {"title": title})
            connection.commit()
            print(color_text(f"Success! '{title}' was removed.","SUCCESS"))
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating, note):
    """Update a movie by adding a note and personal rating."""
    with engine.begin() as connection:
        try:
            connection.execute(text("UPDATE movies "
                                    "SET user_rating = :rating, "
                                    "user_note = :note "
                                    "WHERE title = :title"),
                               {
                                   "rating": rating,
                                   "note": note,
                                   "title": title
                               })
            print(color_text(f"Success! '{title}' updated successfully.",
                             "SUCCESS"))
        except Exception as e:
            print(f"Error: {e}")


def get_html_movie_data():
    """Retrieves movie data from the database for HTML output."""
    with engine.begin() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster_url, user_rating, "
                 "user_note, imdbID FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating":row[2], "poster_url": row[3],
                     "user_rating": row[4], "user_note": row[5],
                     "imdbID": row[6]} for row in movies}
