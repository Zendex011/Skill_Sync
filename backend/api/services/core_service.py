# backend/api/services/core_service.py
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from resume_parser.resume_parser import ResumeParser
from jd_parser.jd_parser import HybridJDParser
from rag.weighted_scorer import WeightedScorer
from rag.roadmap_generator import LearningRoadmapGenerator
from rag.rag_explainer import RAGExplainer
from embeddings.embedding_model import get_embedding_model
from resume_parser.models import Resume
from jd_parser.jd_parser import JobDescription
from api.services.job_search_service import JobSearchService
from api.services.job_search_service import JobSearchService
from job_ingestion.database import get_db, SessionLocal
from job_ingestion.storage.models import Job as JobModel
import uuid
import tempfile
from typing import List, Dict

class CoreService:
    """Bridge service connecting FastAPI to existing Python logic"""
    
    def __init__(self):
        # Initialize all your existing components
        self.resume_parser = ResumeParser(normalize_skills=True)
        self.jd_parser = HybridJDParser()
        self.scorer = WeightedScorer()
        self.roadmap_gen = LearningRoadmapGenerator()
        self.explainer = RAGExplainer()
        self.embedding_model = get_embedding_model()
        self.job_search_service = JobSearchService()
        
        # In-memory cache (use Redis in production)
        self.resume_cache = {}
        self.job_cache = {}
        
        # Load sample jobs from data folder
        self._load_sample_jobs()
    
    def _load_sample_jobs(self):
        """Load sample jobs from data folder or create default ones"""
        # This would load from your data/ folder
        # For now, we'll store parsed jobs in cache
        sample_jobs = [
            """
            Senior Data Scientist - TechCorp India
            Location: Bangalore, Karnataka
            Salary: 15-25 LPA
            Experience: 3-5 years
            
            Requirements:
            - Python, Machine Learning, TensorFlow, PyTorch
            - SQL, AWS, Docker
            - Strong statistics background
            - Experience with MLOps
            """,
            """
            ML Engineer - AI Startup
            Location: Hyderabad
            Salary: 12-20 LPA
            Experience: 2-4 years
            
            Requirements:
            - Python, Deep Learning, PyTorch
            - Docker, Kubernetes
            - REST APIs, FastAPI
            - Experience with model deployment
            """
        ]
        
        for job_text in sample_jobs:
            try:
                job_id = str(uuid.uuid4())
                parsed_job = self.jd_parser.parse(job_text)
                self.job_cache[job_id] = parsed_job
            except:
                pass

        # Load from Database (Job Ingestion)
        try:
            db = SessionLocal()
            db_jobs = db.query(JobModel).all()
            for db_job in db_jobs:
                try:
                    # Convert DB model to JobDescription object expected by the system
                    # We might need to split tags to skills if available, or just rely on description parsing
                    # Ideally, we should parse the description to get actual skills using the JDParser
                    # But for performance, we can do it on demand or pre-parse.
                    # For now, let's parse the description text to ensure skills are extracted.
                    
                    # Using existing parser to extract skills/metadata from raw text
                    parsed_job = self.jd_parser.parse(db_job.description_text or db_job.description_html)
                    
                    # Override fields with known DB data
                    parsed_job.job_title = db_job.title
                    parsed_job.company = db_job.company
                    parsed_job.location = db_job.location
                    # parsed_job.experience_required is extracted by parser
                    
                    # Store in cache
                    # Use a prefix/suffix to avoid collision with UUIDs if needed, or just string of ID
                    job_uuid = f"db_{db_job.id}" 
                    self.job_cache[job_uuid] = parsed_job
                except Exception as ex:
                    print(f"Failed to load DB job {db_job.id}: {ex}")
            db.close()
            print(f"Loaded {len(db_jobs)} jobs from database.")
        except Exception as e:
            print(f"Database loading failed: {e}")
    
    async def parse_resume_file(self, file) -> Resume:
        """
        Parse resume from uploaded file
        
        Args:
            file: UploadFile from FastAPI
            
        Returns:
            Resume object
        """
        content = await file.read()
        
        # Parse using the updated parser method
        parsed = self.resume_parser.parse_upload(content, file.filename)
        
        return parsed
    
    def convert_resume_to_dict(self, resume: Resume) -> dict:
        """Convert Resume object to dict for API response"""
        return {
            'name': resume.name,
            'email': resume.email,
            'phone': resume.phone,
            'linkedin': resume.linkedin,
            'github': resume.github,
            'summary': resume.summary,
            'total_experience_years': resume.total_experience_years,
            'technical_skills': resume.technical_skills,
            'soft_skills': resume.soft_skills,
            'experience': [
                {
                    'company': exp.company,
                    'role': exp.role,
                    'duration': exp.duration,
                    'description': exp.description,
                    'technologies': exp.technologies
                }
                for exp in resume.experience
            ],
            'education': [
                {
                    'degree': edu.degree,
                    'institution': edu.institution,
                    'duration': edu.duration,
                    'gpa': edu.gpa
                }
                for edu in resume.education
            ],
            'projects': [
                {
                    'title': proj.title,
                    'description': proj.description,
                    'technologies': proj.technologies,
                    'link': proj.link
                }
                for proj in resume.projects
            ]
        }
    
    def dict_to_resume(self, resume_dict: dict) -> Resume:
        """Convert dict back to Resume object"""
        from models import Resume, WorkExperience, Education, Project
        
        return Resume(
            name=resume_dict.get('name', ''),
            email=resume_dict.get('email'),
            phone=resume_dict.get('phone'),
            linkedin=resume_dict.get('linkedin'),
            github=resume_dict.get('github'),
            summary=resume_dict.get('summary'),
            total_experience_years=resume_dict.get('total_experience_years'),
            technical_skills=resume_dict.get('technical_skills', []),
            soft_skills=resume_dict.get('soft_skills', []),
            experience=[
                WorkExperience(**exp) for exp in resume_dict.get('experience', [])
            ],
            education=[
                Education(**edu) for edu in resume_dict.get('education', [])
            ],
            projects=[
                Project(**proj) for proj in resume_dict.get('projects', [])
            ]
        )
    
    def match_resume_to_jobs(self, resume_data: dict, specific_job_ids: List[str] = None) -> List[dict]:
        """
        Match resume to all jobs or specific jobs
        
        Args:
            resume_data: Parsed resume dict
            specific_job_ids: Optional list of job IDs to match against
            
        Returns:
            List of jobs with match scores (frontend format)
        """
        # Convert dict to Resume object
        resume = self.dict_to_resume(resume_data)
        
        # Get jobs to match against
        jobs_to_match = {}
        if specific_job_ids:
            jobs_to_match = {jid: job for jid, job in self.job_cache.items() if jid in specific_job_ids}
        else:
            jobs_to_match = self.job_cache
        
        matched_jobs = []
        
        for job_id, job in jobs_to_match.items():
            # Calculate semantic similarity
            resume_embedding = self.embedding_model.encode_resume(resume)
            job_embedding = self.embedding_model.encode_job(job)
            semantic_score = self.embedding_model.compute_similarity(resume_embedding, job_embedding)
            
            # Get weighted score
            scoring_result = self.scorer.calculate_weighted_score(resume, job, semantic_score)
            
            # Extract skill details
            skill_details = scoring_result['breakdown']['skill_match']['details']
            
            # Format for frontend (match mockData.js structure)
            matched_jobs.append({
                'id': job_id,
                'title': job.job_title,
                'company': job.company or 'Company',
                'location': job.location or 'Location TBD',
                'matchScore': round(scoring_result['total_score'] * 100, 1),  # Convert to percentage
                'semanticScore': round(scoring_result['breakdown']['semantic_similarity']['score'] * 100, 1),
                'salary': job.salary_range or 'Competitive',
                'type': job.job_type or 'Full-time',
                'skills': skill_details['matched'],
                'missingSkills': skill_details['missing'],
                'description': f"Experience: {job.experience_required}",
                'experience_required': job.experience_required
            })
        
        # Sort by match score
        matched_jobs.sort(key=lambda x: x['matchScore'], reverse=True)
        
        return matched_jobs
    
    def generate_roadmap(self, resume_data: dict, selected_job: dict) -> dict:
        """
        Generate learning roadmap
        
        Args:
            resume_data: Parsed resume dict
            selected_job: Selected job dict from frontend
            
        Returns:
            Roadmap in frontend format
        """
        resume = self.dict_to_resume(resume_data)
        
        # Get missing skills from selected job
        missing_skills = selected_job.get('missingSkills', [])
        job_title = selected_job.get('title', '')
        
        # Generate roadmap using your existing logic
        roadmap = self.roadmap_gen.generate_roadmap(
            missing_skills,
            job_title,
            resume.technical_skills
        )
        
        # Format for frontend
        return {
            'phases': [
                {
                    'name': phase['name'],
                    'description': phase['description'],
                    'start_week': phase['start_week'],
                    'end_week': phase['end_week'],
                    'skills': [
                        {
                            'name': skill['name'],
                            'weeks': skill['weeks'],
                            'start_week': skill['start_week'],
                            'end_week': skill['end_week'],
                            'resources': skill['resources']
                        }
                        for skill in phase['skills']
                    ]
                }
                for phase in roadmap['phases']
            ],
            'total_skills': roadmap['summary']['total_skills'],
            'estimated_weeks': roadmap['summary']['estimated_weeks'],
            'summary': roadmap['summary']
        }
    
    def generate_explanation(self, resume_data: dict, job: dict, match_score: float) -> dict:
        """Generate AI explanation for match"""
        resume = self.dict_to_resume(resume_data)
        
        # Get job from cache
        job_obj = self.job_cache.get(job['id'])
        if not job_obj:
            return {
                'explanation': 'Job not found in cache',
                'match_score': match_score,
                'breakdown': {}
            }
        
        # Generate explanation
        explanation = self.explainer.explain_match(
            resume,
            job_obj,
            match_score / 100,  # Convert back to 0-1 scale
            job.get('skills', []),
            job.get('missingSkills', [])
        )
        
        return {
            'explanation': explanation,
            'match_score': match_score,
            'match_score': match_score,
            'breakdown': {}
        }
    
    def generate_job_search_links(self, resume_data: dict) -> List[dict]:
        """Generate intelligent job search links using JobSearchService"""
        return self.job_search_service.generate_links(resume_data)

# Global instance
core_service = CoreService()