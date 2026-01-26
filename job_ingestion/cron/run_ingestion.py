import sys
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'ingestion.log'))
    ]
)

# Add project root to path (2 levels up from cron/)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from job_ingestion.ingestion.fetch_jobs import JobFetcher

def main():
    logging.info(f"Starting scheduled ingestion run at {datetime.now()}")
    fetcher = JobFetcher()
    fetcher.run()
    logging.info("Ingestion completed successfully")

if __name__ == "__main__":
    main()
