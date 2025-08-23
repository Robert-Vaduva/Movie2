"""
Movie Database CLI App

This module provides a simple command-line interface (CLI) for managing a movie database.
Users can add, delete, list, update, filter, and view statistics on movies stored in memory.
"""


import sys
import random
import statistics
import helpers.sql.movies_sql_helper as movies_sql_helper
import helpers.api.movies_api_helper as movies_api_helper
import helpers.html.movies_html_helper as movies_html_helper


KEY_POSITION = 0
VALUES_POSITION = 1
MAX_MOVIE_NAME_LENGTH = 30
MIN_YEAR = 1900
MAX_YEAR = 2030
MIN_RATING = 0.0
MAX_RATING = 10.0


def get_valid_input(prompt, min_value, max_value, default_value):
    """Prompt for a numeric value within range or return default if blank."""
    while True:
        user_input = input(prompt)
        if not user_input.strip():
            return default_value
        if any(char.isalpha() for char in user_input):
            print("Invalid input. Please enter a valid number.")
            continue
        try:
            value = float(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if not min_value <= value <= max_value:
            print(f"Please enter a valid value, in the range {min_value}-{max_value}")
            continue
        return value


def exit_fnc(_movies):
    """Exit the application with a goodbye message."""
    print("Bye!")
    sys.exit()


def list_movies(movies):
    """Display all movies in the database with their year and rating."""
    print(f"\n{len(movies)} movies in total")
    try:
        for name, value in movies.items():
            print(f"{name} ({value['year']}): {value['rating']}")
        input("\nPress enter to continue ")
    except (TypeError, ValueError, KeyError) as error:
        print("List movie error: ", error)


def add_movie(movies):
    """Prompt the user to add a new movie to the database."""
    while True:
        movie_name = str(input("Enter new movie name: "))
        if movie_name == "" or len(movie_name) > MAX_MOVIE_NAME_LENGTH:
            print(f"Movie name must not be empty nor "
                  f"greater than {MAX_MOVIE_NAME_LENGTH} characters")
        else:
            if movie_name in movies.keys():
                print(f"Movie \"{movie_name}\" already exists!")
                input("\nPress enter to continue ")
                return
            break
    if movies_api_helper.get_movie_info(movie_name) is not None:
        title, year, rating, poster_url = movies_api_helper.get_movie_info(movie_name)
        movies_sql_helper.add_movie(title, year, rating, poster_url)
    else:
        print("API service not available at the moment, try again later")
    input("\nPress enter to continue ")


def delete_movie(movies):
    """Prompt the user to delete a movie from the database by name."""
    try:
        movie_name = str(input("Enter movie name to delete: "))
        if movie_name in movies.keys():
            movies_sql_helper.delete_movie(movie_name)
        else:
            print(f"Movie \"{movie_name}\" doesn't exist!")
        input("\nPress enter to continue ")
    except (TypeError, ValueError) as error:
        print("Delete movie error: ", error)


def update_movies(movies):
    """Update the rating of an existing movie."""
    try:
        movie_name = str(input("Enter movie name: "))
        if movie_name not in movies.keys():
            print(f"Movie \"{movie_name}\" does not exist!")
            input("\nPress enter to continue ")
            return
        while True:
            try:
                movie_rating = float(input("Enter new movie rating: "))
                if MIN_RATING > movie_rating or movie_rating > MAX_RATING:
                    print(f"Please enter a valid rating, in the range {MIN_RATING}-{MAX_RATING}")
                else:
                    break
            except (TypeError, ValueError) as error:
                print("Add movie error:", error)
        movies_sql_helper.update_movie(movie_name, movie_rating)
        input("\nPress enter to continue ")
    except (TypeError, ValueError) as error:
        print("Update movie error: ", error)


def stats(movies):
    """Display the average, median, best, and the worst movie ratings."""
    # Get the average rating
    total_ratings = 0
    ratings = []
    for _, value in movies.items():
        total_ratings += float(value['rating'])
        ratings.append(float(value['rating']))
    avg_ratings = total_ratings / len(movies)
    sorted_movie = sorted(movies.items(),
                          key=lambda x: x[1]['rating'],
                          reverse=True)
    print(f"Average rating: {avg_ratings:.1f}")
    print(f"Median rating: {statistics.median(ratings):.1f}")
    print(f"Best movie: {sorted_movie[0][0]}, {sorted_movie[0][1]['rating']}")
    print(f"Worst movie: {sorted_movie[-1][0]}, {sorted_movie[-1][1]['rating']}")
    input("\nPress enter to continue ")


def random_movie(movies):
    """Display a randomly selected movie from the database."""
    key, value = random.choice(list(movies.items()))
    print(f"\nYour movie for tonight: {key}, it's rated {value['rating']}")
    input("\nPress enter to continue ")


def search_movie(movies):
    """Search for movies by partial name and display matches."""
    try:
        user_input = str(input("Enter part of movie name: "))
        print()
        for key, value in movies.items():
            if user_input.lower() in key.lower():
                print(f"{key}, {value['rating']}")
        input("\nPress enter to continue ")
    except (TypeError, ValueError) as error:
        print("Random movie error: ", error)


def movies_by_rating(movies):
    """List all movies sorted by rating in descending order."""
    sorted_movies = sorted(movies.items(),
                           key=lambda x: x[1]['rating'],
                           reverse=True)
    print()
    for movie in sorted_movies:
        print(f"{movie[KEY_POSITION]} "
              f"({movie[VALUES_POSITION]['year']}): "
              f"{movie[VALUES_POSITION]['rating']}")
    input("\nPress enter to continue ")


def movies_by_year(movies):
    """List movies sorted by release year, based on user preference."""
    while True:
        try:
            user_input = str(input("Do you want the latest movies first? (Y/N) "))
            if user_input.lower() == "y":
                sorted_movies = sorted(movies.items(),
                                       key=lambda x: x[VALUES_POSITION]['year'],
                                       reverse=True)
                print()
                for movie in sorted_movies:
                    print(f"{movie[KEY_POSITION]} "
                          f"({movie[VALUES_POSITION]['year']}): "
                          f"{movie[VALUES_POSITION]['rating']}")
                input("\nPress enter to continue ")
                break
            if user_input.lower() == "n":
                sorted_movies = sorted(movies.items(),
                                       key=lambda x: x[VALUES_POSITION]['year'],
                                       reverse=False)
                print()
                for movie in sorted_movies:
                    print(f"{movie[KEY_POSITION]} "
                          f"({movie[VALUES_POSITION]['year']}): "
                          f"{movie[VALUES_POSITION]['rating']}")
                input("\nPress enter to continue ")
                break
            if user_input.lower() != "y" and user_input.lower() != "n":
                print("Please enter \"Y\" or \"N\"")
        except (TypeError, ValueError) as error:
            print("Movie by year error: ", error)


def filter_movies(movies):
    """Filter and display movies based on optional rating and year range."""
    min_rating = get_valid_input(
        "Enter minimum rating (leave blank for no minimum rating): ",
        MIN_RATING, MAX_RATING, MIN_RATING
    )
    start_year = get_valid_input(
        "Enter start year (leave blank for no start year): ",
        MIN_YEAR, MAX_YEAR, MIN_YEAR
    )
    end_year = get_valid_input(
        "Enter end year (leave blank for no end year): ",
        MIN_YEAR, MAX_YEAR, MAX_YEAR
    )

    print()
    for title, info in movies.items():
        if min_rating <= info['rating'] and start_year <= info['year'] <= end_year:
            print(f"{title} ({info['year']}): {info['rating']}")

    input("\nPress enter to continue ")


def generate_website(movies):
    """Generate and display the movies' website."""
    movies_html_helper.generate_movies_website(movies)


FUNCTIONS = {0: exit_fnc, 1: list_movies, 2: add_movie, 3: delete_movie,
             4: update_movies, 5: stats, 6: random_movie, 7: search_movie,
             8: movies_by_rating, 9: movies_by_year, 10: filter_movies,
             11: generate_website}


def main():
    """Main function that runs the CLI menu and handles user input."""
    print("********** My Movies Database **********")
    while True:
        try:
            print("\nMenu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Update movie")
            print("5. Stats")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")
            print("9. Movies sorted by year")
            print("10. Filter movies")
            print("11. Generate website")
            user_input = int(input(f"\nEnter choice (0-{len(FUNCTIONS) - 1}): "))
            if 0 <= user_input < len(FUNCTIONS):
                movies_data = movies_sql_helper.get_all_movies()
                if movies_data is not None:
                    FUNCTIONS[user_input](movies_data)
                else:
                    print("The database failed to load the requested data")
            else:
                print(f"Invalid choice, please select a number between 0 and {len(FUNCTIONS) - 1}")
        except (TypeError, ValueError, KeyError) as error:
            print("Main function error:", error)


if __name__ == "__main__":
    main()
