import os
import requests
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()
API_URL = "http://www.omdbapi.com/?t="
API_KEY = os.getenv('API_KEY')


def get_movie_info(title):
    resp = requests.get(f"{API_URL + title}&apikey={API_KEY}")
    data = resp.json()
    return (data['Title'], int(data['Released'][-4:]),
            round(float(data['Ratings'][0]['Value'][0:3]), 1), data['Poster'])


if __name__ == "__main__":
    print(get_movie_info("Titanic"))
    print(get_movie_info("Troy"))
	#rova check what happens if movie could not be found
    #rova check what happens if key missing
    #rova print(get_movie_info("1jk1ejlk21j21"))
	#rova check if internet connection is missing
