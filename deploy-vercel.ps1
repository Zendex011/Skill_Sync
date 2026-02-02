# Quick Vercel Deployment Script
# Run this script to deploy your SkillSync app to Vercel

Write-Host "🚀 SkillSync - Vercel Deployment Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if Vercel CLI is installed
Write-Host "Checking for Vercel CLI..." -ForegroundColor Yellow
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue

if (-not $vercelInstalled) {
    Write-Host "❌ Vercel CLI not found. Installing..." -ForegroundColor Red
    npm install -g vercel
    Write-Host "✅ Vercel CLI installed successfully!`n" -ForegroundColor Green
} else {
    Write-Host "✅ Vercel CLI is already installed`n" -ForegroundColor Green
}

# Login to Vercel
Write-Host "Logging in to Vercel..." -ForegroundColor Yellow
vercel login

# Deploy to Vercel
Write-Host "`n📦 Deploying to Vercel..." -ForegroundColor Yellow
Write-Host "Choose deployment type:" -ForegroundColor Cyan
Write-Host "1. Preview deployment (for testing)" -ForegroundColor White
Write-Host "2. Production deployment" -ForegroundColor White
$choice = Read-Host "`nEnter your choice (1 or 2)"

if ($choice -eq "2") {
    Write-Host "`n🚀 Deploying to PRODUCTION..." -ForegroundColor Green
    vercel --prod
} else {
    Write-Host "`n🔍 Deploying to PREVIEW..." -ForegroundColor Yellow
    vercel
}

Write-Host "`n✅ Deployment complete!" -ForegroundColor Green
Write-Host "`n⚠️  IMPORTANT: Don't forget to set your environment variables!" -ForegroundColor Yellow
Write-Host "Run these commands to add your API keys:" -ForegroundColor Cyan
Write-Host "  vercel env add HF_TOKEN" -ForegroundColor White
Write-Host "  vercel env add X_RapidAPI_Key" -ForegroundColor White
Write-Host "  vercel env add APLY_HUB_API" -ForegroundColor White
Write-Host "`nOr set them in the Vercel Dashboard: https://vercel.com/dashboard" -ForegroundColor Cyan
