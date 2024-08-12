# Hotel Scraper

This project is a web scraper built with Scrapy for gathering hotel property information from [https://uk.trip.com](https://uk.trip.com/hotels/?locale=en-GB&curr=GBP). The scraped data is stored in a PostgreSQL database using SQLAlchemy, with images saved to a designated directory. The database and table will be automatically created if they do not exist.

- [Description](#description)
- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Running the Scraper](#running-the-scraper)
- [Database Schema](#database-schema)
- [Contributing](#contributing)

## Description

The scraper collects hotel property information including title, rating, location, latitude, longitude, room type, price, and images. The data is stored in a PostgreSQL database, and images are saved to a specified directory. The database and necessary tables will be created automatically.

## Features

1. Uses Scrapy for web scraping
2. Stores hotel data in a PostgreSQL database with SQLAlchemy
3. Automatically creates the database and tables if they do not exist
4. Saves images to a directory and stores image path references in the database

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nthalt/scrapy.git
   cd scrapy
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a file named `.env` in the project root and add your PostgreSQL database connection details. Use `.env.example` as a reference:

   ```bash
   cp .env.example .env
   ```

5. Make sure Postgresql database engine is installed and running.

6. Move to the project directory
   ```bash
   cd hotel_scraper
   ```

## Running the Scraper

To start the scraper, use the following command:

```bash
scrapy crawl hotel
```

The scraper will collect hotel data from the specified URLs and store the information in the PostgreSQL database. The database and tables will be created automatically. Images will be saved in the `images/` directory inside the current directory.

## Troubleshooting

Only if the database is not automatically created, please create the database manually.

```bash
CREATE DATABASE your_database_name;
```

## Database Schema

#### Table "hotels"

| Column         | Type                | Collation | Nullable | Default                            |
| -------------- | ------------------- | --------- | -------- | ---------------------------------- |
| id             | integer             |           | not null | nextval('hotels_id_seq'::regclass) |
| property_title | character varying   |           |          |                                    |
| rating         | double precision    |           |          |                                    |
| location       | character varying   |           |          |                                    |
| latitude       | double precision    |           |          |                                    |
| longitude      | double precision    |           |          |                                    |
| room_type      | character varying[] |           |          |                                    |
| price          | double precision    |           |          |                                    |
| img            | character varying   |           |          |                                    |

#### Indexes:

- "hotels_pkey" PRIMARY KEY, btree (id)
- "hotels_property_title_key" UNIQUE CONSTRAINT, btree (property_title)

<details>
<summary>

## Contributing

</summary>

We welcome contributions to this project. To ensure a smooth collaboration, please follow these guidelines:

1. **Fork the Repository**: Start by forking the repository on GitHub.

2. **Clone the Repository**: Clone your forked repository to your local machine using:

   ```bash
   git clone https://github.com/username/scrapy.git
   ```

3. **Create a Branch**: Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature-or-bugfix-description
   ```

4. **Make Changes**: Implement your changes in the codebase. Ensure your code adheres to the project's coding standards and includes appropriate tests.

5. **Commit Changes**: Commit your changes with a clear and descriptive commit message:

   ```bash
   git add .
   git commit -m "Description of the feature or bug fix"
   ```

6. **Push to GitHub**: Push your branch to your forked repository on GitHub:

   ```bash
   git push origin feature-or-bugfix-description
   ```

7. **Create a Pull Request**: Go to the original repository on GitHub and create a pull request. Provide a clear and detailed description of your changes.

8. **Review Process**: Wait for the project maintainers to review your pull request. Be prepared to make any necessary changes based on feedback.

Thank you for your contributions! Your help is greatly appreciated.

</details>
