import scrapy
from scrapy.loader import ItemLoader
from hotel_scraper.items import TripScraperItem
import os
import pathlib

class HotelSpider(scrapy.Spider):
    name = 'hotel_spider'
    start_urls = ['https://uk.trip.com/hotels/?locale=en-GB&curr=GBP']

    def parse(self, response):
        
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)

        for hotel in response.css('some_selector_for_hotel'):
            hotel_url = hotel.css('some_selector_for_link::attr(href)').get()
            if hotel_url:
                yield response.follow(hotel_url, self.parse_hotel)

    def parse_hotel(self, response):
        loader = ItemLoader(item=TripScraperItem(), response=response)
        loader.add_css('title', 'some_selector_for_title::text')
        loader.add_css('rating', 'some_selector_for_rating::text')
        loader.add_css('location', 'some_selector_for_location::text')
        loader.add_css('latitude', 'some_selector_for_latitude::text')
        loader.add_css('longitude', 'some_selector_for_longitude::text')
        loader.add_css('room_type', 'some_selector_for_room_type::text')
        loader.add_css('price', 'some_selector_for_price::text')
        loader.add_css('images', 'some_selector_for_images::attr(src)')

        item = loader.load_item()

        images = item.get('images')
        if images:
            for image_url in images:
                self.download_image(image_url)

        yield item

    def download_image(self, image_url):
        image_content = requests.get(image_url).content
        image_name = os.path.basename(image_url)
        os.makedirs('images', exist_ok=True)
        with open(f'images/{image_name}', 'wb') as image_file:
            image_file.write(image_content)
