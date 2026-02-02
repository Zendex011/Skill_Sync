# Vercel Deployment Guide

This guide explains how to deploy your SkillSync application to Vercel directly from your local machine with custom API keys (different from GitHub).

## Prerequisites

- Node.js installed (v18 or higher)
- Vercel account ([sign up here](https://vercel.com/signup))
- Your local `.env` file with production API keys

## Option 1: Deploy via Vercel CLI (Recommended)

This method deploys directly from your local machine, bypassing GitHub entirely.

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

Follow the prompts to authenticate with your Vercel account.

### Step 3: Configure Your Project

Since you have a monorepo structure (frontend + backend), you need to create a `vercel.json` configuration file.

### Step 4: Deploy

Navigate to your project root and run:

```bash
vercel
```

For production deployment:

```bash
vercel --prod
```

The CLI will:
1. Ask you to link to an existing project or create a new one
2. Detect your framework (Vite for frontend)
3. Ask for build settings
4. Deploy your application

### Step 5: Set Environment Variables

After deployment, add your environment variables:

```bash
# Add environment variables one by one
vercel env add HF_TOKEN
vercel env add X_RapidAPI_Key
vercel env add APLY_HUB_API
```

Or set them via the Vercel Dashboard:
1. Go to your project on [vercel.com](https://vercel.com)
2. Click **Settings** → **Environment Variables**
3. Add each variable with the appropriate value
4. Select the environments (Production, Preview, Development)

### Step 6: Redeploy with Environment Variables

```bash
vercel --prod
```

---

## Option 2: GitHub Integration with Vercel Environment Variables

If you want to keep your GitHub integration but use different API keys:

### Step 1: Connect GitHub Repository to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Configure the project settings

### Step 2: Override Environment Variables

1. In Vercel Dashboard, go to **Settings** → **Environment Variables**
2. Add your production API keys:
   - `HF_TOKEN` = your production HuggingFace token
   - `X_RapidAPI_Key` = your production RapidAPI key
   - `APLY_HUB_API` = your production Aply Hub API key
3. **Important**: Select **Production** environment only
4. Save the variables

### Step 3: Deploy

Push to your main branch or manually trigger a deployment from Vercel dashboard.

**Note**: The environment variables in Vercel will override any `.env` files in your repository. Your GitHub `.env` values won't be used.

---

## Project Configuration

### Required: `vercel.json`

Create this file in your project root to configure the deployment:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    },
    {
      "src": "backend/api/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ],
  "env": {
    "HF_TOKEN": "@hf_token",
    "X_RapidAPI_Key": "@x_rapidapi_key",
    "APLY_HUB_API": "@aply_hub_api"
  }
}
```

### Update Frontend Build Script

Ensure your `frontend/package.json` has the correct build output:

```json
{
  "scripts": {
    "build": "vite build",
    "vercel-build": "vite build"
  }
}
```

### Python Backend Configuration

Create `backend/requirements.txt` if not already present with all your Python dependencies.

---

## Important Notes

### Security Best Practices

1. **Never commit `.env` files** - Already in your `.gitignore`
2. **Use different API keys** for development and production
3. **Rotate keys** if they're ever exposed in GitHub history

### Environment Variable Priority

Vercel uses this priority order:
1. Environment variables set in Vercel Dashboard (highest priority)
2. Environment variables in `vercel.json`
3. `.env` files in your repository (lowest priority)

### Deployment Environments

Vercel has three environments:
- **Production**: Deployments from your main/master branch
- **Preview**: Deployments from pull requests and other branches
- **Development**: Local development with `vercel dev`

You can set different environment variables for each.

---

## Troubleshooting

### Issue: API Keys Not Working

**Solution**: Ensure environment variables are set for the correct environment (Production/Preview/Development).

### Issue: Build Fails

**Solution**: Check build logs in Vercel dashboard. Common issues:
- Missing dependencies in `package.json` or `requirements.txt`
- Incorrect build commands
- Node.js version mismatch

### Issue: Backend Routes Not Working

**Solution**: Verify `vercel.json` routes configuration and ensure Python files are in the correct directory structure.

---

## Quick Reference Commands

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Add environment variable
vercel env add VARIABLE_NAME

# List environment variables
vercel env ls

# Remove environment variable
vercel env rm VARIABLE_NAME

# Pull environment variables to local
vercel env pull
```

---

## Next Steps

1. Choose your deployment method (CLI or GitHub integration)
2. Create `vercel.json` configuration file
3. Set up environment variables in Vercel
4. Deploy your application
5. Test the deployed application with production API keys

For more information, visit [Vercel Documentation](https://vercel.com/docs).
