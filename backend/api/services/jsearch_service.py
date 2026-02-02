"""
JSearch API Service
Handles on-demand job searches using JSearch API (RapidAPI)
Based on the working test_jsearch.py script
"""
import http.client
import json
import urllib.parse
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class JSearchService:
    """Service for searching jobs via JSearch API"""
    
    def __init__(self):
        self.api_key = os.getenv("X_RapidAPI_Key")
        self.host = "jsearch.p.rapidapi.com"
        
        if not self.api_key:
            raise ValueError("X_RapidAPI_Key not found in environment variables")
    
    def search_jobs(
        self,
        query: str,
        country: str = "in",
        remote_only: bool = False,
        date_posted: str = "week",
        page: int = 1,
        num_results: int = 10
    ) -> List[Dict]:
        """
        Search for jobs using JSearch API
        
        Args:
            query: Job title/keywords (e.g., "python developer")
            country: Country code (default: "in" for India)
            remote_only: Filter for remote jobs only
            date_posted: "today", "3days", "week", "month"
            page: Page number for pagination
            num_results: Number of results to return
            
        Returns:
            List of job dictionaries with normalized format
        """
        try:
            conn = http.client.HTTPSConnection(self.host)
            
            headers = {
                "x-rapidapi-key": self.api_key,
                "x-rapidapi-host": self.host
            }
            
            # Build search endpoint
            encoded_query = urllib.parse.quote(query)
            search_endpoint = (
                f"/search?"
                f"query={encoded_query}"
                f"&country={country}"
                f"&work_from_home={str(remote_only).lower()}"
                f"&date_posted={date_posted}"
                f"&page={page}"
            )
            
            # Make request
            print(f"[JSearch] Searching: {query} in {country}")
            print(f"[JSearch] Endpoint: {search_endpoint}")
            conn.request("GET", search_endpoint, headers=headers)
            res = conn.getresponse()
            print(f"[JSearch] Response status: {res.status}")
            search_data = res.read().decode("utf-8")
            search_result = json.loads(search_data)
            print(f"[JSearch] Response keys: {search_result.keys()}")
            
            jobs = search_result.get("data", [])
            print(f"[JSearch] API returned {len(jobs)} jobs")
            
            # Note: API already filters by country parameter, no need to filter again
            # Limit results
            jobs = jobs[:num_results]
            
            # Fetch detailed descriptions for each job
            enriched_jobs = []
            for job in jobs:
                try:
                    job_details = self._fetch_job_details(job["job_id"], country, conn, headers)
                    if job_details:
                        # Merge search result with detailed description
                        job.update(job_details)
                    enriched_jobs.append(job)
                except Exception as e:
                    print(f"Error fetching details for job {job.get('job_id')}: {e}")
                    # Still include job even if details fetch fails
                    enriched_jobs.append(job)
            
            conn.close()
            
            # Normalize to internal format
            normalized_jobs = [self._normalize_job(job) for job in enriched_jobs]
            filtered_jobs = [job for job in normalized_jobs if job]  # Filter out None values
            print(f"[JSearch] Returning {len(filtered_jobs)} normalized jobs")
            return filtered_jobs
            
        except Exception as e:
            print(f"JSearch API error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _fetch_job_details(
        self,
        job_id: str,
        country: str,
        conn: http.client.HTTPSConnection,
        headers: Dict
    ) -> Optional[Dict]:
        """
        Fetch detailed job description for a specific job
        
        Args:
            job_id: JSearch job ID
            country: Country code
            conn: Active HTTPS connection
            headers: Request headers
            
        Returns:
            Dictionary with job_description and other details
        """
        try:
            encoded_job_id = urllib.parse.quote(job_id)
            details_endpoint = f"/job-details?job_id={encoded_job_id}&country={country}"
            
            conn.request("GET", details_endpoint, headers=headers)
            res = conn.getresponse()
            details_data = res.read().decode("utf-8")
            details_result = json.loads(details_data)
            
            job_details_list = details_result.get("data", [])
            if job_details_list:
                return job_details_list[0]
            return None
            
        except Exception as e:
            print(f"Error fetching job details: {e}")
            return None
    
    def _normalize_job(self, api_job: Dict) -> Optional[Dict]:
        """
        Convert JSearch API format to internal Job model format
        
        Args:
            api_job: Raw job data from JSearch API
            
        Returns:
            Normalized job dictionary matching our database schema
        """
        try:
            # Extract fields
            job_id = api_job.get("job_id")
            title = api_job.get("job_title")
            company = api_job.get("employer_name")
            
            # Location
            city = api_job.get("job_city")
            country = api_job.get("job_country")
            location = f"{city}, {country}" if city and country else (country or city or "Remote")
            
            # Description (from details endpoint)
            description = api_job.get("job_description", "")
            
            # Apply link
            url = (
                api_job.get("job_apply_link") or 
                api_job.get("job_url") or 
                api_job.get("job_link")
            )
            
            # Salary
            min_sal = api_job.get("job_min_salary")
            max_sal = api_job.get("job_max_salary")
            currency = api_job.get("job_salary_currency", "USD")
            salary = None
            if min_sal and max_sal:
                salary = f"{min_sal}-{max_sal} {currency}"
            
            # Job type
            job_type = api_job.get("job_employment_type", "Full-time")
            
            # Remote flag
            is_remote = api_job.get("job_is_remote", False)
            
            # Required fields check
            if not title or not company:
                return None
            
            return {
                "job_id": f"jsearch_{job_id}",  # Prefix to avoid conflicts
                "title": title,
                "company": company,
                "location": location,
                "description_text": description,
                "description_html": description,  # JSearch returns text, duplicate it
                "url": url,
                "source": "jsearch_search",
                "salary": salary,
                "job_type": job_type,
                "tags": None,  # Will be extracted by JDParser
                "is_remote": is_remote
            }
            
        except Exception as e:
            print(f"Error normalizing job: {e}")
            return None
