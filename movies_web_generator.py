import os
from api_helper import get_movie_info
from movie_storage_sql import get_all_movies


TEMPLATE_PATH = os.path.join("static", "index_template.html")
TARGET_PATH = os.path.join("static", "index.html")
TITLE_KEYWORD = "__TEMPLATE_TITLE__"
MOVIE_GRID_KEYWORD = "__TEMPLATE_MOVIE_GRID__"
WEB_PAGE_TITLE = "Welcome to Robert's Movie App"


def get_html_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        return file.read()


def format_data_for_html(movies_list):
    output = ""
    for name, value in movies_list.items():
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
    return output


def generate_movies_website():
    movies = get_all_movies()
    formated_movie_grid = format_data_for_html(movies)
    template = get_html_template()
    index = template.replace(TITLE_KEYWORD, WEB_PAGE_TITLE)
    index = index.replace(MOVIE_GRID_KEYWORD, formated_movie_grid)
    with open(TARGET_PATH, "w", encoding="utf-8") as file:
        file.write(index)
        print("Website was generated successfully.")


if __name__ == "__main__":
    generate_movies_website()
