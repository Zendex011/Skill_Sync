# backend/api/models/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

# ============= REQUEST MODELS =============

class JobMatchRequest(BaseModel):
    """Request for matching resume to jobs"""
    resume_data: dict  # Parsed resume from frontend or parse endpoint
    job_ids: Optional[List[str]] = None  # Optional: specific job IDs to match

class RoadmapRequest(BaseModel):
    """Request for generating learning roadmap"""
    resume_data: dict
    selected_job: dict

class JobSearchRequest(BaseModel):
    """Request for generating job search links"""
    resume_data: dict

# ============= RESPONSE MODELS =============

class WorkExperienceResponse(BaseModel):
    company: str
    role: str
    duration: str
    description: Optional[str] = None
    technologies: List[str] = []

class EducationResponse(BaseModel):
    degree: str
    institution: str
    duration: str
    gpa: Optional[float] = None

class ProjectResponse(BaseModel):
    title: str
    description: str
    technologies: List[str] = []
    link: Optional[str] = None

class ParsedResumeResponse(BaseModel):
    """Response from resume parsing - matches Resume model"""
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    summary: Optional[str] = None
    total_experience_years: Optional[float] = None
    technical_skills: List[str] = []
    soft_skills: List[str] = []
    experience: List[WorkExperienceResponse] = []
    education: List[EducationResponse] = []
    projects: List[ProjectResponse] = []

class JobResponse(BaseModel):
    """Single job with match details - matches frontend mockData structure"""
    id: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    matchScore: float  # Note: camelCase to match frontend
    semanticScore: Optional[float] = None
    salary: Optional[str] = None
    type: Optional[str] = None
    skills: List[str] = []
    missingSkills: List[str] = []  # camelCase
    description: Optional[str] = None
    experience_required: Optional[str] = None

class MatchJobsResponse(BaseModel):
    """Response from job matching"""
    jobs: List[JobResponse]
    total_matched: int

class SkillPlanResponse(BaseModel):
    """Individual skill in roadmap"""
    name: str
    weeks: int
    start_week: int
    end_week: int
    resources: dict  # {beginner: [...], intermediate: [...], advanced: [...]}

class PhaseResponse(BaseModel):
    """Phase in learning roadmap"""
    name: str
    description: str
    start_week: int
    end_week: int
    skills: List[SkillPlanResponse]

class RoadmapResponse(BaseModel):
    """Learning roadmap response - matches frontend structure"""
    phases: List[PhaseResponse]
    total_skills: int
    estimated_weeks: int
    summary: dict

class ExplanationResponse(BaseModel):
    """AI explanation for match"""
    explanation: str
    match_score: float
    breakdown: dict

class JobLinkResponse(BaseModel):
    platform: str
    platform_key: str
    query: str
    url: str
    priority: str
    location: str

class JobSearchResponse(BaseModel):
    links: List[JobLinkResponse]
    count: int