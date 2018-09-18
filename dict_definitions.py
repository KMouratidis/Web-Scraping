import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/26.0' }
# if you have more than a thousand words, it is advisable to set delay to >1 second
delay = 0.01

df = pd.read_excel("Word_List.xlsx")
# Turn into a set to avoid duplicate scraping
word_list = set(df["Word"].values)

start_time = time.time()

mapping = {} # word -> definition mapping
incomplete = [] # words that were not found but pointed to other words
failed = [] #  unhandled errors

def get_soup_and_def(word=None, input_url=None):
    # delay for politer scraping

    time.sleep(delay)
    url = input_url
    if input_url is None:
        url = "https://www.ldoceonline.com/dictionary/{}".format(word)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    DEF = None
    if input_url is None:
        DEF = soup.find("span", {"class":"DEF"}) # first definition

    return soup, DEF


### Scraping ###
for word in tqdm(word_list):
    soup, DEF = get_soup_and_def(word)

    if DEF is not None:
        tqdm.write(f"Word: {word}.\n-- Definition: {DEF.text}\n")
        mapping[word] = DEF.text
    else:
        try:
            # A definition was not found, but the website points to another
            # dictionary entry, e.g. the entry for "allude" points to "allude to"
            next_word = soup.find("span",
                                  {"class":"REFHWD"}).parent.attrs['href'].split("/")[-1]
            incomplete.append((word, next_word))
            tqdm.write(f"No definition found for word {word}. Will search for {next_word} instead.")
            tqdm.write("Pausing to get new word...")

            soup, DEF = get_soup_and_def(next_word)

            tqdm.write(f"Got word: {next_word}.\n-- Definition: {DEF.text}\n")
            mapping[word] = DEF.text

        except Exception as e:
            # in case of misspelling (redirection to url /spellcheck/
            # e.g.: https://www.ldoceonline.com/spellcheck/english/?q=discomfiture&entrySet=D
            try:
                # find first suggested spelling correction
                next_word = soup.find('ul', {"class":"didyoumean"}).find('li').text.strip()
                soup, DEF = get_soup_and_def(next_word)
                tqdm.write(f"Word: {word}.\n-- Definition: {DEF.text}\n")
                mapping[word] = DEF.text

            except Exception as e2:
                # General error, input a sentinel value,
                # log the exception, and continue
                tqdm.write(f"Failed for: {word}")
                with open(f"{word}.html", 'wb') as f:
                    f.write(soup.prettify("utf-8"))
                mapping[word] = -999
                failed.append((word, e, next_word, e2))


df["definitions"] = df["Word"].apply(lambda x: mapping.get(x, " "))
df.to_excel("results.xlsx")

with open("incomplete.txt", 'w', encoding='utf-8') as f:
    f.write("old: new\n")
    for old,new in incomplete:
        f.write(f"{old}: {new}\n")

with open("failed.txt", 'w', encoding='utf-8') as f:
    f.write("word :error\n")
    for word, error, next_word, error2 in failed:
        f.write(f"{word}: {error}, {next_word}, {error2}\n")


duration = time.time() - start_time
print("Running time: {:.2f}".format(duration))
print("Average time per result: {:.2f}".format(duration / len(word_list)))
print("Words complete:", len(mapping))
print("Words changed:", len(incomplete))
print("Errors:", len(failed))
