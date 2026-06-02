"""
Handles movie_storage related queries for listing, adding,
deleting and saving movies in the main file.
"""

import json


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.
    """
    with open("data.json", "r", encoding="utf-8") as fileobj:
        movies = json.loads(fileobj.read())

    # movies = []
    # for movie in movie_data:
    #     movies.append(movie)

    return movies


def save_movies(movies):
    """
    Gets all movies as an argument and saves them to the data.json file.
    """
    json_str = json.dumps(movies)
    with open("data.json", "w", encoding="utf-8") as fileobj:
        fileobj.write(json_str)


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the data.json file, adds the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movie_add = {title: {"year": year, "rating": rating}}
    movies.update(movie_add)
    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the data.json file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    del movies[title]
    save_movies(movies)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the data.json file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title]["rating"] = rating
    save_movies(movies)
