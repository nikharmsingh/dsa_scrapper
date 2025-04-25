from .base_scraper import BaseScraper
import json
import time

class LeetCodeScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://leetcode.com"
        self.api_url = "https://leetcode.com/api/problems/all/"

    def get_problems(self):
        """Fetch all problems from LeetCode"""
        problems = []
        response = self._make_request(self.api_url)
        
        if response:
            try:
                data = json.loads(response)
                for problem in data['stat_status_pairs']:
                    if not problem['paid_only']:  # Only get free problems
                        problem_info = {
                            'title': problem['stat']['question__title'],
                            'platform': 'leetcode',
                            'difficulty': self._get_difficulty(problem['difficulty']['level']),
                            'url': f"{self.base_url}/problems/{problem['stat']['question__title_slug']}/",
                            'tags': []  # Tags will be fetched in get_problem_details
                        }
                        problems.append(problem_info)
            except json.JSONDecodeError as e:
                print(f"Error parsing LeetCode API response: {str(e)}")
        
        return problems

    def get_problem_details(self, problem_url):
        """Get detailed information about a specific problem"""
        # LeetCode's problem details are behind their GraphQL API
        # This is a simplified version - in a real implementation, you'd need to
        # handle their GraphQL API properly
        return {
            'description': 'Problem description would be fetched from GraphQL API',
            'tags': ['Array', 'String']  # Example tags
        }

    def _get_difficulty(self, level):
        """Convert numeric difficulty level to string"""
        difficulty_map = {
            1: 'Easy',
            2: 'Medium',
            3: 'Hard'
        }
        return difficulty_map.get(level, 'Unknown') 