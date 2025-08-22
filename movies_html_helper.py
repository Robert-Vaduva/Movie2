"""
A helper module for generating a static HTML website displaying movies.

This module loads an HTML template, formats movie data into HTML, and writes
the final output to a target file. It integrates with the database helper
to retrieve movies and optionally the API helper to fetch movie details.

Constants:
    TEMPLATE_PATH (str): Path to the HTML template file.
    TARGET_PATH (str): Path where the generated HTML will be saved.
    TITLE_KEYWORD (str): Placeholder keyword in the template for the page title.
    MOVIE_GRID_KEYWORD (str): Placeholder keyword in the template for the movie grid.
    WEB_PAGE_TITLE (str): The title displayed on the generated web page.

Functions:
    - get_html_template(path): Read and return HTML template content from a file.
    - format_data_for_html(movies): Convert movie dictionary data into an HTML list.
    - generate_movies_website(movies): Generate the movie website using the template.
"""


import os


TEMPLATE_PATH = os.path.join("static", "index_template.html")
TARGET_PATH = os.path.join("static", "index.html")
TITLE_KEYWORD = "__TEMPLATE_TITLE__"
MOVIE_GRID_KEYWORD = "__TEMPLATE_MOVIE_GRID__"
WEB_PAGE_TITLE = "Welcome to Robert's Movie App"


def get_html_template(path):
    """Read and return the HTML template content from a file."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
    except OSError as error:
        print(f"File error: {error}")
    return None


def format_data_for_html(movies):
    """Convert movie dictionary data into an HTML list structure."""
    output = ""
    if isinstance(movies, dict):
        for name, value in movies.items():
            movie_title = name
            movie_year = value['year']
            movie_poster = value['url']
            output += "\n"
            output += "\t\t<li>\n"
            output += "\t\t\t<div class=\"movie\">\n"
            output += f"\t\t\t\t<img class=\"movie-poster\" src=\"{movie_poster}\" title=\"\"/>\n"
            output += f"\t\t\t\t<div class=\"movie-title\">{movie_title}</div>\n"
            output += f"\t\t\t\t<div class=\"movie-year\">{movie_year}</div>\n"
            output += "\t\t\t</div>\n"
            output += "\t\t</li>\n"
    else:
        print("In order to format the html file, a dictionary is expected")
    return output


def generate_movies_website(movies):
    """Generate the movie website by injecting data into the HTML template."""
    formated_movie_grid = format_data_for_html(movies)
    template = get_html_template(TEMPLATE_PATH)
    index = template.replace(TITLE_KEYWORD, WEB_PAGE_TITLE)
    index = index.replace(MOVIE_GRID_KEYWORD, formated_movie_grid)
    with open(TARGET_PATH, "w", encoding="utf-8") as file:
        file.write(index)
        print("Website was generated successfully.")
