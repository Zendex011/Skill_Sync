# backend/api/routes/resume.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from api.models.schemas import ParsedResumeResponse
from api.services.core_service import core_service

router = APIRouter(prefix="/api", tags=["Resume"])

@router.post("/parse-resume", response_model=ParsedResumeResponse)
async def parse_resume(file: UploadFile = File(...)):
    """
    POST /api/parse-resume
    
    Upload and parse resume (PDF/DOCX)
    
    Returns: Parsed resume matching Resume model
    """
    # Validate file type
    if not file.filename.endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )
    
    try:
        # Parse using core service
        parsed_resume = await core_service.parse_resume_file(file)
        
        # Convert to dict for response
        resume_dict = core_service.convert_resume_to_dict(parsed_resume)
        
        return ParsedResumeResponse(**resume_dict)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Resume parsing failed: {str(e)}"
        )