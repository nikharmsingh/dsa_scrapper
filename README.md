# DSA Problems Scraper

A Flask-based web application that scrapes Data Structures and Algorithms problems from various platforms.

## Features

- Scrapes DSA problems from multiple platforms (currently supports LeetCode)
- Stores problems in a SQLite database
- RESTful API endpoints to access the problems
- Easy to extend with new platform scrapers

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. The server will start at `http://localhost:5000`

## API Endpoints

- `GET /`: Welcome message
- `GET /problems`: Get all problems from all platforms
- `GET /problems/<platform>`: Get problems from a specific platform
- `POST /scrape`: Trigger scraping of problems from all platforms

## Adding New Platform Scrapers

1. Create a new scraper class in the `scrapers` directory that inherits from `BaseScraper`
2. Implement the required methods:
   - `get_problems()`
   - `get_problem_details()`
3. Add the new scraper to the `ScraperService` class in `services/scraper_service.py`

## Note

Please be mindful of the platforms' terms of service and rate limits when scraping. The application includes delays between requests to be respectful to the servers. 