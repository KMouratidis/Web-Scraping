import scrapy


my_links = {
    "4 Frucht- und Gemüsezubereitung": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start={}&paginatevalues=%7B%22hauptwarengruppe%22%3A%2207%22%2C%22oberwarengruppe%22%3A%220705%22%2C%22warengruppe%22%3A%22070504%22%7D",
    "10 Fruchtmark": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start={}&paginatevalues=%7B%22hauptwarengruppe%22%3A%2207%22%2C%22oberwarengruppe%22%3A%220705%22%2C%22warengruppe%22%3A%22070502%22%7D",
    "11 Fruchtsaftkonzentrate": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start={}&paginatevalues=%7B%22hauptwarengruppe%22%3A%2207%22%2C%22oberwarengruppe%22%3A%220705%22%2C%22warengruppe%22%3A%22070501%22%7D",
    "9 Fruchtgrundstoffe": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start={}&paginatevalues=%7B%22hauptwarengruppe%22%3A%2201%22%2C%22oberwarengruppe%22%3A%220101%22%2C%22warengruppe%22%3A%22010104%22%7D",
    "9 Unverarbeitetes Tiefkühl-Obst": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start=0&paginatevalues=%7B%22hauptwarengruppe%22%3A%2202%22%2C%22oberwarengruppe%22%3A%220201%22%2C%22warengruppe%22%3A%22020101%22%7D",
    "13 Tiefgefrorene Obstprodukte": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start={}&paginatevalues=%7B%22hauptwarengruppe%22%3A%2202%22%2C%22oberwarengruppe%22%3A%220201%22%2C%22warengruppe%22%3A%22020102%22%7D",
    "7 Speiseeis": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start={}&paginatevalues=%7B%22hauptwarengruppe%22%3A%2202%22%2C%22oberwarengruppe%22%3A%220206%22%2C%22warengruppe%22%3A%22020601%22%7D",
    "7 Fruchtjoghurt": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start={}&paginatevalues=%7B%22hauptwarengruppe%22%3A%2205%22%2C%22oberwarengruppe%22%3A%220501%22%2C%22warengruppe%22%3A%22050125%22%7D",
    "22 Fruchtsäfte/Obstsäfte": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start={}&paginatevalues=%7B%22hauptwarengruppe%22%3A%2207%22%2C%22oberwarengruppe%22%3A%220701%22%2C%22warengruppe%22%3A%22070101%22%7D",
    "11 Fruchtnektare": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start={}&paginatevalues=%7B%22hauptwarengruppe%22%3A%2207%22%2C%22oberwarengruppe%22%3A%220701%22%2C%22warengruppe%22%3A%22070102%22%7D",
    "3 Dicksäfte": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start={}&paginatevalues=%7B%22hauptwarengruppe%22%3A%2207%22%2C%22oberwarengruppe%22%3A%220701%22%2C%22warengruppe%22%3A%22070107%22%7D",
    "14 Fruchtsaftgetränke": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start={}&paginatevalues=%7B%22hauptwarengruppe%22%3A%2207%22%2C%22oberwarengruppe%22%3A%220701%22%2C%22warengruppe%22%3A%22070126%22%7D",
    "8 Bio Frucht- und Obstsäfte": "http://www.anuga.de/anuga/Ausstellersuche-Neu/Stichwort-Suche/index.php?fw_goto=aussteller/blaettern&&start={}&paginatevalues=%7B%22hauptwarengruppe%22%3A%2221%22%2C%22oberwarengruppe%22%3A%222107%22%2C%22warengruppe%22%3A%22210710%22%7D",
    }

# links = [v.format(i*20) for k,v in my_links.items() for t in k.split()[0] for i in range(int(t))]

class TropiSpider(scrapy.Spider):
    name = "TropiSpider"

    start_urls = [v.format(i*20) for k,v in my_links.items() for t in k.split()[0] for i in range(int(t))]


    def parse(self, response):

        for link in response.css('td[class="cspacer ca3"] a[href]::attr(href)').extract():
            yield {"link": "http://www.anuga.de" + link}