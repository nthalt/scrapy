import json
import re
import scrapy

class HotelSpider(scrapy.Spider):
    """Spider for scraping hotel information from Trip.com"""
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

        # Process inboundCities
        for city in data['initData']['htlsData']['inboundCities']:
            yield from self.process_city_hotels(city)

        # Process outboundCities
        for city in data['initData']['htlsData']['outboundCities']:
            yield from self.process_city_hotels(city)

        # Process fiveStarHotels
        yield from self.process_special_hotels(data['initData']['htlsData']['fiveStarHotels'])

        # Process cheapHotels
        yield from self.process_special_hotels(data['initData']['htlsData']['cheapHotels'])

    def process_city_hotels(self, city):
        for hotel in city['recommendHotels']:
            img_url = f"https://ak-d.tripcdn.com/images{hotel['imgUrl']}"
            yield {
                "propertyTitle": hotel['hotelName'],
                "rating": hotel.get('rating', None),
                "location": city['cityUrl'],
                "latitude": hotel['lat'],
                "longitude": hotel['lon'],
                "room_type": [facility['name'] for facility in hotel.get('hotelFacilityList', [])],
                "price": hotel['displayPrice']['price'],
                "image_urls": [img_url],
                "image_names": [hotel['imgUrl'].split('/')[-1]]
            }

    def process_special_hotels(self, hotels):
        for hotel in hotels:
            img_url = f"https://ak-d.tripcdn.com/images{hotel['imgUrl']}"
            yield {
                "propertyTitle": hotel['hotelName'],
                "rating": hotel.get('rating', None),
                "location": hotel['cityName'],
                "latitude": hotel['lat'],
                "longitude": hotel['lon'],
                "room_type": [facility['name'] for facility in hotel.get('hotelFacilityList', [])],
                "price": hotel['displayPrice']['price'],
                "image_urls": [img_url],
                "image_names": [hotel['imgUrl'].split('/')[-1]]
            }