from scrapers.leetcode_scraper import LeetCodeScraper
from scrapers.codeforces_scraper import CodeforcesScraper
import time

class ScraperService:
    def __init__(self, leetcode_scraper, codeforces_scraper):
        self.leetcode_scraper = leetcode_scraper
        self.codeforces_scraper = codeforces_scraper

    def scrape_all_platforms(self, db, Problem):
        """Scrape problems from all platforms"""
        results = {}
        
        # Scrape LeetCode
        try:
            leetcode_problems = self.leetcode_scraper.get_problems()
            leetcode_results = self._process_problems(db, Problem, leetcode_problems, 'leetcode')
            results['leetcode'] = leetcode_results
        except Exception as e:
            results['leetcode'] = {
                'total': 0,
                'new': 0,
                'updated': 0,
                'errors': [str(e)]
            }
        
        # Scrape Codeforces
        try:
            codeforces_problems = self.codeforces_scraper.get_problems()
            codeforces_results = self._process_problems(db, Problem, codeforces_problems, 'codeforces')
            results['codeforces'] = codeforces_results
        except Exception as e:
            results['codeforces'] = {
                'total': 0,
                'new': 0,
                'updated': 0,
                'errors': [str(e)]
            }
        
        return results

    def _process_problems(self, db, Problem, problems, platform):
        """Process and store problems in the database"""
        total = len(problems)
        new = 0
        updated = 0
        errors = []
        
        print(f"\nProcessing {total} problems for {platform}")
        
        for problem in problems:
            try:
                # Get problem data with defaults for missing fields
                problem_data = {
                    'title': problem.get('title', ''),
                    'difficulty': problem.get('difficulty', 'Unknown'),
                    'url': problem.get('url', ''),
                    'points': problem.get('points', '0'),
                    'tags': problem.get('tags', [])
                }
                
                print(f"\nProcessing problem: {problem_data['title']}")
                
                # Check if problem already exists
                existing_problem = Problem.query.filter_by(
                    platform=platform,
                    title=problem_data['title']
                ).first()
                
                if existing_problem:
                    print(f"Updating existing problem: {problem_data['title']}")
                    # Update existing problem
                    existing_problem.difficulty = problem_data['difficulty']
                    existing_problem.url = problem_data['url']
                    existing_problem.points = problem_data['points']
                    existing_problem.tags = ','.join(problem_data['tags'])
                    updated += 1
                else:
                    print(f"Adding new problem: {problem_data['title']}")
                    # Create new problem
                    new_problem = Problem(
                        title=problem_data['title'],
                        platform=platform,
                        difficulty=problem_data['difficulty'],
                        url=problem_data['url'],
                        points=problem_data['points'],
                        tags=','.join(problem_data['tags'])
                    )
                    db.session.add(new_problem)
                    new += 1
                
            except Exception as e:
                error_msg = f"Error processing problem {problem.get('title', 'Unknown')}: {str(e)}"
                print(error_msg)
                errors.append(error_msg)
                continue
        
        # Commit changes to database
        try:
            print(f"\nCommitting changes to database for {platform}")
            print(f"New problems: {new}")
            print(f"Updated problems: {updated}")
            db.session.commit()
            print("Database commit successful")
        except Exception as e:
            error_msg = f"Database commit error: {str(e)}"
            print(error_msg)
            errors.append(error_msg)
            db.session.rollback()
            print("Database changes rolled back")
        
        return {
            'total': total,
            'new': new,
            'updated': updated,
            'errors': errors
        }

    def get_problems_by_platform(self, db, Problem, platform):
        """Get all problems from a specific platform"""
        return Problem.query.filter_by(platform=platform).all()

    def get_all_problems(self, db, Problem):
        """Get all problems from all platforms"""
        return Problem.query.all() 