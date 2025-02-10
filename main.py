import logging
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from scripts.load_from_ryans import load_from_ryans
from scripts.load_from_skyland import load_from_skyland
from scripts.load_from_startech import load_from_startech
from scripts.load_from_techland import load_from_techland

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get schedule time from environment variables
hour = int(os.getenv('SCHEDULE_HOUR', '1'))    # Default to 1 AM UTC
minute = int(os.getenv('SCHEDULE_MINUTE', '0')) # Default to 0 minutes

# Create the scheduler instance
scheduler = BlockingScheduler(timezone='UTC')

# Schedule the tasks to run at specified time UTC every day
scheduler.add_job(load_from_techland, 'cron', hour=hour, minute=minute)
scheduler.add_job(load_from_skyland, 'cron', hour=hour, minute=minute)
scheduler.add_job(load_from_ryans, 'cron', hour=hour, minute=minute)
scheduler.add_job(load_from_startech, 'cron', hour=hour, minute=minute)

# Start the scheduler
if __name__ == '__main__':
    try:
        logger.info(f"Starting product loaders scheduler... Will run daily at {hour:02d}:{minute:02d} UTC")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
        pass