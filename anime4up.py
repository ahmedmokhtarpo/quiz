# -*- coding: utf-8 -*-
"""anime4up.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Yey-lLxfdapH-2_k8FGTtHlEY0Cy-0CX

# **this is blogger auto publidh vedio**
"""

from bs4 import BeautifulSoup
import requests
from itertools import zip_longest
import csv
import json

url = 'https://ww.anime4up.com/قائمة-الانمي'
all_anime_url = []
all_anime_poster = []
all_anime_title = []
all_anime_status = []


def get_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    for i in soup.find_all('img', class_='img-responsive'):
        all_anime_poster.append(i['src'])
    for i in soup.find_all('div', class_='anime-card-status'):
        all_anime_status.append(i.get_text())
    for i in soup.find_all('div', class_='anime-card-title'):
        title = i.get_text().strip('\n')
        if '/' in title :
          title = title.replace('/','_')
          all_anime_title.append(title)
        all_anime_title.append(title)
        all_anime_url.append(i.a['href'])

def get_espoid(es_url):
    aime_servar = 'google drive'
    re = requests.get(es_url)
    soup = BeautifulSoup(re.content, 'lxml')
    lis = soup.find('ul', {"class" : "nav nav-tabs"}).find_all('li')
    espoid_src = []
    
    for li in lis :
        if 'google drive' in li.a.get_text():
            espoid_src.append(li.a['data-ep-url'])
            break
        elif 'mp4upload' in li.a.get_text() :
            espoid_src.append(li.a['data-ep-url'])
            break
        else:
            continue    
    return espoid_src 
def anime_finish(all_anime_url, all_anime_title):
    t = 0
    for url in all_anime_url:

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        anime_espoid_img = soup.find('img', class_="img-responsive")['src']
        espoids_src =[]
        for espoid in soup.find_all('div', class_='episodes-card-title'):
            espoid_link = espoid.a['href']
            src = get_espoid(espoid_link)
            espoids_src.append(src)
       
  
        with open(all_anime_title[t]+'.txt','w') as anime_file: 
            
            for s in espoids_src:
              
              anime_file.write(f'{s}\n')
          

        espoids_src.clear()
            
        print(f"{all_anime_title[t]}  Finsihed")
        print(all_anime_url[t])
        t += 1


def main(url, page_count):
    for p in range(page_count):
           
        get_data(url + '/page/' + str(p))
        anime_about = [all_anime_title,all_anime_poster,all_anime_status,all_anime_url]
        exported = zip_longest(*anime_about)

        with open("about.csv", "w") as f:
            head = ['name','poster','status','url in anime4up','espoids src']
            w = csv.writer(f)
            w.writerow(head)
            w.writerows(exported)
            f.close()
        anime_finish(all_anime_url, all_anime_title)
        print(f'{p+1} Done!')


main(url, 13)

def post(title, content='empty',poster,blogId='646319922572405238'):
  # this is the header of Oauth request to send api token
  headers = {
      "Authorization":
      "Bearer ya29.A0AfH6SMA3v-A_SEAhxn0ajyl_-41Gbi3xOjZJcaEl4IfiNdt6CefliBrToIxwNKjUKU-ENfa3r1dxmJkIx91kRKp7tX_ZsvMMD5GqrsstafuRMOmXxPvnjyAH2DeFHNDdJwtR8wVot78jpPBrwORLYYlLD2Lz"
      
  }
  # these are the data of file wich will be created on google drive


  pyload = {
    "kind": "blogger#post",
  "blog": {"id": blogId},
  "title": title,
  "content": content
}
  
  
  url = f'https://www.googleapis.com/blogger/v3/blogs/{blogId}/posts'
    # tis is the  upload oprating
  r = requests.post(
      url,
      headers=headers,
      data=json.dumps(pyload)
      )
  print(r.status_code)

import os

def publish(anime,src,poster):

  content = f'''
  
        
  
  
   '''
  post(title=anime, content=content, poster=poster,blogId='646319922572405238')


path, dirs, files = next(os.walk('anime_data'))
file_count = len(files)

for f in range(file_count):
  with open(files[f] 'r') as af:
    for line in af :
      publish(all_anime_title[f], line)