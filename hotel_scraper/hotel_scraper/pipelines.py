"""Module providing a function printing python version."""

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class HotelScraperPipeline:
#     def process_item(self, item, spider):
#         return item






# import os
# import scrapy
# from scrapy.pipelines.images import ImagesPipeline
# from scrapy.exceptions import DropItem

# class CustomImagesPipeline(ImagesPipeline):

#     def open_spider(self, spider):
#         # Create the images directory if it doesn't exist
#         if not os.path.exists('images'):
#             os.makedirs('images')

#     def file_path(self, request, response=None, info=None):
#         # Use the image name extracted from the request meta
#         image_name = request.meta['image_name']
#         return f'images/{image_name}'

#     def get_media_requests(self, item, info):
#         # Yield image URLs along with custom image names
#         for image_url, image_name in zip(item.get('image_urls', []), item.get('image_names', [])):
#             yield scrapy.Request(image_url, meta={'image_name': image_name})

#     def item_completed(self, results, item, info):
#         # Check if all images are downloaded
#         if 'image_urls' in item:
#             if not all(result[0] for result in results):
#                 raise DropItem("Image download failed")
#         return item





import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import scrapy

# Load environment variables
load_dotenv()

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True)
    property_title = Column(String)
    rating = Column(Float)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    room_type = Column(ARRAY(String))
    price = Column(Float)
    img = Column(String)

class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_name = request.meta['image_name']
        return f'{image_name}'

    def get_media_requests(self, item, info):
        for image_url, image_name in zip(item.get('image_urls', []), item.get('image_names', [])):
            yield scrapy.Request(image_url, meta={'image_name': image_name})

    def item_completed(self, results, item, info):
        if 'image_urls' in item:
            if not all(result[0] for result in results):
                raise DropItem("Image download failed")
            item['img'] = f"images/{item['image_names'][0]}"
        return item

class PostgresPipeline:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise Exception("DATABASE_URL environment variable is not set")
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)

    def open_spider(self, spider):
        Base.metadata.create_all(self.engine)

    def process_item(self, item, spider):
        session = self.Session()
        hotel = Hotel(
            property_title=item['propertyTitle'],
            rating=item['rating'],
            location=item['location'],
            latitude=item['latitude'],
            longitude=item['longitude'],
            room_type=item['room_type'],
            price=item['price'],
            img=item['img']
        )
        session.add(hotel)
        session.commit()
        session.close()
        return item
    