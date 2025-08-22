from sqlalchemy import create_engine, text


# Define the database URL
DB_URL = "sqlite:///data//movies.db"
# Create the engine
DEBUGGING_ACTIVE = False
engine = create_engine(DB_URL, echo=DEBUGGING_ACTIVE)


def get_all_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}


def add_movie(title, year, rating, url):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, url) "
                                    "VALUES (:title, :year, :rating, :url)"),
                               {"title": title, "year": year, "rating": rating, "url": url})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title=:title"), {"title": title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating=:rating WHERE title=:title"),
                               {"title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")


def main():
    print(get_all_movies())

    add_movie("Caca1", 2001, 8.1)
    add_movie("Caca2", 2002, 8.2)
    add_movie("Caca3", 2003, 8.3)
    print(get_all_movies())

    update_movie("Caca1", 8.2)
    update_movie("Caca2", 8.3)
    update_movie("Caca3", 8.1)
    print(get_all_movies())

    delete_movie("Caca1")
    delete_movie("Caca2")
    delete_movie("Caca3")
    print(get_all_movies())


if __name__ == "__main__":
    main()
