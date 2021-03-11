import scrapy


class AutoSpider(scrapy.Spider):
    name = "auto"

    def __init__(self):
        with open('./marks-list.txt') as file:
            lines = file.readlines()
        self.start_urls = [x.strip() for x in lines]

    def parse(self, response):

        model_links = response.css('a.ListingPopularMMM-module__itemName::attr(href)').getall()
        for model_link in model_links:
            yield response.follow(model_link, self.parse)

        car_links = response.css('a.ListingItemTitle-module__link::attr(href)').getall()
        for car_link in car_links:
            yield {'car_link': car_link}

        next_page = response.css('a.ListingPagination-module__next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)