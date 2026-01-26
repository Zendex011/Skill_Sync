import requests
import sys
import os
from typing import List, Dict, Optional
from datetime import datetime

# Add project root to path to allow importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import RAPIDAPI_KEY, RAPIDAPI_HOST, RAPIDAPI_URL, REQUEST_TIMEOUT

class RapidAPIClient:
    """Client for fetching jobs from RapidAPI (JSearch)"""
    
    def __init__(self):
        self.api_url = RAPIDAPI_URL
        self.headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }
        
    def fetch_jobs(self, query: str = "Software Developer", num_pages: int = 1) -> List[Dict]:
        """
        Fetch jobs from JSearch API
        """
        if not RAPIDAPI_KEY:
            print("Error: X-RapidAPI-Key not found in environment variables.")
            return []
            
        all_jobs = []
        
        for page in range(1, num_pages + 1):
            try:
                querystring = {"query": query, "page": str(page), "num_pages": "1"}
                
                print(f"Fetching page {page} from RapidAPI (JSearch)...")
                response = requests.get(
                    self.api_url, 
                    headers=self.headers, 
                    params=querystring,
                    timeout=REQUEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    data = response.json()
                    jobs_data = data.get('data', [])
                    print(f"  Found {len(jobs_data)} jobs on page {page}.")
                    
                    for job_data in jobs_data:
                        normalized_job = self.normalize_job(job_data)
                        if normalized_job:
                            all_jobs.append(normalized_job)
                else:
                    print(f"  Failed to fetch: {response.status_code} - {response.text}")
                    break
                    
            except Exception as e:
                print(f"  Error fetching from RapidAPI: {e}")
                
        return all_jobs
    
    def normalize_job(self, api_job: Dict) -> Optional[Dict]:
        """
        Convert JSearch API job format to our internal Job model dict
        """
        try:
            # JSearch structure mapping
            job_id = api_job.get('job_id')
            title = api_job.get('job_title')
            company = api_job.get('employer_name')
            description = api_job.get('job_description')
            url = api_job.get('job_apply_link')
            
            # Location construction
            city = api_job.get('job_city')
            country = api_job.get('job_country')
            location = f"{city}, {country}" if city and country else (country or city or "Remote")
            
            # Salary construction (if available)
            min_sal = api_job.get('job_min_salary')
            max_sal = api_job.get('job_max_salary')
            currency = api_job.get('job_salary_currency', 'USD')
            salary = None
            if min_sal and max_sal:
                salary = f"{min_sal}-{max_sal} {currency}"
            
            # Job Type
            job_type = api_job.get('job_employment_type', 'Full-time')
            
            # Extract required fields
            if not title or not company:
                return None
                
            return {
                "job_id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "description_text": description,
                "description_html": description, # JSearch usually returns text, duplicate it
                "url": url,
                "source": "rapidapi_jsearch",
                "salary": salary,
                "job_type": job_type,
                "tags": None # Will need parsing later
            }
        except Exception as e:
            print(f"Error normalizing job: {e}")
            return None
