# DSA Problems Scraper

A Flask-based web application that scrapes and stores DSA (Data Structures and Algorithms) problems from various coding platforms.

## Instructions for Others

### Quick Start Guide

1. **Clone the Repository**
```bash
git clone https://github.com/nikharmsingh/dsa_scrapper.git
cd dsa_scrapper
```

2. **Set Up Environment**
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

3. **Generate and Set API Key**
```bash
# Generate a secure API key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Edit .env and replace the API key placeholder with your generated key
```

4. **Run the Application**
```bash
python app.py
```

### Making API Requests

Use the API key in your requests:
```bash
# Health check
curl http://localhost:5000/health \
  -H "X-API-Key: your_api_key_here"

# Get all problems
curl http://localhost:5000/problems \
  -H "X-API-Key: your_api_key_here"

# Trigger scraping
curl -X POST http://localhost:5000/scrape \
  -H "X-API-Key: your_api_key_here"
```

### Development Guidelines

1. **Environment Setup**
   - Always use a virtual environment
   - Keep your `.env` file secure and private
   - Never commit `.env` to version control

2. **API Key Security**
   - Generate a unique API key for your development
   - Use different keys for development and production
   - Keep your API keys secure

3. **Code Contributions**
   - Follow PEP 8 style guide
   - Add comments for complex logic
   - Update documentation when making changes

4. **Testing**
   - Test your changes locally before committing
   - Verify API endpoints after modifications
   - Check scraper functionality

### Troubleshooting

1. **Database Issues**
   - Check if the database file exists in `instance/`
   - Verify database permissions
   - Check for any pending migrations

2. **API Authentication**
   - Verify your API key is correct
   - Check the `X-API-Key` header in requests
   - Ensure the key matches your `.env` file

3. **Scraper Problems**
   - Check network connectivity
   - Verify platform URLs are accessible
   - Review rate limiting settings

## Configuration

### Environment Setup

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file and set your own values:
```bash
# Required: Generate a secure API key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

3. Update the following in your `.env`:
   - `INTERNAL_API_KEY`: Use the generated secure key
   - Other values can remain as default for development

⚠️ **Important Security Notes:**
- Never commit or share your actual `.env` file
- Keep your API keys secure and private
- Use different keys for development and production
- The `.env` file is already in `.gitignore` for security

### Environment Variables

The application uses the following environment variables:

```env
# Internal Service API Key (Required)
INTERNAL_API_KEY=your_secure_random_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1

# Cache Configuration
CACHE_TYPE=simple
CACHE_DEFAULT_TIMEOUT=300

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

The `INTERNAL_API_KEY` is required for:
- Triggering the scraping process
- Accessing protected endpoints
- Internal service communication

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
- `POST /scrape` - Trigger scraping process (requires API key)

### API Key Usage

To use protected endpoints, include the API key in the request header:

```bash
# Example: Trigger scraping with API key
curl -X POST http://localhost:5000/scrape \
  -H "X-API-Key: your_secret_key_here"

# Example: Get database info with API key
curl http://localhost:5000/db-info \
  -H "X-API-Key: your_secret_key_here"
```

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

4. Create `.env` file with your API key:
```bash
echo "INTERNAL_API_KEY=your_secret_key_here" > .env
```

5. Run the application:
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