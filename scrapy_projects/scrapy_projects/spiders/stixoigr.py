import scrapy
# import pandas as pd
import re

url_template = "http://www.stixoi.info/stixoi.php?info=Lyrics&act=details&song_id={}"
# url_template = "http://www.stixoi.info/stixoi.php?info=Lyrics&act=index&\
# kota={page}&letter={letter}&sort=alpha&order=asc&composer_id=&lyricist_id=&singer_id=&member_id="

letters = "Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω".split()

with open("song_ids_left.txt", 'r') as f:
    ids = f.read().split()

class StixoiSpider(scrapy.Spider):
    name = "stixoigr" # the spider's name


    # instead of defining a start_requests function
    # this works with magic
    # start_urls = [url_template.format(page="1", letter="{}".format(i)) for i in letters]
    start_urls = (url_template.format(id) for id in ids)


    def parse(self, response):
        # try:
        #     max_page = int(response.css("font.blue b::text").extract()[1])
        # except:
        #     max_page = 1

        try:
            song_year = response.css("td.poemtitle0 b::text").extract()[0]
            song_title = song_year.split(" - ")[0]
            year = re.findall(r"[12]\d{3}", song_year)[0] # 1 or 2 followed by 3 more numbers
            lyrics = response.css("div.lyrics::text").extract()
            first_performance = response.css("b a::text").extract()[0]


            yield {
                "song_title": song_title,
                "year": year,
                "lyrics": lyrics,
                "first_performance": first_performance,
            }

        except:
            print("\nID not found\n")


        # globals()["c"] += 1

        # yield {"response":response.body}

        # nexturl_p1 = response.url.split("kota=")
        # nexturl_p2 = nexturl_p1[1].split("&letter")
        # p = int(nexturl_p2[0]) + 1

        # if p <= max_page:
        #     next_page_url = "{}kota={}&letter{}".format(nexturl_p1[0], p, nexturl_p2[1])
        # elif letters:
        #     next_page_url = url_template.format(page="1", letter="{}".format(letters.pop(0))),
        # else:
        #     next_page_url = None

        # next_page_url = url_template.format(c)
        #
        # if next_page_url is not None and c<71480:
        #     yield scrapy.Request(response.urljoin(next_page_url))



        # song_id = response.url.split("=")[-1]
        # song_and_year = response.css("td.poemtitle0 b::text").extract()[0].encode("utf-8").decode()
        # lyrics = [i.encode("utf-8").decode() for i in response.css("div.lyrics::text").extract()]
        # music_lyrics_artist = [i.encode("utf-8").decode() for i in response.css("td.row3 a::text").extract()] # sometimes one is missing, usually the second
        # artist = [i.encode("utf-8").decode() for i in response.css("b a::text").extract()] # sometimes it doesn't exist, but maybe I should delete and keep the previous
        #
        # yield {
        #     'song_id': song_id,
        #     'song_and_year': song_and_year,
        #     'music_lyrics_artist': music_lyrics_artist,
        #     'artist': artist,
        #     'lyrics': lyrics,
        # }