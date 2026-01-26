import requests
import logging
from typing import List, Dict
import logging
from typing import List, Dict
from job_ingestion.config import REMOTIVE_API_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class RemotiveClient:
    """Client for fetching jobs from Remotive API"""
    
    def fetch_jobs(self, limit: int = 50) -> List[Dict]:
        """
        Fetch latest jobs from Remotive.
        
        Args:
            limit: Max jobs to return (Remotive returns all, we slice locally)
            
        Returns:
            List of job dictionaries
        """
        # Headers to mimic a real browser and bypass Cloudflare
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://remotive.io/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }
        
        try:
            logger.info("Fetching jobs from Remotive...")
            response = requests.get(REMOTIVE_API_URL, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get("jobs", [])
            
            logger.info(f"Retrieved {len(jobs)} jobs from API")
            
            # Sort by publication date if needed, or just take first N
            # Remotive sorts by date descending by default
            return jobs[:limit]
            
        except Exception as e:
            logger.error(f"Error fetching from Remotive: {e}")
            return []

    def normalize_job(self, raw_job: Dict) -> Dict:
        """Convert Remotive format to internal Job model format"""
        return {
            "job_id": str(raw_job.get("id")),
            "title": raw_job.get("title"),
            "company": raw_job.get("company_name", "Unknown"),
            "location": raw_job.get("candidate_required_location", "Remote"),
            "description_html": raw_job.get("description"),
            "url": raw_job.get("url"),
            "source": "remotive",
            "salary": raw_job.get("salary", ""),
            "job_type": raw_job.get("job_type", "full_time"),
            "tags": ",".join(raw_job.get("tags", []))
        }
