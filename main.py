"""
Main script to handle database commands from the user to edit, sort
and analyze movie data.
"""

import random as rand  # Used for random movie selection.

import matplotlib.pyplot as plt  # Used to create histogram.
from rapidfuzz import fuzz  # Used to allow fuzzy search.

from movie_storage import movie_storage_sql as storage
from web import html_generator as generator
from utils.utilities import color_text, format_text

RATIO_VALUE = 50


def main():
    """
    Handles the command dictionary and function assignment. Uses main loop
    to ensure a continuous flow for the user until the exit command.
    """

    print("********** My Ultimate Movie Database **********")

    action_dict = {
        0: print_exit_message,
        1: command_list_movies, #updated
        2: command_add_movie,
        3: command_delete_movie,
        4: command_update_movie,
        5: combine_movie_stats,
        6: get_random_movie,
        7: combine_search_results,
        8: get_sorted_by_rating_movie_list,
        9: get_sorted_by_year_movie_list,
        10: get_filtered_movies,
        11: create_histogram,
        12: generate_website,
    }

    while True:
        display_movies_menu()
        try:
            # Ensures valid int commands with appropriate error to guide user
            user_selection = int(input(format_text("Enter choice (0-12): ",
                                                  "INPUT")))
            if not 0 <= user_selection <= 12:
                raise ValueError(
                    color_text("Invalid choice, please enter a number "
                               "between 0 and 12.", "ERROR")
                )
            # Program exit to break loop
            if user_selection == 0:
                print_exit_message()
                break

            result = action_dict[user_selection]()
            handle_output(result)

            # User command to trigger menu again
            input(color_text("\nPress enter to continue ", "MENU"))

        except ValueError:
            print(
                color_text("Invalid choice, please enter a number between 0 "
                           "and 11.","ERROR"))


def display_movies_menu():
    """Displays the menu of actions available to the user."""
    print(format_text("\nMenu:","INPUT"))
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Sort movies by rating")
    print("9. Sort movies by year")
    print("10. Filter movies")
    print("11. Create rating histogram")
    print("12. Generate website\n")


def handle_output(result):
    """
    Defines how to handle various function outputs based
    on data type.
    """
    if isinstance(result, (list, tuple, set)):
        for item in result:
            print(item)
    elif isinstance(result, (str, int, float, bool)):
        print(result)


def print_exit_message():
    """Prints an exit message for when the user exits the program."""
    print("Bye!")


def command_list_movies():
    """
    Returns number of movies and lists all movies with their
    release year and rating from database.
    """
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


def check_input_not_empty(prompt):
    """
    Checks that user input is not empty. Loop until a non-empty
    value is entered.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(color_text("Input cannot be empty.", "ERROR"))


def check_unique_movie_title(prompt):
    """
    Checks that movie title input is not empty and does not already
    exist. Returns input or message that title already exists.
    """
    titles = set(storage.list_movies())
    title_input = check_input_not_empty(prompt)
    if title_input in titles:
        print(color_text(f"Sorry! '{title_input}' already exists.", "ERROR"))
    else:
        return title_input


def check_duplicate_movie_title(prompt):
    """
    Checks that movie title input is not empty and already exists.
    Returns input or message that title does not exist.
    """
    titles = set(storage.list_movies())
    title_input = check_input_not_empty(prompt)
    if title_input not in titles:
        print(color_text(f"Sorry! '{title_input}' does not exist.", "ERROR"))
    else:
        return title_input


def get_valid_year(prompt):
    """
    Gets year input and validates that it consists of four digits.
    Loops until a valid year is entered.
    """
    while True:
        year_input = check_input_not_empty(prompt)
        if year_input.isdigit() and len(year_input) == 4:
            return int(year_input)
        print(color_text("Please enter a valid year.", "ERROR"))


def get_valid_rating(prompt):
    """
    Gets rating input and validates that it is a float value between 0
    and 10. Loops until a valid rating is entered.
    """
    while True:
        rating_input = check_input_not_empty(prompt)
        try:
            if 0 <= float(rating_input) <= 10:
                return float(rating_input)
            raise ValueError(color_text("Please enter a valid rating.",
                                        "ERROR"))
        except ValueError:
            print(color_text("Please enter a valid rating.", "ERROR"))


def command_add_movie():
    """
    Takes valid movie title, year and rating from the user and
    adds the movie data to the database.
    """
    add_name_input = check_unique_movie_title(
        format_text("\nEnter new movie name: ", "INPUT"))

    if add_name_input is not None:
        storage.add_movie(add_name_input)


def command_delete_movie():
    """
    Takes valid movie title from the user and deletes it from the database.
    """
    delete_name_input = check_duplicate_movie_title(
        format_text("\nEnter movie name to delete: ", "INPUT"))

    if delete_name_input is not None:
        storage.delete_movie(delete_name_input)


def command_update_movie():
    """
    Takes valid movie name and rating from the user, and
    replaces the existing rating with the new one.
    """
    update_name_input = check_duplicate_movie_title(
        format_text("\nEnter movie name to update: ", "INPUT"))

    if update_name_input is not None:
        personal_rating_input = get_valid_rating(
            format_text("Enter your personal movie rating (0-10): ",
                      "INPUT"))
        personal_note_input = input(
            format_text("Enter a personal movie comment: ",
                      "INPUT"))
        storage.update_movie(update_name_input,
                             personal_rating_input,
                             personal_note_input)


def calculate_average_rating():
    """
    Calculates and returns the average rating of all movies in the
    database.
    """
    movies = storage.list_movies()
    ratings_lst = [movies[movie]["rating"] for movie in movies]
    rating_count = len(ratings_lst)
    running_total = 0
    for rating in ratings_lst:
        running_total += rating
    average_rating = running_total / rating_count
    return round(average_rating, 1)


def calculate_median_rating():
    """
    Calculates and returns the median rating of all movies in
    the database. Separate calculations are applied depending on
    whether there is an even odd number of movies.
    """
    movies = storage.list_movies()
    ratings_lst = list(movies[movie]["rating"] for movie in movies)
    rating_count = len(ratings_lst)
    ratings_lst.sort()

    # If even number of items, average the middle two values.
    if rating_count % 2 == 0:
        median1 = ratings_lst[rating_count // 2]
        median2 = ratings_lst[rating_count // 2 - 1]
        median = (median1 + median2) / 2

    # If odd number of items, find middle value.
    else:
        median = ratings_lst[rating_count // 2]
    return round(median, 1)


def calculate_max_ratings():
    """
    Gets the movies with the highest rating in the database and
    returns a dictionary with the movies and their rating.
    """
    movies = storage.list_movies()
    ratings_lst = list(movies[movie]["rating"] for movie in movies)
    max_rating = max(ratings_lst)
    highest_rated_movies = {}
    for movie in movies:
        if movies[movie]["rating"] == max_rating:
            highest_rated_movies[movie] = movies[movie]["rating"]
    return highest_rated_movies


def calculate_min_ratings():
    """
    Gets the movies with the lowest rating in the database and
    returns a dictionary with the movies and their rating.
    """
    movies = storage.list_movies()
    ratings_lst = list(movies[movie]["rating"] for movie in movies)
    min_rating = min(ratings_lst)
    lowest_rated_movies = {}
    for movie in movies:
        if movies[movie]["rating"] == min_rating:
            lowest_rated_movies[movie] = movies[movie]["rating"]
    return lowest_rated_movies


def combine_movie_stats():
    """
    Collates stats info from the four previous functions
    and returns the results in a list.
    """
    result = []
    average_rating = calculate_average_rating()
    result.append(format_text("\nAverage rating: ", "INPUT")
                  + f"{average_rating}")

    median_rating = calculate_median_rating()
    result.append(format_text("Median rating: ", "INPUT")
                  + f"{median_rating}")

    highest_ratings = calculate_max_ratings()
    result.append(format_text("Best movie(s):", "INPUT"))
    for movie, rating in highest_ratings.items():
        result.append(f"\t• {movie}: {rating}")

    lowest_ratings = calculate_min_ratings()
    result.append(format_text("Worst movie(s):", "INPUT"))
    for movie, rating in lowest_ratings.items():
        result.append(f"\t• {movie}: {rating}")

    return result


def get_random_movie():
    """
    Gets a random movie from the movie database and returns the movie
    with its rating in a list.
    """
    movies = storage.list_movies()
    titles = list(movies)
    random_movie = rand.choice(titles)
    result = ""
    for movie in movies:
        if movie == random_movie:
            result = (
                f"\nYour movie for tonight: {random_movie}, it's rated"
                f" {movies[movie]['rating']}."
            )
    return result


def get_search_result(search_input):
    """
    Takes search input from combine_search_results, looks for
    matches and returns all movies that partially match the search input.
    Returns a dictionary of matching movies and their ratings.
    """
    movies = storage.list_movies()
    partial_matches = {}
    for movie in movies:
        if search_input.lower() in movie.lower():
            partial_matches[movie] = movies[movie]["rating"]
    return partial_matches


def get_fuzzy_search_result(search_input):
    """
    Takes search input from combine_search_results and looks for fuzzy
    matches with a similarity_ratio of at least 50. Returns a
    dictionary of matching movies and their ratings.
    """
    movies = storage.list_movies()
    fuzzy_matches = {}
    for movie in movies:
        similarity_ratio = fuzz.ratio(movie.lower(), search_input.lower())
        if similarity_ratio > RATIO_VALUE:
            fuzzy_matches[movie] = movies[movie]["rating"]
    return fuzzy_matches


def combine_search_results():
    """
    Combines output from partial and fuzzy matching functions into a single
    output. If no partial matches are available, it displays fuzzy matches.
    Returns a list of results and a message when no matches were found.
    """

    search_input = check_input_not_empty(
        format_text("\nEnter part of movie name: ", "INPUT"))
    partial_matches = get_search_result(search_input)
    fuzzy_matches = get_fuzzy_search_result(search_input)

    result = []
    # Get partial matches
    if len(partial_matches) > 0:
        result.append(
            color_text(
                f"Your search for '{search_input}' returned the following "
                f"movie(s):", "SUCCESS"))
        for ext_match, ext_rating in partial_matches.items():
            result.append(color_text(f"{ext_match}: {ext_rating}", "SUCCESS"))

    # Get fuzzy matches
    elif len(fuzzy_matches) > 0:
        result.append(
            color_text(
                f"No movie was found for '{search_input}'. Did you mean:",
                "WARN"))
        for fuzz_match, fuzz_rating in fuzzy_matches.items():
            result.append(color_text(
                f"{fuzz_match}: {fuzz_rating}", "WARN"))

    # If no partial or fuzzy matches, return message without suggestions.
    else:
        result.append(
            color_text(
            f"Sorry! No matching movie was found for '{search_input}'.",
            "ERROR"))
    return result


def get_sorted_by_rating_movie_list():
    """
    Sorts movies by rating in descending order and returns the result
    in a list.
    """
    movies = storage.list_movies()
    movies_sorted = sorted(
        movies.items(), key=lambda item: item[1]["rating"], reverse=True
    )
    result = []
    result.append(
        format_text(f"\n{len(movies_sorted)} movies sorted by rating:",
                   "INPUT"))
    for title, info in movies_sorted:
        result.append(f"{title} ({info['year']}): {info['rating']}")
    return result


def get_sorted_by_year_movie_list():
    """
    Takes input from the user to sort either in ascending or descending
    order, sorts accordingly, and returns the result.
    """
    movies = storage.list_movies()
    while True:
        sort_order_input = input(
            "Do you want the latest movies first? (Y/N) ")
        if sort_order_input.upper() == "Y":
            movies_sorted = sorted(
                movies.items(), key=lambda item: item[1]["year"], reverse=True
            )
            break
        if sort_order_input.upper() == "N":
            movies_sorted = sorted(
                movies.items(), key=lambda item: item[1]["year"])
            break
        print(color_text('Please enter "Y" or "N".', "ERROR"))

    result = []
    result.append(
        format_text(f"\n{len(movies_sorted)} movies sorted by year:",
                   "INPUT"))
    for title, info in movies_sorted:
        result.append(f"{title} ({info['year']}): " f"{info['rating']}")
    return result


def get_min_rating_filter(prompt):
    """
    Takes rating input from user and checks if it is either empty or
    a float value between 0 and 10. Loops until user enters a valid rating.
    """
    while True:
        value = input(prompt).strip()
        if value == "":
            return None
        try:
            if 0 <= float(value) <= 10:
                return float(value)
            raise ValueError(
                color_text("Invalid input. Please enter a valid rating.",
                           "ERROR"))
        except ValueError:
            print(color_text("Invalid input. Please enter a valid rating.",
                           "ERROR"))


def get_valid_year_filter(prompt):
    """
    Gets year input and validates that it is either empty or consists
    of four digits. Loops until a valid year is entered.
    """
    while True:
        value = input(prompt).strip()
        if value == "":
            return None
        try:
            if value.isdigit() and len(value) == 4:
                return int(value)
            raise ValueError(
                color_text("Invalid input. Please enter a valid year.",
                           "ERROR"))
        except ValueError:
            print(color_text("Invalid input. Please enter a valid year.",
                           "ERROR"))


def filter_movies(min_rating=None, min_year=None, max_year=None):
    """
    Filters movies based on arguments passed on by get_filtered_movies.
    Defaults set to 'None' for instances where the user leaves the
    filter fields blank. Returns a list of filtered movies, year and rating.
    """
    movies = storage.list_movies()
    filtered_movies = []
    for title, info in movies.items():
        if (
            (min_rating is None or info["rating"] >= min_rating)
            and (min_year is None or info["year"] >= min_year)
            and (max_year is None or info["year"] <= max_year)
            ):
            filtered_movies.append(f"{title} ({info['year']}): "
                                   f"{info['rating']}")
    return filtered_movies


def get_filtered_movies():
    """Gets valid min rating, min and max year and passes them to the
    filter_movie function and returns the filtered movies.
    """
    min_rating = get_min_rating_filter(
        format_text("Enter minimum rating (leave blank for no minimum rating): ", "INPUT")
    )
    min_year = get_valid_year_filter(
        format_text("Enter start year (leave blank for no start year): ", "INPUT")
    )
    max_year = get_valid_year_filter(
      format_text("Enter end year (leave blank for no end year): ", "INPUT")
    )
    filtered_movies = filter_movies(min_rating, min_year, max_year)
    return filtered_movies


def create_histogram():
    """
    Gets a file name from the user, saves and displays the movie
    rating histogram.
    """
    file_name = input(
        format_text("\nEnter file name for histogram: ", "INPUT")).strip()

    # Extract ratings
    movies = storage.list_movies()
    ratings = [movie["rating"] for movie in movies.values()]

    # Create plot with histogram
    plt.figure()
    plt.hist(ratings, bins=10, color="steelblue", edgecolor="black")

    # Labels and title
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.title("Movie Rating Histogram")

    # Save and close
    plt.savefig(f"{file_name}.jpg", dpi=300)
    plt.close()

    print(color_text("Success! Histogram successfully saved.", "SUCCESS"))


def generate_website():
    """Generates index.html file based on current database."""
    generator.generate_html()
    print(color_text("Success! The 'index.html' file was generated.",
                     "SUCCESS"))


if __name__ == "__main__":
    main()
