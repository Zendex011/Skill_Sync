# Start Frontend Development Server

Write-Host "🚀 Starting SkillSync Frontend..." -ForegroundColor Cyan

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Navigate to frontend
Set-Location "$scriptDir\frontend"

# Start the dev server
Write-Host "Starting Vite dev server on http://localhost:5173" -ForegroundColor Green
npm run dev
