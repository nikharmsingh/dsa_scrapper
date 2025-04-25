from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from scrapers.leetcode_scraper import LeetCodeScraper
from scrapers.codeforces_scraper import CodeforcesScraper
from services.scraper_service import ScraperService
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from environment
INTERNAL_API_KEY = os.getenv('INTERNAL_API_KEY')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != INTERNAL_API_KEY:
            return jsonify({
                'status': 'error',
                'message': 'Invalid or missing API key'
            }), 401
        return f(*args, **kwargs)
    return decorated_function

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Configure SQLite database
db_path = os.path.join(app.instance_path, 'dsa_problems.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure caching
app.config['CACHE_TYPE'] = 'simple'  # Use simple in-memory cache
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds (5 minutes)

# Initialize extensions
db = SQLAlchemy(app)
cache = Cache(app)

def init_db():
    """Initialize the database"""
    with app.app_context():
        # Check if database already exists
        if os.path.exists(db_path):
            print("\nDatabase already exists at:", db_path)
            print(f"Current size: {os.path.getsize(db_path)} bytes")
            return
        
        print("\nInitializing database...")
        print(f"Database path: {db_path}")
        
        # Create all tables
        db.create_all()
        
        # Verify database creation
        if os.path.exists(db_path):
            print("Database created successfully")
            print(f"Database size: {os.path.getsize(db_path)} bytes")
        else:
            print("Error: Database file not created")
        
        print("Database initialization complete\n")

# Models
class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50))
    url = db.Column(db.String(200))
    points = db.Column(db.String(50))
    tags = db.Column(db.String(200))

# Initialize scrapers
leetcode_scraper = LeetCodeScraper()
codeforces_scraper = CodeforcesScraper()

# Initialize scraper service
scraper_service = ScraperService(
    leetcode_scraper,
    codeforces_scraper
)

def get_db_stats():
    """Get database statistics and information"""
    stats = {}
    
    # Get database size
    if os.path.exists(db_path):
        stats['size_bytes'] = os.path.getsize(db_path)
        stats['size_mb'] = round(stats['size_bytes'] / (1024 * 1024), 2)
    
    # Get total number of problems
    stats['total_problems'] = Problem.query.count()
    
    # Get problems by platform
    platforms = ['leetcode', 'codeforces']
    problems_by_platform = {}
    for platform in platforms:
        count = Problem.query.filter_by(platform=platform).count()
        problems_by_platform[platform] = count
    stats['problems_by_platform'] = problems_by_platform
    
    # Get problems by difficulty
    difficulties = Problem.query.with_entities(Problem.difficulty, db.func.count(Problem.id)).group_by(Problem.difficulty).all()
    stats['problems_by_difficulty'] = {diff: count for diff, count in difficulties if diff}
    
    # Get database last modified time
    if os.path.exists(db_path):
        stats['last_modified'] = datetime.fromtimestamp(os.path.getmtime(db_path)).isoformat()
    
    # Get database schema info
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table info
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    stats['tables'] = [table[0] for table in tables]
    
    # Get Problem table columns
    cursor.execute("PRAGMA table_info(problem);")
    columns = cursor.fetchall()
    stats['problem_table_columns'] = [col[1] for col in columns]
    
    conn.close()
    
    return stats

# Routes
@app.route('/')
def index():
    return jsonify({'message': 'DSA Problems Scraper API'})

@app.route('/health', methods=['GET'])
def health_check():
    """Check the health of the application and database"""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'application': 'up',
            'database': 'up'
        }
    }
    
    try:
        # Check database connection
        db.session.execute('SELECT 1')
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['components']['database'] = 'down'
    
    return jsonify(health_status)

@app.route('/db-info', methods=['GET'])
@require_api_key
def get_db_info():
    """Get database statistics and information"""
    try:
        stats = get_db_stats()
        return jsonify({
            'status': 'success',
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/problems', methods=['GET'])
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_problems():
    """Get all problems from the database"""
    try:
        problems = Problem.query.all()
        return jsonify({
            'status': 'success',
            'count': len(problems),
            'problems': [{
                'id': p.id,
                'title': p.title,
                'platform': p.platform,
                'difficulty': p.difficulty,
                'url': p.url,
                'points': p.points,
                'tags': p.tags.split(',') if p.tags else []
            } for p in problems]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/problems/<platform>', methods=['GET'])
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_problems_by_platform(platform):
    """Get problems by platform"""
    try:
        problems = Problem.query.filter_by(platform=platform).all()
        return jsonify({
            'status': 'success',
            'count': len(problems),
            'problems': [{
                'id': p.id,
                'title': p.title,
                'platform': p.platform,
                'difficulty': p.difficulty,
                'url': p.url,
                'points': p.points,
                'tags': p.tags.split(',') if p.tags else []
            } for p in problems]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/scrape', methods=['POST'])
@require_api_key
def scrape_problems():
    """Trigger scraping of problems from all platforms"""
    try:
        # Clear cache before scraping
        cache.clear()
        
        # Scrape problems
        results = scraper_service.scrape_all_platforms(db, Problem)
        
        # Prepare response
        response = {
            'status': 'success',
            'message': 'Scraping completed successfully',
            'results': {}
        }
        
        # Add results for each platform
        for platform, result in results.items():
            response['results'][platform] = {
                'total': result.get('total', 0),
                'new': result.get('new', 0),
                'updated': result.get('updated', 0),
                'errors': result.get('errors', [])
            }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Initialize database only when running the app directly
    init_db()
    
    # Run the app
    app.run(debug=True) 