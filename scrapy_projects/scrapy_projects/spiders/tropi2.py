import scrapy
import pandas as pd
import re

df = pd.read_json("tropi.json")

v = ['tel:','mailto','http://']

class TropiSpider2(scrapy.Spider):
    name = "TropiSpider2"

    start_urls = list(df.values.ravel())


    def parse(self, response):

        d = dict((key, i) for i in response.css('div.texts a[href]::attr(href)').extract() for key in v if key in i)
        d["company_name"] = response.css("h1::text").extract_first().strip()
        d["fax"] = None

        rest = " ".join(response.css('div.texts::text').extract())
        lst = [x for x in re.sub(" +", " ", re.sub("\t"," ", rest)).split("\n") if (len(x)>1 and ("Halle" not in x))]

        for i in lst:
            if re.findall("[(+)]", i):
                d["fax"] = i
                lst.remove(i)

        d["address"] = ", ".join(lst)

        yield d