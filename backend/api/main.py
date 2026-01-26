# backend/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import resume, matching, jobs

# Create app
app = FastAPI(
    title="SkillSync API",
    description="AI-Powered Resume-to-Job Matching Backend",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS - Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # Alternative
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router)
app.include_router(matching.router)
app.include_router(jobs.router)

@app.get("/")
async def root():
    return {
        "message": "SkillSync API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}