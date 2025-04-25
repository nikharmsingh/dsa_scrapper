from .base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup
import time
import logging

class GFGScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://practice.geeksforgeeks.org"
        self.problems_url = "https://practice.geeksforgeeks.org/explore"
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        })

    def get_problems(self):
        """Fetch problems from GeeksforGeeks practice section"""
        problems = []
        page = 1
        max_pages = 5  # Limit the number of pages to scrape initially
        
        while page <= max_pages:
            url = f"{self.problems_url}?page={page}"
            print(f"Fetching page {page} from GeeksforGeeks...")
            
            try:
                response = requests.get(url, headers=self.headers)
                if response.status_code != 200:
                    print(f"Failed to fetch page {page}: Status code {response.status_code}")
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all problem links
                problem_links = soup.find_all('a', class_='problem-title')
                if not problem_links:
                    print("No problems found on page")
                    break
                
                for link in problem_links:
                    try:
                        title = link.get_text(strip=True)
                        problem_url = self.base_url + link['href']
                        
                        # Get problem details
                        problem_info = self.get_problem_details(problem_url)
                        
                        # Add problem to list
                        problems.append({
                            'title': title,
                            'platform': 'geeksforgeeks',
                            'difficulty': problem_info.get('difficulty', 'Unknown'),
                            'url': problem_url,
                            'points': problem_info.get('points', '0'),
                            'tags': problem_info.get('tags', [])
                        })
                        
                        print(f"Found problem: {title}")
                        
                        # Add delay between problem requests
                        time.sleep(2)
                        
                    except Exception as e:
                        print(f"Error processing problem: {str(e)}")
                        continue
                
                # Add delay between pages
                time.sleep(3)
                page += 1
                
            except Exception as e:
                print(f"Error fetching page {page}: {str(e)}")
                break
        
        print(f"Total problems found: {len(problems)}")
        return problems

    def get_problem_details(self, problem_url):
        """Get detailed information about a specific problem"""
        print(f"Fetching details for: {problem_url}")
        details = {
            'difficulty': 'Unknown',
            'points': '0',
            'tags': []
        }
        
        try:
            response = requests.get(problem_url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find difficulty
                difficulty_elem = soup.find('span', class_='problem-difficulty')
                if difficulty_elem:
                    details['difficulty'] = difficulty_elem.text.strip()
                
                # Find tags
                tags_div = soup.find('div', class_='problem-tags')
                if tags_div:
                    tag_links = tags_div.find_all('a')
                    details['tags'] = [tag.text.strip() for tag in tag_links]
                
                # Find solved count
                solved_elem = soup.find('div', class_='solved-count')
                if solved_elem:
                    solved_text = solved_elem.text.strip()
                    # Extract number from text like "Solved by 1234 users"
                    import re
                    match = re.search(r'\d+', solved_text)
                    if match:
                        details['points'] = match.group()
        
        except Exception as e:
            print(f"Error fetching problem details: {str(e)}")
        
        return details 