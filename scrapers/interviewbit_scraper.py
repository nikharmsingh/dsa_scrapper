from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re
import time

class InterviewBitScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.interviewbit.com"
        self.arrays_url = "https://www.interviewbit.com/courses/programming/arrays/"
        # Add authentication headers if needed
        self.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })

    def get_problems(self):
        """Fetch array problems from InterviewBit"""
        problems = []
        response = self._make_request(self.arrays_url)
        
        if response:
            soup = self._parse_html(response)
            if soup:
                # Try different possible selectors for problem sections
                problem_sections = (
                    soup.find_all('div', class_='problem-section') or
                    soup.find_all('div', class_='problem') or
                    soup.find_all('div', class_='question')
                )
                
                for section in problem_sections:
                    try:
                        # Try different possible selectors for title
                        title_elem = (
                            section.find('a', class_='problem-title') or
                            section.find('a', class_='question-title') or
                            section.find('h3')
                        )
                        
                        if title_elem:
                            title = title_elem.text.strip()
                            url = self.base_url + title_elem.get('href', '')
                            
                            # Try different possible selectors for difficulty
                            difficulty_elem = (
                                section.find('span', class_='difficulty') or
                                section.find('span', class_='level') or
                                section.find('div', class_='difficulty')
                            )
                            difficulty = difficulty_elem.text.strip() if difficulty_elem else 'Unknown'
                            
                            # Try different possible selectors for points
                            points_elem = (
                                section.find('span', class_='points') or
                                section.find('span', class_='score') or
                                section.find('div', class_='points')
                            )
                            points = points_elem.text.strip() if points_elem else '0'
                            
                            problem_info = {
                                'title': title,
                                'platform': 'interviewbit',
                                'difficulty': difficulty,
                                'url': url,
                                'points': points,
                                'tags': ['Arrays']  # Default tag for array problems
                            }
                            problems.append(problem_info)
                            
                            # Add delay between requests to be respectful
                            time.sleep(1)
                    except Exception as e:
                        print(f"Error processing problem section: {str(e)}")
                        continue
        
        return problems

    def get_problem_details(self, problem_url):
        """Get detailed information about a specific problem"""
        response = self._make_request(problem_url)
        details = {
            'description': '',
            'tags': ['Arrays']
        }
        
        if response:
            soup = self._parse_html(response)
            if soup:
                # Try different possible selectors for description
                description_elem = (
                    soup.find('div', class_='problem-description') or
                    soup.find('div', class_='question-description') or
                    soup.find('div', class_='content')
                )
                if description_elem:
                    details['description'] = description_elem.text.strip()
                
                # Try different possible selectors for tags
                tags_elem = (
                    soup.find('div', class_='problem-tags') or
                    soup.find('div', class_='question-tags') or
                    soup.find('div', class_='tags')
                )
                if tags_elem:
                    tags = [tag.text.strip() for tag in tags_elem.find_all('a')]
                    details['tags'].extend(tags)
        
        return details 