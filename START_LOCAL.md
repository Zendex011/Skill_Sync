# 🚀 Start Local Development

## Quick Start Commands

### Terminal 1: Start Backend

```powershell
# Navigate to project root
cd "c:\Users\ASUS\OneDrive\Desktop\college\ML\job finder"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Navigate to backend
cd backend

# Run the backend server
python run.py
```

**Backend will run on:** http://localhost:8000

### Terminal 2: Start Frontend

```powershell
# Navigate to frontend
cd "c:\Users\ASUS\OneDrive\Desktop\college\ML\job finder\frontend"

# Start the dev server
npm run dev
```

**Frontend will run on:** http://localhost:5173

---

## Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'fastapi'"

**Problem:** Virtual environment not activated

**Solution:**
```powershell
# Make sure you're in the project root
cd "c:\Users\ASUS\OneDrive\Desktop\college\ML\job finder"

# Activate venv
.\venv\Scripts\Activate.ps1

# You should see (venv) in your terminal prompt
# Now run the backend
cd backend
python run.py
```

### ❌ "npm ERR! Missing script: 'start'"

**Problem:** Wrong npm command

**Solution:**
```powershell
# Use 'npm run dev' instead of 'npm start'
npm run dev
```

### ❌ Virtual environment activation fails

**Solution:**
```powershell
# Enable script execution (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.\venv\Scripts\Activate.ps1
```

---

## One-Command Startup Scripts

### Backend Startup Script

Create `start-backend.ps1`:

```powershell
# Activate venv and start backend
cd "c:\Users\ASUS\OneDrive\Desktop\college\ML\job finder"
.\venv\Scripts\Activate.ps1
cd backend
python run.py
```

Run with: `.\start-backend.ps1`

### Frontend Startup Script

Create `start-frontend.ps1`:

```powershell
# Start frontend
cd "c:\Users\ASUS\OneDrive\Desktop\college\ML\job finder\frontend"
npm run dev
```

Run with: `.\start-frontend.ps1`

---

## Verify Everything is Running

1. **Backend Health Check:** http://localhost:8000/health
2. **Backend API Docs:** http://localhost:8000/api/docs
3. **Frontend:** http://localhost:5173

---

## Stop the Servers

- Press `Ctrl + C` in each terminal to stop the servers
