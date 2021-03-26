import scrapy
import re


class AutoSpider(scrapy.Spider):
    name = "drom"

    def __init__(self):
        with open('./drom-marks-list.txt') as file:
            lines = file.readlines()

        self.brand_pattern = re.compile("https://www.drom.ru/topcars/(.+)/")
        self.model_pattern = re.compile("(\\S+) (.+)")

        self.start_urls = [f"https://www.drom.ru/topcars/{x.strip()}/" for x in lines]
        # self.start_urls = ["https://www.drom.ru/topcars/bmw/"]

    def parse(self, response):
        url = response.request.url
        alias = self.brand_pattern.match(url).group(1)
        model_scores = response.css('.b-sticker__text::text').getall()
        brand_models = response.css('.b-info-block__title::text').getall()

        for index, model_score in enumerate(model_scores):
            model = self.model_pattern.match(brand_models[index].strip()).group(2)
            brand = self.model_pattern.match(brand_models[index].strip()).group(1)
            yield {'url': url, 'brand': brand, 'alias': alias, 'score': model_score, 'model': model}
