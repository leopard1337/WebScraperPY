import scrapy
import json

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['INPUT_URL']

    def parse(self, response):
        page_title = response.xpath('//title/text()').get().strip()
        validated_links = response.css('a[href^="http"]::attr(href)').getall()

        linked_page_titles = []
        for link in validated_links:
            yield scrapy.Request(link, callback=self.parse_linked_page, cb_kwargs={'linked_page_titles': linked_page_titles})

        header_texts = response.css('h1::text').getall()

        data = {
            'page_title': page_title,
            'urls': [{'url': url, 'title': title} for url, title in zip(validated_links, linked_page_titles)],
            'headers': header_texts
        }

        with open('scraped_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)

        self.log("Web scraping completed. Data captured and saved to 'scraped_data.json'.")

    def parse_linked_page(self, response, linked_page_titles):
        linked_title = response.xpath('//title/text()').get().strip()
        linked_page_titles.append(linked_title)
