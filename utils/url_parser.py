import re
from urllib.parse import urlparse

def extract_problem_identifier(url):
    """
    Extract problem identifier from platform-specific URLs.
    
    Args:
        url (str): The problem URL
        
    Returns:
        tuple: (platform, identifier) or (None, None) if URL is invalid
    """
    try:
        # Remove any trailing slashes and whitespace
        url = url.strip().rstrip('/')
        parsed_url = urlparse(url)
        
        # Debug print
        print(f"Parsing URL: {url}")
        print(f"Netloc: {parsed_url.netloc}")
        print(f"Path: {parsed_url.path}")
        
        # LeetCode URL pattern: https://leetcode.com/problems/two-sum/
        if 'leetcode.com' in parsed_url.netloc:
            if '/problems/' in parsed_url.path:
                # Extract everything after /problems/
                parts = parsed_url.path.split('/problems/')
                if len(parts) > 1:
                    slug = parts[1].split('/')[0]  # Get the first part after /problems/
                    print(f"Extracted LeetCode slug: {slug}")
                    return 'leetcode', slug
        
        # Codeforces URL pattern: https://codeforces.com/problemset/problem/4/A
        elif 'codeforces.com' in parsed_url.netloc:
            if '/problemset/problem/' in parsed_url.path:
                parts = parsed_url.path.split('/problemset/problem/')[1].split('/')
                if len(parts) >= 2:
                    # Format: number/letter (e.g., 4/A)
                    identifier = f"{parts[0]}/{parts[1]}"
                    print(f"Extracted Codeforces identifier: {identifier}")
                    return 'codeforces', identifier
        
        print("URL format not recognized")
        return None, None
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None, None 