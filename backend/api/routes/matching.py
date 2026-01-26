# backend/api/routes/matching.py
from fastapi import APIRouter, HTTPException, Body
from api.models.schemas import (
    JobMatchRequest,
    MatchJobsResponse,
    RoadmapRequest,
    RoadmapResponse,
    RoadmapResponse,
    ExplanationResponse,
    JobSearchRequest,
    JobSearchResponse
)
from api.services.core_service import core_service
from typing import Optional

router = APIRouter(prefix="/api", tags=["Matching"])

@router.post("/match-jobs", response_model=MatchJobsResponse)
async def match_jobs(request: JobMatchRequest):
    """
    POST /api/match-jobs
    
    Input: Parsed Resume data + optional Job IDs
    Process: Calls weighted_scorer.py
    Returns: List of Jobs with matchScore and missingSkills
    """
    try:
        # Match resume to jobs
        matched_jobs = core_service.match_resume_to_jobs(
            request.resume_data,
            request.job_ids
        )
        
        return MatchJobsResponse(
            jobs=matched_jobs,
            total_matched=len(matched_jobs)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Job matching failed: {str(e)}"
        )

@router.post("/generate-roadmap", response_model=RoadmapResponse)
async def generate_roadmap(request: RoadmapRequest):
    """
    POST /api/generate-roadmap
    
    Input: Selected Job + Resume
    Process: Calls roadmap_generator.py
    Returns: Phased roadmap structure matching frontend
    """
    try:
        roadmap = core_service.generate_roadmap(
            request.resume_data,
            request.selected_job
        )
        
        return RoadmapResponse(**roadmap)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Roadmap generation failed: {str(e)}"
        )

@router.post("/explain-match", response_model=ExplanationResponse)
async def explain_match(
    resume_data: dict = Body(...),
    job: dict = Body(...),
    match_score: float = Body(...)
):
    """
    POST /api/explain-match
    
    Generate AI explanation for why resume matches job
    """
    try:
        explanation = core_service.generate_explanation(
            resume_data,
            job,
            match_score
        )
        
        return ExplanationResponse(**explanation)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Explanation generation failed: {str(e)}"
        )

@router.post("/job-search", response_model=JobSearchResponse)
async def job_search(request: JobSearchRequest):
    """
    POST /api/job-search
    
    Generate intelligent job search links for multiple platforms
    """
    try:
        links = core_service.generate_job_search_links(request.resume_data)
        
        return JobSearchResponse(
            links=links,
            count=len(links)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Link generation failed: {str(e)}"
        )