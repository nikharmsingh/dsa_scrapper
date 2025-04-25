# DSA Problems Scraper

A Flask-based web application that scrapes and stores DSA (Data Structures and Algorithms) problems from various coding platforms.

## Table of Contents
- [Quick Start](#quick-start)
- [Supported Platforms](#supported-platforms)
- [Features](#features)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Development Guide](#development-guide)
- [Troubleshooting](#troubleshooting)

## Quick Start

1. **Clone and Setup**
```bash
git clone https://github.com/nikharmsingh/dsa_scrapper.git
cd dsa_scrapper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
# Copy example env file
cp .env.example .env

# Generate and set API key
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Edit .env and replace the API key placeholder
```

3. **Run Application**
```bash
python app.py
```

## Supported Platforms

1. **LeetCode**
   - Scrapes problem titles, difficulty levels, and tags
   - Fetches problem URLs and acceptance rates
   - Updates existing problems in the database

2. **Codeforces**
   - Scrapes problem titles and difficulty levels
   - Fetches problem URLs and tags
   - Updates existing problems in the database

## Features

- **RESTful API**
  - Get all problems
  - Get problems by platform
  - Trigger scraping process
  - Health check
  - Database statistics

- **Database Management**
  - SQLite storage
  - Automatic updates
  - Duplicate prevention
  - Platform categorization

## API Documentation

### Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /db-info` - Database statistics
- `GET /problems` - Get all problems
- `GET /problems/<platform>` - Get platform-specific problems
- `POST /scrape` - Trigger scraping

### Authentication
All endpoints except `/` and `/health` require API key authentication:
```bash
curl -H "X-API-Key: your_api_key_here" http://localhost:5000/endpoint
```

## Configuration

### Environment Variables
```env
# Required
INTERNAL_API_KEY=your_secure_random_key_here

# Optional
FLASK_ENV=development
FLASK_DEBUG=1
CACHE_TYPE=simple
CACHE_DEFAULT_TIMEOUT=300
RATE_LIMIT_PER_MINUTE=60
LOG_LEVEL=INFO
LOG_FILE=app.log
```

⚠️ **Security Notes:**
- Never commit or share your `.env` file
- Use different keys for development and production
- Keep API keys secure and private

## Development Guide

### Code Standards
- Follow PEP 8 style guide
- Add comments for complex logic
- Update documentation with changes

### Testing
- Test changes locally before committing
- Verify API endpoints
- Check scraper functionality

## Troubleshooting

### Common Issues

1. **Database Problems**
   - Check `instance/` directory for database file
   - Verify file permissions
   - Check for pending migrations

2. **API Authentication**
   - Verify API key in `.env`
   - Check request headers
   - Ensure key matches environment

3. **Scraper Issues**
   - Check network connectivity
   - Verify platform URLs
   - Review rate limits

### Getting Help
- Check the error logs in `app.log`
- Review the health check endpoint
- Verify environment configuration 