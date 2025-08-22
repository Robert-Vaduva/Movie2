import requests


BASE_URL = "http://www.omdbapi.com/?apikey=23f2b8ab"


def get_movie_info(title):
    resp = requests.get(f"{BASE_URL}&t={title}")
    data = resp.json()
    return (data['Title'], int(data['Released'][-4:]),
            round(float(data['Ratings'][0]['Value'][0:3]), 1), data['Poster'])


if __name__ == "__main__":
    #print(get_movie_info("Titanic"))
	#rova check what happens if movie could not be found
    print(get_movie_info("1jk1ejlk21j21"))
	#rova check if internet connection is missing
