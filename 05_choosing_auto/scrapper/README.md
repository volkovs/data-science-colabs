# Data Scrapper

This document contains spider script comments and running instructions

## Setup

Please create scrapy project (for further details please look at [scrapy.org](https://docs.scrapy.org/en/latest/intro/tutorial.html#creating-a-project)):
1. `scrapy startproject tutorial`
1. copy spider scripts from `spiders` directory to `spiders` directory in the generated project
1. copy initial links file `marks-list.txt` to the root folder of the project (or running folder)
1. `scrapy crawl <specific spider name> -O output.json`

## Spiders

1. `auto_spider` navigates through all next page links for every brand and collects every link to used car
1. `auto_details_spider` visits every link collected on previous step and collects all the data on used car

## Running example

1. `scrapy crawl auto_spider -O car-links-big.json`
1. `scrapy crawl auto_details_spider -O auto-details-big.json` - ~8 hours

## Running results example

- [car-links-big.json](https://github.com/volkovs/data-science-colabs/raw/main/05_choosing_auto/scrapper/car-links-big.json.zip)
- [auto-details-big.json](https://github.com/volkovs/data-science-colabs/raw/main/05_choosing_auto/scrapper/auto-details-big.json.zip)

 