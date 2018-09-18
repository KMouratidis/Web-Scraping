import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
    "http://quotes.toscrape.com/page/1",
    "http://quotes.toscrape.com/page/2",
    ]
    # By using start_urls instead of urls I don't need to define
    # the start_requests function

    # def start_requests(self):
        # urls = [
        # "http://quotes.toscrape.com/page/1",
        # "http://quotes.toscrape.com/page/2",
        # ]

        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)
        #     # a generator: returns the yield,
        #     # and then when rerun stars from here

    def parse(self, response):
        # page = response.url.split('/')[-2] # ??
        # filename = "quotes-{}.html".format(page)
        # with open(filename,"wb") as f:
        #     f.write(response.body) # this would be to save the file
        # self.log("Saved file " + filename)

        for quote in response.css("div.quote"):
            yield {
            "text": quote.css("span.text::text").extract_first(),
            "author": quote.css("small.author::text").extract_first(),
            "tags": quote.css("div.tags a.tag::text").extract()
            }

            next_page = response.css("li.next a::attr(href)").extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
