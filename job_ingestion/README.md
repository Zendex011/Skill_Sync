# Job Ingestion Service

Automated job description fetching and storage system for SkillSync.

## Overview

This service fetches job postings from public APIs, cleans and stores them in a local database, and integrates with the existing skill extraction and matching pipeline.

## Structure

```
job_ingestion/
├── config.py              # Configuration (API URLs, DB settings)
├── database.py            # SQLAlchemy setup
├── ingestion/
│   ├── remotive_client.py # Remotive API client
│   └── fetch_jobs.py      # Main fetcher logic
├── storage/
│   ├── models.py          # Job model
│   └── repository.py      # (Future) Advanced queries
└── cron/
    └── run_ingestion.py   # Cron entry point
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r job_ingestion/requirements.txt
   ```

2. **Initialize database:**
   The database (`jobs.db`) will be created automatically on first run.

3. **Test the ingestion:**
   ```bash
   python job_ingestion/cron/run_ingestion.py
   ```

## Scheduling (Cron)

### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every 12 hours
4. Action: Start a program
   - Program: `python`
   - Arguments: `C:\path\to\job_ingestion\cron\run_ingestion.py`
   - Start in: `C:\path\to\project`

### Linux/Mac (crontab)
```bash
# Run every 12 hours
0 */12 * * * cd /path/to/project && python job_ingestion/cron/run_ingestion.py >> /var/log/job_ingestion.log 2>&1
```

## Current Status

⚠️ **Note**: The Remotive API currently has Cloudflare protection that blocks automated requests. 

### Workarounds:
1. **Manual CSV Import**: Download jobs manually and import via a script
2. **Alternative APIs**: Use GitHub Jobs API, Adzuna, or similar
3. **RSS Feeds**: Parse job board RSS feeds
4. **Selenium/Playwright**: Use browser automation (heavier solution)

## Integration

The `CoreService` automatically loads jobs from the database on startup:
- Jobs are parsed using the existing `JDParser`
- Skills are extracted via `SkillOntology`
- Jobs appear in the matching results alongside sample jobs

## Database Schema

```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    job_id VARCHAR UNIQUE,
    title VARCHAR NOT NULL,
    company VARCHAR NOT NULL,
    location VARCHAR,
    description_text TEXT,
    description_html TEXT,
    source VARCHAR DEFAULT 'remotive',
    url VARCHAR,
    salary VARCHAR,
    job_type VARCHAR,
    tags VARCHAR,
    created_at DATETIME,
    updated_at DATETIME
);
```

## Future Enhancements

- [ ] Add more job sources (LinkedIn, Indeed APIs)
- [ ] Implement retry logic with exponential backoff
- [ ] Add job expiration/cleanup logic
- [ ] Create admin endpoint to trigger manual ingestion
- [ ] Add metrics/monitoring
