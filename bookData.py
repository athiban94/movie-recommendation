
# coding: utf-8

# In[ ]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import requests                   
from bs4 import BeautifulSoup 
import csv
import re

def extract_source(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source=requests.get(url, headers=headers).text
    return source

def extract_data(source,category="",mvname=""):
    
    mvdata=dict.fromkeys(["category","movie","title","rating","genre","subgenre","theme","keyword","releasedate","country","review"],"")
    #print(mvdata)
    mvdata["category"]=category
    mvdata["movie"]=mvname
    
    soup=BeautifulSoup(source, 'html.parser')
    
    #Title
    names=soup.find('meta',property ="og:title" )
    title=names["content"] if names else "No meta title given"
    mvdata["title"]=title.split("-")[0].strip()
    #print(title)
    
    #Rating
    rating_par = soup.findAll('div', attrs={'itemprop':'ratingValue'})
    if(rating_par!=None and len(rating_par)>0):
        rating=rating_par[0].text.strip()
        mvdata["rating"]=rating
        #print(rating)
    
    #Genre
    genre_par = soup.findAll("span", class_="header-movie-genres")
    gtext= genre_par[0].findAll("a",href=True)
    genre=gtext[0].text
    mvdata["genre"]=genre
    #print(genre)
    
    #Sub_Genre
    sub_genre_par = soup.findAll("span", class_="header-movie-subgenres")
    if(sub_genre_par!=None and len(sub_genre_par)>0):
        stext = sub_genre_par[0].findAll("a",href=True)
        if(stext!=None and len(stext)>0):
            sub_genre=stext[0].text
            mvdata["subgenre"]=sub_genre
            #print(sub_genre)
    
    #Theme
    theme_str = ""
    theme = soup.findAll("div",class_="charactList")
    if(theme!=None and len(theme)>0):
        ttext = theme[0].findAll("a",href=True)
        for themes in ttext:
            theme_str=themes.text+","+theme_str
        theme_str=theme_str.strip(",")
        mvdata["theme"]=theme_str
        #print(theme_str)
    
    #Keyword
    keyword_par = soup.findAll("div",class_="keywords")
    if(keyword_par!=None and len(keyword_par)>0):
        keywords=keyword_par[0].findAll("div",class_="charactList")[0].text.strip()
        #keywords=keyword_par[0]
        mvdata["keyword"]=keywords
    #print(keywords)
    
    #Details
    #date of release
    detail = soup.findAll("hgroup",class_="details")
    for det in detail[0].findAll("span"):
        #print( det.text.split("-")[0].strip(" \n"))
        if det.text.split("-")[0].strip()=="Release Date":
            rel_dte = det.text.split("-")[1].split("(")[0].strip()
            mvdata["releasedate"]=rel_dte
            #print(rel_dte)
    
            #Countries of Release\
        if det.text.split("-")[0].strip()=="Countries":
            cntry=det.text.split("-")[1].strip().strip("|\xa0")
            mvdata["country"]=cntry
            #print(cntry)
    
    #Review
    review_par = soup.findAll("div",itemprop = "description")
    if(review_par!=None and len(review_par)>0):
        review=review_par[0].text.strip()
        mvdata["review"]=review
        #print(review)
    
    return mvdata

url_str1 = 'https://www.allmovie.com/movie/a-star-is-born-v548181'
url_str2 = 'https://www.allmovie.com/movie/the-revenant-v597171'

print(extract_data(extract_source(url_str2)))


#.split("-")[1]

    


# In[ ]:




with open('movie10k.csv', 'w', newline = '') as f:  # Just use 'w' mode in 3.x
    with open('categoryMovieLinksList.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        cnt=0
        seen = set()
        for row in csv_reader:
            if cnt<11000:
                print(row)
                if row[1].strip() not in seen: 
                    seen.add(row[1].strip())
                    mvdict=extract_data(extract_source(row[2]),row[0],row[1])
                    w = csv.writer(f)
                    #w.writeheader()
                    if cnt==0:
                        w.writerow(mvdict.keys())
                    w.writerow(mvdict.values())
                else:
                    print("Duplicate:::::: ",row[1].strip())
                cnt=cnt+1

