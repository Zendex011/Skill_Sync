import re
import logging
import re
import logging
from job_ingestion.ingestion.remotive_client import RemotiveClient
from job_ingestion.ingestion.alternative_client import AlternativeJobClient
from job_ingestion.storage.models import Job
from job_ingestion.database import SessionLocal, init_db
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from job_ingestion.ingestion.rapidapi_client import RapidAPIClient

class JobFetcher:
    def __init__(self):
        self.remotive = RemotiveClient()
        self.rapidapi = RapidAPIClient()
        self.alternative = AlternativeJobClient()
        
    def clean_html(self, raw_html: str) -> str:
        """Strip HTML tags using regex for minimal dependencies"""
        if not raw_html:
            return ""
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, ' ', raw_html)
        return " ".join(cleantext.split())

    def save_jobs(self, db: Session, jobs_data: list):
        """Save jobs to DB, skipping duplicates"""
        count = 0
        for job_data in jobs_data:
            # Check for existing
            existing = db.query(Job).filter(Job.job_id == job_data['job_id']).first()
            if existing:
                continue
            
            # Create new
            cleaned_text = self.clean_html(job_data['description_html'])
            
            new_job = Job(
                job_id=job_data['job_id'],
                title=job_data['title'],
                company=job_data['company'],
                location=job_data['location'],
                description_html=job_data['description_html'],
                description_text=cleaned_text,
                url=job_data['url'],
                source=job_data['source'],
                salary=job_data['salary'],
                job_type=job_data['job_type'],
                tags=job_data['tags']
            )
            db.add(new_job)
            count += 1
        
        db.commit()
        logger.info(f"Saved {count} new jobs")

    def run(self):
        """Main execution flow"""
        init_db()
        db = SessionLocal()
        
        try:
            combined_jobs = []

            # 1. Fetch from RapidAPI (JSearch)
            logger.info("Fetching from RapidAPI...")
            try:
                rapid_jobs = self.rapidapi.fetch_jobs()
                combined_jobs.extend(rapid_jobs)
            except Exception as e:
                logger.error(f"RapidAPI failed: {e}")

            # 2. Fetch from Remotive
            logger.info("Fetching from Remotive API...")
            try:
                raw_remotive = self.remotive.fetch_jobs()
                norm_remotive = [self.remotive.normalize_job(j) for j in raw_remotive]
                combined_jobs.extend(norm_remotive)
            except Exception as e:
                logger.error(f"Remotive failed: {e}")
            
            # 3. Fallback or Save
            if not combined_jobs:
                logger.warning("All APIs returned no jobs, using alternative source...")
                raw_jobs = self.alternative.fetch_jobs()
                combined_jobs = [self.alternative.normalize_job(j) for j in raw_jobs]
            
            # 4. Save
            self.save_jobs(db, combined_jobs)
            
        except Exception as e:
            logger.error(f"Ingestion run failed: {e}")
        finally:
            db.close()
            

