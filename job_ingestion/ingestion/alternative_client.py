"""
Alternative job source using Adzuna API (free tier available)
or creating sample jobs for testing
"""
import requests
import logging
from typing import List, Dict
from job_ingestion.config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class AlternativeJobClient:
    """Fallback client that creates sample jobs for testing"""
    
    def fetch_jobs(self, limit: int = 50) -> List[Dict]:
        """
        Generate sample jobs for testing purposes.
        Replace this with a real API when you have access.
        """
        logger.info("Generating sample jobs...")
        
        sample_jobs = [
            {
                "id": "sample_001",
                "title": "Senior Python Developer",
                "company_name": "TechCorp Solutions",
                "candidate_required_location": "Remote - India",
                "description": """
                <p>We are looking for a Senior Python Developer with 5+ years of experience.</p>
                <h3>Requirements:</h3>
                <ul>
                    <li>Strong Python programming skills</li>
                    <li>Experience with Django or Flask</li>
                    <li>Knowledge of PostgreSQL and Redis</li>
                    <li>Docker and Kubernetes experience</li>
                    <li>AWS or GCP cloud platforms</li>
                </ul>
                <h3>Responsibilities:</h3>
                <ul>
                    <li>Design and develop scalable backend services</li>
                    <li>Write clean, maintainable code</li>
                    <li>Collaborate with cross-functional teams</li>
                </ul>
                """,
                "url": "https://example.com/jobs/sample_001",
                "salary": "$80,000 - $120,000",
                "job_type": "full_time",
                "tags": ["python", "django", "aws", "docker"]
            },
            {
                "id": "sample_002",
                "title": "Machine Learning Engineer",
                "company_name": "AI Innovations Ltd",
                "candidate_required_location": "Bangalore, India",
                "description": """
                <p>Join our ML team to build cutting-edge AI solutions.</p>
                <h3>Requirements:</h3>
                <ul>
                    <li>3+ years in Machine Learning</li>
                    <li>Strong Python, TensorFlow, PyTorch</li>
                    <li>Experience with NLP or Computer Vision</li>
                    <li>MLOps knowledge preferred</li>
                </ul>
                """,
                "url": "https://example.com/jobs/sample_002",
                "salary": "15-25 LPA",
                "job_type": "full_time",
                "tags": ["machine learning", "python", "tensorflow", "nlp"]
            },
            {
                "id": "sample_003",
                "title": "Full Stack Developer (React + Node)",
                "company_name": "StartupXYZ",
                "candidate_required_location": "Remote",
                "description": """
                <p>Looking for a Full Stack Developer to join our growing team.</p>
                <h3>Tech Stack:</h3>
                <ul>
                    <li>React, TypeScript</li>
                    <li>Node.js, Express</li>
                    <li>MongoDB, PostgreSQL</li>
                    <li>Docker, AWS</li>
                </ul>
                """,
                "url": "https://example.com/jobs/sample_003",
                "salary": "$60,000 - $90,000",
                "job_type": "full_time",
                "tags": ["react", "nodejs", "typescript", "mongodb"]
            }
        ]
        
        logger.info(f"Generated {len(sample_jobs)} sample jobs")
        return sample_jobs[:limit]
    
    def normalize_job(self, raw_job: Dict) -> Dict:
        """Convert format to internal Job model format"""
        return {
            "job_id": str(raw_job.get("id")),
            "title": raw_job.get("title"),
            "company": raw_job.get("company_name", "Unknown"),
            "location": raw_job.get("candidate_required_location", "Remote"),
            "description_html": raw_job.get("description"),
            "url": raw_job.get("url"),
            "source": "sample",
            "salary": raw_job.get("salary", ""),
            "job_type": raw_job.get("job_type", "full_time"),
            "tags": ",".join(raw_job.get("tags", []))
        }
