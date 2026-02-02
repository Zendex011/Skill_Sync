# Start Backend Server with Virtual Environment

Write-Host "🚀 Starting SkillSync Backend..." -ForegroundColor Cyan

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "$scriptDir\venv\Scripts\Activate.ps1"

# Navigate to backend
Set-Location "$scriptDir\backend"

# Start the server
Write-Host "Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
python run.py
