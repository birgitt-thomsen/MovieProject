from movie_storage import movie_storage_sql as storage

TARGET_HTML = "__TEMPLATE_MOVIE_GRID__"


def serialize_movie(movie):
    """Serialize a movie to HTML."""
    output = ""
    output += '<li>\n'
    output += '<div class="movie">\n'
    output += f'<a href="https://www.imdb.com/title/{movie[1]['imdbID']}">\n'
    output += '<img class="movie-poster"\n'
    output += (f"src='{movie[1]['poster_url']}' "
               f"title='{movie[1]['user_note']}'/>\n"
               f"<div class='movie-title'>{movie[0]}</div>\n"
               f"<div class='movie-year'>{movie[1]['year']}</div>\n"
               f"<div class='movie-ratings'>⭐ {movie[1]['rating']}/10 "
               f"- ❤️ {movie[1]['user_rating']}/10</div>\n"
               )
    output += '</a>\n'
    output += '</div>\n'
    output += '</li>'
    return output


def return_movie_data(movies):
    """ Returns the movie data """
    output = ""
    for movie in movies.items():
        output += serialize_movie(movie)
    return output


def load_html_template(file_path):
    """ Loads an HTML file """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def replace_html(html, movies):
    """ Replaces the HTML template with movie data """
    return html.replace(TARGET_HTML, movies)


def write_movies_html(file_path, html):
    """ Writes movie grid into an HTML file """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html)
    # print("\nSuccess! The 'index.html' file has been generated.")


def generate_html():
    """ Contains steps to generate HTML """
    # load movie data
    movie_data = storage.get_html_movie_data()

    # serialized movie data
    movie_grid = return_movie_data(movie_data)

    # load html template
    html_orig = load_html_template('web/templates/index_template.html')

    # replace original html with new animals data
    updated_html = replace_html(html_orig, movie_grid)

    # write final output
    write_movies_html('web/static/index.html', updated_html)

# generate_html()

