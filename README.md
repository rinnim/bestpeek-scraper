# BestPeek - Web Scraper
Web Scraper for BestPeek

## Dependencies
- beautifulsoup4 >= 4.12.0 (HTML parsing)
- requests >= 2.31.0 (HTTP requests)
- apscheduler (Task scheduling)
- python-dotenv (Environment variable management)
- bs4 (BeautifulSoup4 extras)

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/bestpeek-scraper.git
   ```

2. Create and activate virtual environment
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate on Windows
   venv\Scripts\activate

   # Activate on Linux/Mac
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables
   - Copy `.env.example` to `.env`
   - Update the variables with your configuration

## Usage
1. Start the scraper
   ```bash
   python main.py
   ``
## Configuration
The following environment variables can be configured in `.env`:

- `API_URL`: URL for the API endpoint
- `STARTECH_SITEMAP_URL`: Sitemap URL for Startech
- `RYANS_SITEMAP_URL`: Sitemap URL for Ryans
- `TECHLAND_SITEMAP_URL`: Sitemap URL for Techland 
- `SKYLAND_SITEMAP_URL`: Sitemap URL for Skyland
- `SCHEDULE_HOUR`: Schedule Hour (UTC Time Hour)
- `SCHEDULE_MINUTE`: Schedule Minute (UTC Time Minute)
