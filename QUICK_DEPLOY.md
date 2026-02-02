# 🚀 Quick Deployment Guide

## TL;DR - Fastest Way to Deploy

Your app needs **split deployment** because the Python backend is too complex for Vercel serverless functions.

### Step 1: Deploy Backend to Railway (5 minutes)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy from project root
railway init
railway up
```

**Add environment variables in Railway Dashboard:**
- Go to https://railway.app/dashboard
- Click your project → Variables
- Add:
  - `HF_TOKEN` = `your_huggingface_token_here`
  - `X_RapidAPI_Key` = `your_rapidapi_key_here`
  - `APLY_HUB_API` = `your_aply_hub_api_key_here`

**Copy your Railway URL** (looks like: `https://skillsync-production.up.railway.app`)

### Step 2: Update Frontend Config (1 minute)

Edit `frontend/.env.production` and replace with your Railway URL:

```env
VITE_API_URL=https://your-actual-backend.railway.app
```

### Step 3: Deploy Frontend to Vercel (3 minutes)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

**Done!** 🎉

---

## Why This Approach?

| Issue | Vercel Serverless | Railway |
|-------|-------------------|---------|
| 50MB size limit | ❌ Your backend is 200MB+ | ✅ No limit |
| Cold start timeout | ❌ ML models take 30s+ | ✅ Always warm |
| Database support | ❌ No persistent storage | ✅ Full PostgreSQL |
| Cost | Free | $5/month (free $5 credit) |

---

## Troubleshooting

### Backend deployment fails on Railway

**Check your `requirements.txt`** - Make sure it has all dependencies:

```bash
# From project root
pip freeze > requirements.txt
```

Then redeploy:

```bash
railway up
```

### Frontend can't connect to backend

1. **Check CORS**: Your backend should allow your Vercel domain
2. **Verify API URL**: Make sure `VITE_API_URL` in `frontend/.env.production` is correct
3. **Check Railway logs**: `railway logs`

### Environment variables not working

- Railway: Set them in the dashboard, then restart the service
- Vercel: Set with `vercel env add VARIABLE_NAME`

---

## Alternative: Deploy Everything to Railway

If you want to avoid Vercel entirely:

```bash
railway login
railway init
railway up
```

Railway will serve both frontend and backend from one deployment.

---

## Files Created for You

- ✅ `Procfile` - Railway/Heroku startup command
- ✅ `railway.json` - Railway configuration
- ✅ `frontend/.env.production` - Production API URL (UPDATE THIS!)
- ✅ `frontend/.env.development` - Local development config
- ✅ `vercel.json` - Vercel frontend-only config
- ✅ `DEPLOYMENT_STRATEGY.md` - Full deployment guide
- ✅ `VERCEL_DEPLOYMENT.md` - Original Vercel guide (for reference)

---

## Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Copy Railway URL
3. ✅ Update `frontend/.env.production` with Railway URL
4. ✅ Deploy frontend to Vercel
5. ✅ Test your live app!

**Need help?** Check `DEPLOYMENT_STRATEGY.md` for detailed instructions.
