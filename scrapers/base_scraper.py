from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

class BaseScraper(ABC):
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    @abstractmethod
    def get_problems(self):
        """Fetch problems from the platform"""
        pass

    @abstractmethod
    def get_problem_details(self, problem_url):
        """Get detailed information about a specific problem"""
        pass

    def _make_request(self, url):
        """Make HTTP request with error handling"""
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def _parse_html(self, html_content):
        """Parse HTML content using BeautifulSoup"""
        if html_content:
            return BeautifulSoup(html_content, 'html.parser')
        return None 