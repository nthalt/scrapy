"""Module providing a function printing python version."""

import scrapy
import json
import re

class HotelSpider(scrapy.Spider):
    name = "hotel"

    def start_requests(self):
        url = "https://uk.trip.com/hotels/"
        params = {
            'locale': 'en-GB',
            'curr': 'GBP'
        }
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        yield scrapy.Request(url, headers=headers, callback=self.parse, cb_kwargs={'params': params})

    def parse(self, response, params):
        script_text = response.xpath('//script[contains(text(), "window.IBU_HOTEL")]/text()').get()
        json_data = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script_text, re.DOTALL).group(1)
        data = json.loads(json_data)

        for city in data['initData']['htlsData']['outboundCities']:
            if city['cityUrl'] == "bangkok":
                for hotel in city['recommendHotels']:
                    img_url = f"https://ak-d.tripcdn.com/images{hotel['imgUrl']}"
                    yield {
                        "propertyTitle": hotel['hotelName'],
                        "rating": hotel['rating'],
                        "location": city['cityUrl'],
                        "latitude": hotel['lat'],
                        "longitude": hotel['lon'],
                        "room_type": [facility['name'] for facility in hotel['hotelFacilityList']],
                        "price": hotel['displayPrice']['price'],
                        "image_urls": [img_url],
                        "image_names": [hotel['imgUrl'].split('/')[-1]]
                    }