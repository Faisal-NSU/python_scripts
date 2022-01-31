# using urls list scrapes sm_sites like facebook pages from landing page

from numpy import NaN
import requests
import pandas as pd
from bs4 import BeautifulSoup
from IPython.display import display
from googlesearch import search

urls = [
    "https://www.daraz.com.bd/",
    "https://www.startech.com.bd/",
    'https://gadgetandgear.com/',
    'https://www.bdshop.com/',
    'https://www.gadgetshopbd.com/',
    'https://gadgetbd.com/',
    'https://ajkerdeal.com/'
]

sm_sites = ['facebook.com']
sm_sites_present = []
columns = ['url'] + sm_sites
df = pd.DataFrame(data={'url' : urls}, columns=columns)

def clear_link(link):
    index = link.find('facebook.com')
    if index == -1:
        return link
    else:  
        link = link[index:]  
        link = 'https://www.' + link      
        return link


def get_sm(row):
    r = requests.get(row['url'])
    output = pd.Series(dtype=str)

    soup = BeautifulSoup(r.content, 'html.parser')
    all_links = soup.find_all('a', href = True)
    flag = False
    count = 0
    for sm_site in sm_sites:
        for link in all_links:
            if sm_site in link.attrs['href']:
                link = link.attrs['href']
                link = clear_link(link)
                output[sm_site] = link
                flag = True

    if flag is False:
        for i in search('facebook '+row['url'],  tld='com', lang='en', num=1, start=0, stop=1, pause=2.0):
            output[sm_site] = i
    return output

sm_columns = df.apply(get_sm, axis=1)
df.update(sm_columns)
df.fillna(value='no link')
print(df)
