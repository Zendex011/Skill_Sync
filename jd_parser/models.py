# models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class JobDescription(BaseModel):
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