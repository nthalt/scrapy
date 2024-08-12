"""Module providing a function printing python version."""
import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from scrapy.exceptions import DropItem
import scrapy
from sqlalchemy_utils import database_exists, create_database
from scrapy.pipelines.images import ImagesPipeline

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class Hotel(Base):
    """Module providing a function printing python version."""
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True)
    property_title = Column(String, unique=True)
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
        logger.info(f"Connecting to database: {self.database_url}")

        self.create_database_if_not_exists()

        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_database_if_not_exists(self):
        db_name = self.database_url.split('/')[-1]
        db_url_without_name = '/'.join(self.database_url.split('/')[:-1])

        if not database_exists(self.database_url):
            logger.info(f"Database {db_name} does not exist. Creating it now.")
            try:
                # Connect to default database
                conn = psycopg2.connect(db_url_without_name + '/postgres')
                conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                cur = conn.cursor()

                # Create the database
                cur.execute(f'CREATE DATABASE {db_name}')

                # Close communication with the database
                cur.close()
                conn.close()

                logger.info(f"Database {db_name} created successfully.")
            except (Exception, psycopg2.Error) as error:
                logger.error(f"Error while creating database: {error}")
        else:
            logger.info(f"Database {db_name} already exists.")

    def open_spider(self, spider):
        logger.info("Creating tables if they don't exist")
        Base.metadata.create_all(self.engine)

    def process_item(self, item, spider):
        logger.info(f"Processing item: {item['propertyTitle']}")
        session = self.Session()
        try:
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
            logger.info(f"Successfully added hotel: {item['propertyTitle']}")
        except Exception as e:
            logger.error(f"Error adding hotel to database: {str(e)}")
            session.rollback()
        finally:
            session.close()
        return item