# Setting Up Automated Job Ingestion

## Quick Test (Run Manually First)

Before scheduling, test that it works:

```bash
# From project root
run_job_ingestion.bat
```

You should see: "Saved X new jobs" in the output.

---

## Option 1: Windows Task Scheduler (Recommended)

### Step-by-Step Setup:

1. **Open Task Scheduler**
   - Press `Win + R`
   - Type `taskschd.msc`
   - Press Enter

2. **Create Basic Task**
   - Click "Create Basic Task..." (right panel)
   - Name: `SkillSync Job Ingestion`
   - Description: `Fetches job postings every 12 hours`
   - Click Next

3. **Set Trigger**
   - Select "Daily"
   - Click Next
   - Start date: Today
   - Recur every: 1 days
   - Click Next

4. **Set Action**
   - Select "Start a program"
   - Click Next
   - Program/script: Browse to `run_job_ingestion.bat`
   - Full path example: `C:\Users\ASUS\OneDrive\Desktop\college\ML\job finder\run_job_ingestion.bat`
   - Start in: `C:\Users\ASUS\OneDrive\Desktop\college\ML\job finder`
   - Click Next

5. **Advanced Settings**
   - Check "Open the Properties dialog..."
   - Click Finish
   - In Properties → Triggers → Edit
   - Check "Repeat task every: 12 hours"
   - Duration: Indefinitely
   - Click OK

6. **Test It**
   - Right-click the task → Run
   - Check `job_ingestion\cron\ingestion.log` for output

---

## Option 2: Simple Python Scheduler (Alternative)

If Task Scheduler is too complex, use this Python script:

**File: `start_scheduler.py`**
```python
import schedule
import time
import subprocess
import os

def run_ingestion():
    print("Running job ingestion...")
    subprocess.run(["python", "job_ingestion/cron/run_ingestion.py"])
    print("Ingestion complete!")

# Schedule every 12 hours
schedule.every(12).hours.do(run_ingestion)

print("Scheduler started. Job ingestion will run every 12 hours.")
print("Press Ctrl+C to stop.")

# Run once immediately
run_ingestion()

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

**Install dependency:**
```bash
pip install schedule
```

**Run it:**
```bash
python start_scheduler.py
```

Keep this terminal open. It will run in the background.

---

## Option 3: Manual (For Testing)

Just run whenever you want new jobs:

```bash
python job_ingestion/cron/run_ingestion.py
```

---

## Verify It's Working

1. **Check logs:**
   ```
   job_ingestion\cron\ingestion.log
   ```

2. **Check database:**
   ```bash
   python check_db.py
   ```

3. **Restart backend** to see new jobs:
   ```bash
   python backend/run.py
   ```

---

## Current Status

✅ Script created: `run_job_ingestion.bat`
❌ **NOT scheduled yet** - you need to choose one option above

**Recommendation:** Use Option 1 (Task Scheduler) for production, or Option 3 (Manual) for development.
