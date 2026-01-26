# backend/api/routes/jobs.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from api.services.jsearch_service import JSearchService
from api.services.core_service import core_service
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from job_ingestion.database import SessionLocal
from job_ingestion.storage.models import Job as JobModel
from jd_parser.jd_parser import HybridJDParser

router = APIRouter(prefix="/api", tags=["Jobs"])

# Initialize services
jsearch_service = JSearchService()
jd_parser = HybridJDParser()

# Request/Response Models
class JobSearchRequest(BaseModel):
    query: str
    location: str = "in"  # Default to India
    remote_only: bool = False
    date_posted: str = "week"
    page: int = 1
    resume_data: Optional[dict] = None  # Optional: for immediate matching

class JobSearchResponse(BaseModel):
    jobs: List[dict]
    total: int
    page: int
    matched: bool = False  # True if matching was performed

@router.post("/search-jobs", response_model=JobSearchResponse)
async def search_jobs(request: JobSearchRequest):
    """
    Search for jobs using JSearch API
    
    Flow:
    1. Call JSearch API with search parameters
    2. Store new jobs in database
    3. Parse jobs with JDParser to extract skills
    4. (Optional) Match against resume if provided
    5. Return results
    """
    try:
        # Step 1: Search jobs via JSearch API
        print(f"Searching for: {request.query} in {request.location}")
        jobs_data = jsearch_service.search_jobs(
            query=request.query,
            country=request.location,
            remote_only=request.remote_only,
            date_posted=request.date_posted,
            page=request.page,
            num_results=10
        )
        
        if not jobs_data:
            return JobSearchResponse(
                jobs=[],
                total=0,
                page=request.page,
                matched=False
            )
        
        # Step 2: Store jobs in database
        db = SessionLocal()
        stored_count = 0
        
        try:
            for job_data in jobs_data:
                # Check if job already exists
                existing = db.query(JobModel).filter(
                    JobModel.job_id == job_data['job_id']
                ).first()
                
                if not existing:
                    # Parse job description to extract skills
                    try:
                        parsed_job = jd_parser.parse(job_data['description_text'])
                        # Store parsed skills as comma-separated tags
                        tags = ','.join(parsed_job.technical_skills) if parsed_job.technical_skills else None
                    except Exception as e:
                        print(f"Error parsing job {job_data['job_id']}: {e}")
                        tags = None
                    
                    # Create new job entry
                    new_job = JobModel(
                        job_id=job_data['job_id'],
                        title=job_data['title'],
                        company=job_data['company'],
                        location=job_data['location'],
                        description_text=job_data['description_text'],
                        description_html=job_data['description_html'],
                        url=job_data['url'],
                        source=job_data['source'],
                        salary=job_data.get('salary'),
                        job_type=job_data.get('job_type'),
                        tags=tags
                    )
                    db.add(new_job)
                    stored_count += 1
            
            db.commit()
            print(f"Stored {stored_count} new jobs in database")
            
        finally:
            db.close()
        
        # Step 3: Format response
        response_jobs = []
        for job_data in jobs_data:
            response_jobs.append({
                'id': job_data['job_id'],
                'title': job_data['title'],
                'company': job_data['company'],
                'location': job_data['location'],
                'salary': job_data.get('salary', 'Not specified'),
                'type': job_data.get('job_type', 'Full-time'),
                'url': job_data.get('url'),
                'description': job_data.get('description_text', '')[:200] + '...',
                'is_remote': job_data.get('is_remote', False)
            })
        
        # Step 4: (Optional) Match against resume if provided
        matched = False
        if request.resume_data:
            # Load jobs from cache and match
            try:
                # Reload jobs into core service cache
                core_service._load_sample_jobs()
                
                # Perform matching
                matched_jobs = core_service.match_resume_to_jobs(
                    request.resume_data,
                    specific_job_ids=[job['id'] for job in response_jobs]
                )
                
                # Update response with match scores
                for matched_job in matched_jobs:
                    for resp_job in response_jobs:
                        if resp_job['id'] == matched_job['id']:
                            resp_job['matchScore'] = matched_job.get('matchScore', 0)
                            resp_job['skills'] = matched_job.get('skills', [])
                            resp_job['missingSkills'] = matched_job.get('missingSkills', [])
                
                matched = True
            except Exception as e:
                print(f"Error during matching: {e}")
        
        return JobSearchResponse(
            jobs=response_jobs,
            total=len(response_jobs),
            page=request.page,
            matched=matched
        )
        
    except Exception as e:
        print(f"Search jobs error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Job search failed: {str(e)}"
        )
