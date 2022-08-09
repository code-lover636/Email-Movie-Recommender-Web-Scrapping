from bs4 import BeautifulSoup
import requests
import random
from sendmail import send

def random_movie(movie_list,count=5):
    mlist = []
    title = []
    while count > 0:
        movie = random.choice(movie_list)
        if movie not in mlist:
            mlist.append(movie)
        else: 
            continue  
        count -= 1
            
    for m in mlist:
        if m[0] in title: 
            random_movie(movie_list)
            break
        else: 
            title.append(m[0])
    return mlist


def extract_details(url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, 'html.parser')
    table = soup.find('tbody', class_='lister-list')
    movie_list = []
    for movie in table.find_all('tr'):
        tag1 = movie.find('td', class_='titleColumn')
        tag2 = movie.find('td', class_='ratingColumn')
        tag3 = movie.find('td', class_='posterColumn')
        # Poster image 
        src = tag3.img.get("src")
        # Movie title
        title = tag1.a.text
        link = tag1.a.get("href")                  
        # Movie Year
        if tag1.contents[3].name == "span":   year = tag1.span.text.strip("()")
        else: year="N/A"
        # Movie rating
        try:   rating = tag2.strong.text
        except AttributeError: rating = 'N/A'
        movie_list.append((title, year, rating, src, link))
    return movie_list
            
    
if __name__ == '__main__':   
    popular = "https://www.imdb.com/chart/moviemeter/"
    top_rated = "https://www.imdb.com/chart/top/"     
    movie_list = extract_details(popular)+ extract_details(top_rated)
    mlist = random_movie(movie_list)
    send(mlist)