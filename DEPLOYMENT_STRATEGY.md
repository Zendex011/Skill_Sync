# Deployment Strategy for SkillSync

## Problem

Your SkillSync application has a complex Python backend with heavy dependencies (LangChain, HuggingFace, SQLAlchemy, ChromaDB, etc.) that are **not suitable for Vercel's serverless functions** due to:

1. **Size limitations**: Vercel serverless functions have a 50MB limit
2. **Cold start times**: Heavy ML models cause timeouts
3. **Stateful dependencies**: Database connections and embeddings require persistent storage

## Recommended Solution: Split Deployment

Deploy your frontend and backend separately with different API keys for each environment.

### Architecture

```
Frontend (Vercel) → Backend API (Railway/Render/Heroku)
```

---

## Option 1: Frontend on Vercel + Backend on Railway (Recommended)

This is the **best approach** for your use case.

### Step 1: Deploy Backend to Railway

[Railway](https://railway.app) is perfect for Python backends with databases and ML models.

#### 1.1 Create `Procfile` for Railway

Create this file in your project root:

```
web: cd backend && uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

#### 1.2 Create `railway.json`

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn api.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 1.3 Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variables
railway variables set HF_TOKEN=your_production_token
railway variables set X_RapidAPI_Key=your_production_key
railway variables set APLY_HUB_API=your_production_key

# Deploy
railway up
```

Railway will give you a URL like: `https://your-app.railway.app`

### Step 2: Deploy Frontend to Vercel

#### 2.1 Update Frontend API URL

Create `frontend/.env.production`:

```env
VITE_API_URL=https://your-app.railway.app
```

Update your frontend API calls to use this environment variable:

```javascript
// In your API service file
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

#### 2.2 Simplify `vercel.json`

```json
{
  "buildCommand": "cd frontend && npm ci && npm run build",
  "outputDirectory": "frontend/dist"
}
```

#### 2.3 Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Set environment variable
vercel env add VITE_API_URL

# Deploy
vercel --prod
```

---

## Option 2: Both on Railway

Deploy everything to Railway if you prefer a single platform.

### Configuration

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn api.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Deploy

```bash
railway login
railway init
railway variables set HF_TOKEN=your_token
railway variables set X_RapidAPI_Key=your_key
railway variables set APLY_HUB_API=your_key
railway up
```

Railway will serve both your frontend (as static files) and backend.

---

## Option 3: Frontend-Only on Vercel (Mock Backend)

If you just want to deploy the frontend for demonstration purposes:

### Step 1: Create Mock API

Create `frontend/src/services/mockApi.js`:

```javascript
// Mock API for demo purposes
export const mockApi = {
  parseResume: async (file) => {
    // Return mock data
    return { /* mock resume data */ };
  },
  // ... other mock endpoints
};
```

### Step 2: Deploy to Vercel

```bash
vercel --prod
```

This is only suitable for **demos**, not production.

---

## Comparison Table

| Platform | Frontend | Backend | Database | ML Models | Cost (Free Tier) |
|----------|----------|---------|----------|-----------|------------------|
| **Vercel + Railway** | ✅ Excellent | ✅ Excellent | ✅ Yes | ✅ Yes | $0-5/month |
| **Railway Only** | ✅ Good | ✅ Excellent | ✅ Yes | ✅ Yes | $5/month |
| **Vercel Only** | ✅ Excellent | ❌ Limited | ❌ No | ❌ No | Free |
| **Render** | ✅ Good | ✅ Excellent | ✅ Yes | ✅ Yes | Free (slow) |

---

## Quick Start: Recommended Path

### 1. Deploy Backend to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up

# Add environment variables in Railway dashboard
# https://railway.app/dashboard
```

### 2. Update Frontend Configuration

```bash
cd frontend

# Create production environment file
echo "VITE_API_URL=https://your-backend.railway.app" > .env.production
```

### 3. Deploy Frontend to Vercel

```bash
# From project root
vercel --prod
```

---

## Environment Variables Summary

### Backend (Railway)
- `HF_TOKEN` - Your HuggingFace token
- `X_RapidAPI_Key` - Your RapidAPI key
- `APLY_HUB_API` - Your Aply Hub API key
- `PORT` - Auto-set by Railway

### Frontend (Vercel)
- `VITE_API_URL` - Your Railway backend URL

---

## Next Steps

1. **Choose your deployment strategy** (I recommend Option 1)
2. **Create necessary configuration files** (Procfile, railway.json, etc.)
3. **Deploy backend first** to get the API URL
4. **Update frontend** with the backend URL
5. **Deploy frontend** to Vercel
6. **Test the integration**

---

## Troubleshooting

### Backend won't start on Railway
- Check logs: `railway logs`
- Ensure all dependencies are in `requirements.txt`
- Verify `Procfile` has correct command

### Frontend can't connect to backend
- Check CORS settings in `backend/api/main.py`
- Add your Vercel URL to allowed origins
- Verify `VITE_API_URL` is set correctly

### API keys not working
- Ensure environment variables are set in Railway dashboard
- Check variable names match your code (underscores vs hyphens)
- Restart the service after adding variables

---

## Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)
- [Render Documentation](https://render.com/docs)
