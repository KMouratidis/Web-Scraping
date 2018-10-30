import os
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import numpy as np
import pandas as pd
import time
from tqdm import tqdm_notebook


# Change this
keyword = "disinformation"


df = pd.DataFrame(columns=["title", "authors", "link", "abstract"])
headers = requests.utils.default_headers()
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'


### Oxford

for page in range(1,6):
    print("Page {} out of 5".format(page))
    url = "https://academic.oup.com/journals/search-results?page={}&q={}&\
    allJournals=1&f_ContentType=Journal+Article".format(page, keyword)
    resp = requests.get(url, headers=headers)
    time.sleep(2) # always space requests
    soup = BeautifulSoup(resp.text, "lxml")

    article = 0
    for a,b,c in zip(soup.findAll("a", {"class":"article-link"}),
                 soup.findAll("div", {"class":"sri-authors al-authors-list"}),
                   soup.findAll("div", {"class":'abstract-response-placeholder js-abstract-response-placeholder'})):

        article += 1
        print("Article {} out of 20".format(article))
        title = a.text
        authors = b.text
        link = "https://academic.oup.com" + a.attrs['href']


        aresp = requests.get(link, headers=headers)
        time.sleep(2) # always space requests
        asoup = BeautifulSoup(aresp.text, "lxml")  
        for i in asoup.findAll("div", {"class":"widget-items",
                                  "data-widgetname":"ArticleFulltext"}):
            abstract = " ".join([t.text for t in i.findAll('p')])

        df = df.append(pd.DataFrame([[a.text, b.text, link, abstract]], columns=["title", "authors", "link", "abstract"]))

### Taylor and Francis

for page in range(5):
    print("Page {} out of 5".format(page+1))
    url = "https://www.tandfonline.com/action/doSearch?AllField={}&pageSize=20&subjectTitle=&startPage={}".format(keyword, page)
    resp = requests.get(url)
    time.sleep(2) # always space requests
    soup = BeautifulSoup(resp.text, "lxml")

    article = 0
    for a,b in zip(soup.findAll("a", {"class":"ref nowrap"}),
                soup.findAll("div", {"class":"author"})):
        
        
        article += 1
        try:
            print("Article {} out of 20".format(article))
        
            title = a.text
            link = "https://www.tandfonline.com" + a.attrs["href"]
            authors = (b.text)

            aresp = requests.get(link)
            time.sleep(1) # always space requests
            asoup = BeautifulSoup(aresp.text, "lxml")

            abstract = asoup.findAll("div", {"class":"abstractSection abstractInFull"})[0].text

            df = df.append(pd.DataFrame([[title, authors, link, abstract]],
                                        columns=["title", "authors", "link", "abstract"]))
            
        except:
            pass
            
            
### Code for Wiley omitted

### Springer

for page in range(1,10):

    print("Page {} out of 10".format(page))
    url = "https://link.springer.com/search/page/{}?facet-content-type=%22Article%22&query={}".format(page, keyword)
    resp = requests.get(url)
    time.sleep(1)
    soup = BeautifulSoup(resp.text, "lxml")

    article = 0
    for i, b in zip(soup.findAll('a', {"class":"title"}), soup.findAll('span', {"class":"authors"})):

        article += 1
        
        try:
            print("Article {} out of 20".format(article))

            link = "https://link.springer.com" + i.attrs['href']
            aresp = requests.get(link)
            time.sleep(1)
            asoup = BeautifulSoup(aresp.text, "lxml")

            title = i.text
            authors = b.text.strip()
            abstract = asoup.findAll("p", {"class":"Para"})[0].text

            df = df.append(pd.DataFrame([[title, authors, link, abstract]],
                                        columns=["title", "authors", "link", "abstract"]))

        except:
            pass
            
            
### Sage

for page in range(5):

    print("Page {} out of 5".format(page+1))
    url = "http://journals.sagepub.com/action/doSearch?AllField={}&ContentItemType=research-article&pageSize=20&startPage={}".format(keyword, page)
    resp = requests.get(url)
    time.sleep(1)
    soup = BeautifulSoup(resp.text, "lxml")

    article=0
    for i, b, c in zip(soup.findAll('a', {"class":"ref nowrap"}),
                       soup.findAll('span', {"class":"articleEntryAuthorsLinks"}),
                       soup.findAll('a', {"class":"abstract-link"})):

        article+=1
        print("Article {} out of 20".format(article))
        try:
            authors = ""
            for author in b.findAll("a", {"class":"entryAuthor"}):
                if len(author)>0 and ("See" not in author.text) and ("Search" not in author.text):
                    authors += author.text + ", "


            title = i.text

            link = "http://journals.sagepub.com" + c.attrs['href']
            aresp = requests.get(link)
            time.sleep(1)
            asoup = BeautifulSoup(aresp.text, "lxml")

            abstract = asoup.findAll("div", {"class":"abstractSection abstractInFull"})[0].text

            df = df.append(pd.DataFrame([[title, authors, link, abstract]],
                                            columns=["title", "authors", "link", "abstract"]))
        except Exception as e:
            print(e)
            
            
            
df["Key term"] = keyword
df.drop_duplicates().reset_index(drop=True).to_excel("{}.xlsx".format(keyword))

