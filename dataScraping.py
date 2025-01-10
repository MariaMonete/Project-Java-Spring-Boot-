#importare librarii
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

all_movies=[]
url='https://editorial.rottentomatoes.com/guide/best-movies-of-all-time/'

#cerere catre site
response=requests.get(url)
soup=BeautifulSoup(response.text,'html.parser')

#gasirea tuturor sectiunilor pentru filme
movies=soup.find_all('div', class_='article_movie_title')

for movie in movies:
    try:
        #titlu
        title_tag=movie.find('a')
        title=title_tag.text.strip() if title_tag else "N/A"

        #rating
        rating_tag = movie.find_next ( 'span', class_='tMeterScore' )
        rating = rating_tag.text.strip () if rating_tag else "N/A"

        #an
        year_tag = movie.find_next ( 'span', class_='start-year' )
        year = year_tag.text.strip ( "()" ) if year_tag else "N/A"

        #critics
        consensus_tag = movie.find_next ( 'div', class_='info critics-consensus' )
        consensus = consensus_tag.text.strip () if consensus_tag else "N/A"

        #synopsis
        synopsis_tag = movie.find_next ( 'div', class_='info synopsis' )
        synopsis = synopsis_tag.text.strip () if synopsis_tag else "N/A"

        #actori
        starring_section = movie.find_next ( 'div', class_='info cast' )
        starring = ", ".join (
            [a.text.strip () for a in starring_section.find_all ( 'a' )] ) if starring_section else "N/A"

        #regizor
        director_tag = movie.find_next ( 'div', class_='info director' )
        director = director_tag.text.strip () if director_tag else "N/A"

        #adaugare date in lista de filme
        all_movies.append({
            "Title":title,
            "Rating":rating,
            "Year":year,
            "Critics Consensus": consensus,
            "Synopsis":synopsis,
            "Starring Actors": starring,
            "Director":director
        })
        #@pauza pentru a nu fi blocat de server
        time.sleep(1)

    except Exception as e:
        print(f"Error scraping movie: {e}")
        continue

#creare csv si exportul sal
df=pd.DataFrame(all_movies)
df.to_csv("best_movies.csv",index=False)
print("CSV file created")
