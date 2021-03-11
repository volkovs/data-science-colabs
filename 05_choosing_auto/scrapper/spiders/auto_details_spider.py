import scrapy
import re


class AutoDetailsSpider(scrapy.Spider):
    name = "auto-details"

    def __init__(self):
        with open('./car-links-big.json') as file:
            lines = file.readlines()
        self.start_urls = [x.strip() for x in lines]
        # self.start_urls = [
        #     "https://auto.ru/cars/used/sale/ac/cobra/1102143699-0da687c4/",
        #     "https://auto.ru/cars/used/sale/ford/explorer/1101752365-61bdffa4/"
        # ]

    # start_urls = [
    #     "https://auto.ru/cars/zotye/used/",
    # ]

    def parse(self, response):
        # car_links = response.xpath("//a[contains(@class, 'ListingItemTitle-module__link')]/@href").getall()

        number_of_doors = None
        number_of_doors_string = response.css('.CardInfoRow_bodytype span:last-of-type ::text').get()
        body_type = number_of_doors_string
        matcher = re.match(r"(.+)(\d).*", number_of_doors_string)
        if matcher is not None:
            body_type = matcher.group(1).replace(" ", "")
            number_of_doors = matcher.group(2)

        engine_power = None
        engine_displacement = None
        engine_string = response.css('.CardInfoRow_engine span:last-of-type ::text').get().replace(" ","")
        matcher = re.match(r"(\d+\.*\d*)[^\d]+(\d+).*", engine_string)
        if matcher is not None:
            engine_displacement = matcher.group(1)
            engine_power = matcher.group(2)

        mileage_string = response.css('.CardInfoRow_kmAge span:last-of-type ::text').get().replace(" ", "").replace("км", "").replace(" ", "")
        mileage = int(mileage_string)

        owners = None
        owners_string = response.css('.CardInfoRow_ownersCount span:last-of-type ::text').get()
        matcher = re.match(r".*(\d+).*", owners_string)
        if matcher is not None:
            owners = matcher.group(1)

        price = int(response.css('.CardSidebarActions__price .OfferPriceCaption__price ::text').get().replace(" ", "").replace("₽", "").replace(" ", ""))

        complectation = {}
        complectation_groups = response.css('.ComplectationGroups__group')
        for complectation_group in complectation_groups:
            group_name = complectation_group.css('.ComplectationGroups__itemName ::text').get()
            group_items = complectation_group.css('.ComplectationGroups__itemContentEl ::text').getall()
            complectation[group_name] = group_items

        # print(complectation)

        yield {
            "bodyType": body_type,
            "brand": response.css('.CardBreadcrumbs:nth-child(2) a ::text').get(),
            "color": response.css('.CardInfoRow_color span:last-of-type ::text').get(),
            "fuelType": response.css('.CardInfoRow_engine span:last-of-type a ::text').get(),
            "modelDate": None,
            "name": response.css('.CardInfoRow_engine span:last-of-type ::text').get().replace(" ",""),
            "numberOfDoors": number_of_doors,
            "productionDate": response.css('.CardInfoRow_year span:last-of-type ::text').get(),
            "vehicleConfiguration": None,
            "vehicleTransmission": response.css('.CardInfoRow_transmission span:last-of-type ::text').get(),
            "engineDisplacement": engine_displacement,
            "enginePower": engine_power,
            "description": response.css('.CardDescription__textInner span:last-of-type ::text').get(),
            "mileage": mileage,
            "Комплектация": complectation,
            "Привод": response.css('.CardInfoRow_drive span:last-of-type ::text').get(),
            "Руль": response.css('.CardInfoRow_wheel span:last-of-type ::text').get(),
            "Состояние": response.css('.CardInfoRow_state span:last-of-type ::text').get(),
            "Владельцы": owners,
            "ПТС": response.css('.CardInfoRow_pts span:last-of-type ::text').get(),
            "Таможня": True if response.css('.CardInfoRow_customs span:last-of-type ::text').get() == 'Растаможен' else False,
            "Владение": "",
            "price": price,
            "start_date": response.xpath('//div[contains(@title,"Дата размещения объявления")]').css('::text').get(),
            "hidden": "",
            "model": response.css('.CardBreadcrumbs .CardBreadcrumbs__item:nth-child(4) ::text').get(),
            "url": response.request.url
        }