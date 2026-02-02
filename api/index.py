# api/index.py - Vercel Serverless Function Entry Point
from backend.api.main import app

# Export the FastAPI app for Vercel
handler = app
