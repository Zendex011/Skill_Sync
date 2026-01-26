"""
Repository layer for Job storage operations.
Provides helper methods for querying and managing jobs.
"""

from sqlalchemy.orm import Session
from .models import Job
from typing import List, Optional
from datetime import datetime, timedelta

class JobRepository:
    """Data access layer for Job model"""
    
    @staticmethod
    def get_all(db: Session, limit: int = 100) -> List[Job]:
        """Get all jobs, most recent first"""
        return db.query(Job).order_by(Job.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_by_source(db: Session, source: str) -> List[Job]:
        """Get jobs from a specific source"""
        return db.query(Job).filter(Job.source == source).all()
    
    @staticmethod
    def get_recent(db: Session, days: int = 7) -> List[Job]:
        """Get jobs posted in the last N days"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        return db.query(Job).filter(Job.created_at >= cutoff).all()
    
    @staticmethod
    def exists(db: Session, job_id: str) -> bool:
        """Check if job already exists"""
        return db.query(Job).filter(Job.job_id == job_id).first() is not None
    
    @staticmethod
    def create(db: Session, job_data: dict) -> Job:
        """Create a new job"""
        job = Job(**job_data)
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    
    @staticmethod
    def delete_old(db: Session, days: int = 30) -> int:
        """Delete jobs older than N days"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        count = db.query(Job).filter(Job.created_at < cutoff).delete()
        db.commit()
        return count
