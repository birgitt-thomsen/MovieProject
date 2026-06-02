"""
Script checks if movie is found in the omdb api that matches the user
input title.
"""
import requests

from utils.utilities import color_text


def search_movies(title):
    """Checks if a single movie is found that matches the user input title."""
    try:
        url = "http://www.omdbapi.com/?apikey=9766f1e0&t=" + title
        response = requests.get(url, timeout=5)
        data = response.json()

        response.raise_for_status()

        data = response.json()

        if data.get("Response") == "False":
            return None

        return (
            data["Title"],
            data["Year"],
            data["imdbRating"],
            data["Poster"],
            data["imdbID"]
        )

    except requests.exceptions.ConnectionError:
        print(color_text("Connection failed", "ERROR"))
    except requests.exceptions.Timeout:
        print(color_text("Request timed out", "WARN"))
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == 404:
            print(color_text("Not found — check the endpoint URL", "ERROR"))
        elif status_code >= 500:
            print(color_text("Server error — try again later", "WARN"))
        else:
            print(f"HTTP Error {status_code}")
    except requests.exceptions.RequestException as e:
        print(color_text(f"Unexpected error: {e}", "ERROR"))

    return None
