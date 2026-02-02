# api/index.py - Vercel Serverless Function Entry Point
import sys
import os

# Add the parent directory to the path so we can import from backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.api.main import app

# Vercel expects the ASGI app to be named 'app'
# FastAPI is already an ASGI app, so we can export it directly
app = app
