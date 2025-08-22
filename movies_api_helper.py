"""
Movie information retrieval module.

This module connects to the OMDb API to fetch movie details such as title,
release year, rating, and poster URL. The API key is securely loaded from
environment variables using a `.env` file.

Functions:
    get_movie_info(title): Fetch details for a movie by its title.
"""


import os
import requests
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()
API_URL = "http://www.omdbapi.com/?t="
API_KEY = os.getenv('API_KEY')
CONNECT_TIMEOUT = 5  # seconds
READ_TIMEOUT = 10  # seconds
ENCODING = "utf-8"


def get_movie_info(title):
    """Fetch movie details (title, year, rating, poster) from the API by title."""
    try:
        response = requests.get(f"{API_URL + title}&apikey={API_KEY}",
                                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
        response.encoding = ENCODING
        data = response.json()
        return (data['Title'], int(data['Released'][-4:]),
                round(float(data['Ratings'][0]['Value'][0:3]), 1), data['Poster'])
    except requests.exceptions.Timeout:
        print("The API request timed out")
        return None
