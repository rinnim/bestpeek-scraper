import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_url = os.getenv("API_URL")
startech_sitemap = os.getenv("STARTECH_SITEMAP_URL") 
ryans_sitemap = os.getenv("RYANS_SITEMAP_URL")
techland_sitemap = os.getenv("TECHLAND_SITEMAP_URL")
binarylogic_sitemap = os.getenv("BINARYLOGIC_SITEMAP_URL")
skyland_sitemap = os.getenv("SKYLAND_SITEMAP_URL")
schedule_hour = os.getenv("SCHEDULE_HOUR")
schedule_minute = os.getenv("SCHEDULE_MINUTE")

# Print values (for testing)
print(f"API URL: {api_url}")
print(f"Startech Sitemap URL: {startech_sitemap}")
print(f"Ryans Sitemap URL: {ryans_sitemap}")
print(f"Techland Sitemap URL: {techland_sitemap}")
print(f"Binary Logic Sitemap URL: {binarylogic_sitemap}")
print(f"Skyland Sitemap URL: {skyland_sitemap}")
print(f"Schedule Hour: {schedule_hour}")
print(f"Schedule Minute: {schedule_minute}")
