from .base_scraper import BaseScraper
import requests
import time
import logging

class CodeforcesScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://codeforces.com"
        self.api_url = "https://codeforces.com/api/problemset.problems"
        self.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_problems(self):
        """Fetch problems from Codeforces using their API"""
        problems = []
        print("Fetching problems from Codeforces API...")
        
        try:
            # Make direct API request
            response = requests.get(self.api_url, headers=self.headers)
            print(f"API Response Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"API request failed with status code: {response.status_code}")
                return problems
                
            data = response.json()
            print(f"API Response Status: {data.get('status')}")
            
            if data['status'] != 'OK':
                print(f"API returned error: {data.get('comment', 'Unknown error')}")
                return problems
            
            # Log the structure of the response
            print(f"Number of problems in response: {len(data['result']['problems'])}")
            print(f"Number of problem statistics: {len(data['result']['problemStatistics'])}")
            
            # Process problems
            for problem in data['result']['problems']:
                try:
                    # Get problem statistics
                    problem_stats = next(
                        (stats for stats in data['result']['problemStatistics'] 
                         if stats['contestId'] == problem['contestId'] and stats['index'] == problem['index']),
                        None
                    )
                    
                    # Skip problems without a name
                    if not problem.get('name'):
                        print(f"Skipping problem without name: {problem}")
                        continue
                        
                    solved_count = str(problem_stats['solvedCount']) if problem_stats else '0'
                    rating = str(problem['rating']) if 'rating' in problem else 'Unknown'
                    
                    # Create problem info
                    problem_info = {
                        'title': f"{problem['contestId']}{problem['index']} - {problem['name']}",
                        'platform': 'codeforces',
                        'difficulty': rating,
                        'url': f"{self.base_url}/problemset/problem/{problem['contestId']}/{problem['index']}",
                        'points': solved_count,
                        'tags': problem.get('tags', [])
                    }
                    
                    # Add to problems list
                    problems.append(problem_info)
                    print(f"Found problem: {problem_info['title']}")
                    
                except Exception as e:
                    print(f"Error processing problem: {str(e)}")
                    print(f"Problem data: {problem}")
                    continue
            
            print(f"Total problems found: {len(problems)}")
            return problems
            
        except Exception as e:
            print(f"Error fetching problems from API: {str(e)}")
            return problems

    def get_problem_details(self, problem_url):
        """Get detailed information about a specific problem"""
        print(f"Fetching details for: {problem_url}")
        details = {
            'description': '',
            'tags': []
        }
        
        try:
            # Extract contest ID and problem index from URL
            parts = problem_url.split('/')
            contest_id = parts[-2]
            problem_index = parts[-1]
            
            # Get problem details from API
            api_url = f"{self.api_url}?tags={contest_id}{problem_index}"
            response = requests.get(api_url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK' and data['result']['problems']:
                    problem = data['result']['problems'][0]
                    details['tags'] = problem.get('tags', [])
                    
                    # Get problem statement from the website
                    html_response = requests.get(problem_url, headers=self.headers)
                    if html_response.status_code == 200:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(html_response.text, 'html.parser')
                        statement_div = soup.find('div', class_='problem-statement')
                        if statement_div:
                            description_paragraphs = statement_div.find_all('div', class_=None)
                            if description_paragraphs:
                                details['description'] = description_paragraphs[0].text.strip()
        
        except Exception as e:
            print(f"Error fetching problem details: {str(e)}")
        
        return details 