import requests
from bs4 import BeautifulSoup
import csv

headers = { 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.'
                          '86 Safari/537.36'}

# site url
siteURL = "https://www.allmovie.com"

def getGenreContentMovies(genreLink):
    page = requests.get(genreLink, headers=headers)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        # Creating a dictionary to store the movies - movie-name as "key" and movie-DPL as "value"
        movieListDictionary = {}

        moviesList = soup.select("section.highlights div.movie-highlights .movie_row .movie p.title a")
        for movie in moviesList:
            movieListDictionary[movie.text.strip()] = siteURL + movie['href']

        print(movieListDictionary)




if __name__ == "__main__":

    # send a get request to the web page
    page = requests.get("https://www.allmovie.com/genres", headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        # Creating a dictionary to store the genre name as "key" and link as "value"
        genres = {}

        genreList = soup.select("div.genres div.genre h3 a")
        for genre in genreList:
            genres[genre.text] = genre['href']

        with open('genres.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['Genre', 'link'])
            for key, value in genres.items():
                writer.writerow([key, value])

        for i, (genreName, genreLink) in enumerate(genres.items()):
            getGenreContentMovies(genreLink)
            break

    else:
        print("Oops! could not get page, Error: ",page.status_code)
