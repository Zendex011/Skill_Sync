# models.py (add to existing file)
from pydantic import BaseModel, Field
from typing import List, Optional

# Your existing JobDescription model stays here
class JobDescription(BaseModel):
    # ... (keep existing code)
    """Structured job description data"""
    
    job_title: str = Field(
        description="The job title or position name"
    )
    
    experience_required: str = Field(
        description="Years of experience required (e.g., '3-5 years', 'Entry level')"
    )
    
    technical_skills: List[str] = Field(
        description="List of technical skills required (e.g., Python, SQL, AWS)"
    )
    
    soft_skills: List[str] = Field(
        default=[],
        description="List of soft skills (e.g., communication, leadership)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "job_title": "Senior Data Scientist",
                "experience_required": "3-5 years",
                "technical_skills": ["Python", "Machine Learning", "SQL", "PyTorch"],
                "soft_skills": ["Communication", "Team collaboration"]
            }
        }
    pass

# NEW: Resume model
class WorkExperience(BaseModel):
    """Single work experience entry"""
    company: Optional[str] = Field(description="Company name")
    role: Optional[str] = Field(description="Job title/role")
    duration: Optional[str] = Field(description="Duration (e.g., 'Jan 2020 - Dec 2022')")
    description: Optional[str] = Field(default=None, description="Job description")
    technologies: List[str] = Field(default=[], description="Technologies used")

class Education(BaseModel):
    """Education entry"""
    degree: Optional[str] = Field(default="N/A", description="Degree name")
    institution: Optional[str] = Field(default="N/A", description="College/University name")
    duration: Optional[str] = Field(default="N/A", description="Duration or graduation year")
    gpa: Optional[float] = Field(default=None, description="GPA/percentage")

class Project(BaseModel):
    """Project entry"""
    title: Optional[str] = Field(default="Untitled Project", description="Project name")
    description: Optional[str] = Field(default="No description provided", description="Project description")
    technologies: List[str] = Field(default=[], description="Technologies used")
    link: Optional[str] = Field(default=None, description="GitHub/demo link")

class Resume(BaseModel):
    """Complete resume structure - focus on skills and experience"""
    name: Optional[str] = Field(default="Unknown", description="Candidate's full name")
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile URL")
    github: Optional[str] = Field(default=None, description="GitHub profile URL")
    summary: Optional[str] = Field(default=None, description="Professional summary")
    total_experience_years: Optional[float] = Field(default=0.0, description="Total years of work experience")
    
    technical_skills: List[str] = Field(default=[], description="Technical skills")
    soft_skills: List[str] = Field(default=[], description="Soft skills")
    
    experience: List[WorkExperience] = Field(default=[], description="Work experience")
    education: List[Education] = Field(default=[], description="Education")
    projects: List[Project] = Field(default=[], description="Projects")

