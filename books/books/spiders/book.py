import scrapy

from books.items import BooksItem

#Scrapy Spider

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"] #list of strings containing urls 

    def parse(self, response):
        #parsing the data from the css selectors
        for book in response.css("article.product_pod"):
            item = BooksItem()
            item["url"] = book.css("h3 > a::attr(href)").get()
            item["title"] = book.css("h3 > a::attr(title)").get()
            item["price"] = book.css(".price_color::text").get()
            yield item #using yield to turn parse() into a function that generates results rather than returning the response 

        next_page = response.css("li.next > a::attr(href)").get() #grabbing the href link that takes the user to the next page of books
        if next_page: #if another page exists
            next_page_url = response.urljoin(next_page) #turning the href into an absolute url
            yield scrapy.Request(url=next_page_url, callback=self.parse) #creates a scrapy request on the next page 
