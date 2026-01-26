from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime
from datetime import datetime
from job_ingestion.database import Base

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)  # External ID from source
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String)
    description_text = Column(Text)  # Cleaned text
    description_html = Column(Text)  # Original HTML
    source = Column(String, default="remotive")
    url = Column(String)
    salary = Column(String, nullable=True)
    job_type = Column(String, nullable=True)
    tags = Column(String, nullable=True)  # Comma-separated tags
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "job_id": self.job_id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description_text,
            "url": self.url,
            "source": self.source,
            "created_at": self.created_at.isoformat()
        }
