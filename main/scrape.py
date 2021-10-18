from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)
url = 'https://www.metacritic.com/browse/albums/score/metascore/year/filtered'
browser.visit(url)
url = 'https://www.metacritic.com/browse/albums/score/metascore/year/filtered'


# def metaScrape(url_for_scrape, page_num):

user_agent = {'User-agent': 'Mozilla/5.0'}
# send response
# response_score = requests.get(url_for_scrape, headers = user_agent)
# scrape website into variable to parse
soup_score = BeautifulSoup(response_score.text, 'html.parser')

# create temporary lists for user scores
userP = []
userM = []
userN = []
# create/initialize dictionary 
albums_dict = {'artist':[], 'album':[], 'date':[], 'week_num':[], 'meta_score': [], 'user_score':[]}
# csv variables
output_path = os.path.join('..', 'data', 'meta_scrape.csv')
soup_score.find_all('td', class_='clamp-summary-wrap')
# create soup 
for artist in soup_score.find_all('td', class_='clamp-summary-wrap'):
    # scrape album name
    albums_dict['album'].append(artist.find('a', class_= 'title').text)
    # scrape artist name and strip white space and extra characters
    albums_dict['artist'].append(artist.find('div', class_='artist').text.strip().lstrip('by '))
    # scrape date
    albums_dict['date'].append(artist.find('div', class_='clamp-details').find('span').text)
    # scrape meta_score, handle for changes in class name, convert data type of score to int and append to dict
    # except set to pass since all alubms have a score

    try:
        albums_dict['meta_score'].append(int(artist.find('div', class_='metascore_w large release positive').text))  
    except:
        pass
    try:
        albums_dict['meta_score'].append(int(artist.find('div', class_='metascore_w large release mixed').text))  
    except:
        pass 
    try:
        albums_dict['meta_score'].append(int(artist.find('div', class_='metascore_w large release negative').text))  
    except:
        pass
    # scrape user score, handle errors for tbd/class name and append to temp list
    try:
        userP.append(float(artist.find('div', class_='metascore_w user large release positive').text))  
    except:
        userP.append(0)
    try:
        userM.append(float(artist.find('div', class_='metascore_w user large release mixed').text))  
    except:
        userM.append(0)
    try:
        userN.append(float(artist.find('div', class_='metascore_w user large release negative').text))  
    except:
        userN.append(0)
        
# merge user score by filtering scores from tbd using data type in temporary lists, convert data type of scores to int and append to dictionary        
for a, b, c in zip(userP, userM, userN):
    if isinstance(a, float):
        albums_dict['user_score'].append(int(a * 10))
    elif isinstance(b, float):
        albums_dict['user_score'].append(int(b * 10))
    elif isinstance(c, float):
        albums_dict['user_score'].append(int(c * 10))
    else:
        albums_dict['user_score'].append(c)
# create week_num key and values for weekly scrape
for dates in albums_dict['date']:
    albums_dict['week_num'].append((datetime.strptime(dates, '%B %d, %Y')).isocalendar()[1])
# write dictionary to csv
# create header
fields = ['artist', 'album', 'date', 'week_num', 'meta_score', 'user_score'] 
# create variable for data to be written
data = zip(albums_dict['artist'], albums_dict['album'], albums_dict['date'], albums_dict['week_num'], albums_dict['meta_score'], albums_dict['user_score'])
# create file and write csv
if page_num == 0 or False:
    with open(output_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        for d in data:
            writer.writerow(d)
else:
    with open(output_path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        for d in data:
            writer.writerow(d)
# return 

# def metaScorePages(week_num):  
#     url_pages = f'https://www.metacritic.com/browse/albums/release-date/new-releases/date'
#     # set user agent for header
#     user_agent = {'User-agent': 'Mozilla/5.0'}
#     # send response
#     response_pages = requests.get(url_pages, headers = user_agent)
#     # scrape website into variable to parse
#     soup_pages = BeautifulSoup(response_pages.text, 'html.parser')
#     # set condition to check for one or multiple pages and pass the url to the scrape funtion accordingly
#     if soup_pages.find('li', class_='page last_page') is None:
#             url_for_scrape = 'https://www.metacritic.com/browse/albums/score/metascore/year/filtered'
#             page_num = False
#             metaScrape(week_num, url_for_scrape, page_num)
#     else:
#         pages = int(soup_pages.find('li', class_='page last_page').text)
        
#         for page_num in range(pages):
#             url_for_scrape = f'{url_pages}&page={page_num}'
#             metaScrape(url_pages, page_num)

#     return