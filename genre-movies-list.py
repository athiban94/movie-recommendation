import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

headers = { 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.'
                          '86 Safari/537.36'}

# site url
siteURL = "https://www.allmovie.com"
movieCorpusList = []
def scrapePageContents(category, categoryLink):
    print(categoryLink)
    page = requests.get(categoryLink, headers=headers)
    if page.status_code == 200:
        print("succes")
        soup = BeautifulSoup(page.content, 'html.parser')
        pagenationNext = soup.select('div.pagination span.next a')

        moviesList = soup.select("div.movie-highlights div.movie_row div.movie p.title a")
        for movie in moviesList:
            movieTuple = (category, movie.text.strip(), siteURL + movie["href"])
            movieCorpusList.append(movieTuple)
        if(pagenationNext):
            for page in pagenationNext:
                url = siteURL + page["href"]
                scrapePageContents(category, url)
        else:
            print("End of category: " + category)

def generateMovieCateoryTuples(categoryList):
    for category, categoryLink in categoryList.items():
        scrapePageContents(category, categoryLink)

    for element in movieCorpusList:
        print(element)
    return movieCorpusList

def saveMoviesInCSV(movieCorpusList):
    with open('categoryMovieLinksList.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for tup in movieCorpusList:
            writer.writerow(tup)


if __name__ == "__main__":
    data = pd.read_csv("genres.csv", header=0)
    categoryList = dict(zip(data["Genre"].values.tolist(), data["link"].values.tolist()))
    # generateMovieCateoryTuples(categoryList)
    entireMovieList = generateMovieCateoryTuples(categoryList)
    saveMoviesInCSV(entireMovieList)

