"""Module providing a function printing python version."""

# from pathlib import Path
# import json
# import re
# import scrapy

# class HotelSpider(scrapy.Spider):
#     """Class representing a person"""

#     name = "hotel"
#     def start_requests(self):
#         url = "https://uk.trip.com/hotels/"
#         params = {
#             'locale': 'en-GB',
#             'curr': 'GBP'
#         }
#         headers = {
#             'Accept': '*/*',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Connection': 'keep-alive',
#         }

#         yield scrapy.Request(url, headers=headers, callback=self.parse, cb_kwargs={'params': params})

#     def parse(self, response, params):
        
#         # Extract the script tag content
#         script_text = response.xpath('//script[contains(text(), "window.IBU_HOTEL")]/text()').get()

#         # Use regex to find the JSON object within the script
#         json_data = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script_text, re.DOTALL).group(1)

#         # Parse the JSON object
#         data = json.loads(json_data)

#         hotels = []
#         for city in data['initData']['htlsData']['inboundCities']:
#             if city['cityUrl'] == "london":
#                 for hotel in city['recommendHotels']:
#                     img_url = f"https://ak-d.tripcdn.com/images{hotel['imgUrl']}"
#                     item = {
#                         "propertyTitle": hotel['hotelName'],
#                         "rating": hotel['rating'],
#                         "location": city['cityUrl'],
#                         "latitude": hotel['lat'],
#                         "longitude": hotel['lon'],
#                         "room_type": [facility['name'] for facility in hotel['hotelFacilityList']],
#                         "price": hotel['displayPrice']['price'],
#                         "image_urls": [img_url],  # This is used by the pipeline to download images
#                         "image_names": [hotel['imgUrl'].split('/')[-1]]  # Filename for saving locally
#                     }
#                     hotels.append(item)

#         # Save the results to a JSON file after processing
#         output_file = 'london_hotels.json'
#         Path(output_file).write_text(json.dumps(hotels, indent=4))
#         self.log(f'Saved file {output_file}')








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