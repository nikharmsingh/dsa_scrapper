# DSA Problems Scraper

A Flask-based web application that scrapes and stores DSA (Data Structures and Algorithms) problems from various coding platforms.

## Supported Platforms

Currently, the scraper supports the following platforms:

1. **LeetCode**
   - Scrapes problem titles, difficulty levels, and tags
   - Fetches problem URLs and acceptance rates
   - Updates existing problems in the database

2. **Codeforces**
   - Scrapes problem titles and difficulty levels
   - Fetches problem URLs and tags
   - Updates existing problems in the database

## Features

- RESTful API endpoints for:
  - Getting all problems
  - Getting problems by platform
  - Triggering scraping process
  - Checking application health
  - Viewing database statistics

- Database Features:
  - SQLite database for problem storage
  - Automatic problem updates
  - Duplicate prevention
  - Problem categorization by platform and difficulty

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check for application and database
- `GET /db-info` - Database statistics and information
- `GET /problems` - Get all problems
- `GET /problems/<platform>` - Get problems by platform
- `POST /scrape` - Trigger scraping process

## Setup

1. Clone the repository:
```bash
git clone https://github.com/nikharmsingh/dsa_scrapper.git
cd dsa_scrapper
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

## Usage

1. Start the Flask application
2. Access the API endpoints:
   - Health check: `curl http://localhost:5000/health`
   - Get all problems: `curl http://localhost:5000/problems`
   - Scrape problems: `curl -X POST http://localhost:5000/scrape`

## Database Schema

The application uses a SQLite database with the following schema:

```sql
CREATE TABLE problem (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    difficulty VARCHAR(50),
    url VARCHAR(200),
    points VARCHAR(50),
    tags VARCHAR(200)
);
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License. 