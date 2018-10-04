'''
This is means as a quick scraping utility to collect data for a deep
learning model. It is not meant as a complete, well-designed, scraper.
'''

import requests
from bs4 import BeautifulSoup as BS
from PIL import Image
from io import BytesIO
import time


links = []
names = []

for page in range(1,50):
    resp = requests.get(f"https://www.brickowl.com/catalog/lego-parts?page={page}")
    soup = BS(resp.text, 'lxml')
    for i in soup.findAll('a', {"class":"category-item-image"}):
        # links to individual-piece pages, 
        # e.g.: https://www.brickowl.com/catalog/lego-seat-2-x-2-with-sprue-mark-in-seat-4079
        links.append("https://www.brickowl.com"+i.attrs["href"])
        # name, e.g.: "LEGO Seat 2 x 2 with Sprue Mark in Seat (4079)"
        names.append(i.attrs["title"])
    
def get_img(url):
    resp1 = requests.get(url)
    soup1 = BS(resp1.text, 'lxml')
    
    im_url = None
    im_name = None
    
    for im in soup1.findAll("img"):
        try:
            if im.parent.attrs['title'] in names:
                im_url = im.attrs["src"][2:]
                im_name = im.parent.attrs["title"]
        except:
            print("Something went wrong with:", url)
    
    if im_url is not None:
        img = requests.get("http://"+im_url)
        img = Image.open(BytesIO(img.content))
        img.save("lego_images/"+im_name+".jpg")
        
        
for link in links:
    try:
        get_img(link)
    except:
        print("Error with", link)
    
    time.sleep(1)
