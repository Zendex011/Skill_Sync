import os

# API Configuration
REMOTIVE_API_URL = "https://remotive.io/api/remote-jobs"

# RapidAPI (JSearch) Configuration
RAPIDAPI_KEY = os.getenv("X-RapidAPI-Key")
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
RAPIDAPI_URL = "https://jsearch.p.rapidapi.com/search"

# Database Configuration
# Using SQLite for simplicity as requested, but easily switchable to Postgres
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = "jobs.db"
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Ingestion Settings
BATCH_SIZE = 50
REQUEST_TIMEOUT = 30  # seconds
