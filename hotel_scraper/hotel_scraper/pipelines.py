# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class HotelScraperPipeline:
#     def process_item(self, item, spider):
#         return item

import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class CustomImagesPipeline(ImagesPipeline):

    def open_spider(self, spider):
        # Create the images directory if it doesn't exist
        if not os.path.exists('images'):
            os.makedirs('images')

    def file_path(self, request, response=None, info=None):
        # Use the image name extracted from the request meta
        image_name = request.meta['image_name']
        return f'images/{image_name}'

    def get_media_requests(self, item, info):
        # Yield image URLs along with custom image names
        for image_url, image_name in zip(item.get('image_urls', []), item.get('image_names', [])):
            yield scrapy.Request(image_url, meta={'image_name': image_name})

    def item_completed(self, results, item, info):
        # Check if all images are downloaded
        if 'image_urls' in item:
            if not all(result[0] for result in results):
                raise DropItem("Image download failed")
        return item
