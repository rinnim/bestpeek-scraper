import requests
import os
from bs4 import BeautifulSoup
from .http_utils import fetch_html
from dotenv import load_dotenv

def send_to_api(url, parse_function):
    """Fetch and process product data from a URL."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Fetch HTML content from the product URL
        html = fetch_html(url)
        if not html:
            return

        # Parse HTML and extract product data
        soup = BeautifulSoup(html, 'html.parser')
        product_data = parse_function(soup, url)

        # Set headers for API request
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Send product data to API
        api_response = requests.post(
            os.getenv('API_URL'),
            json=product_data,
            headers=headers
        )
        
        # Handle API responses
        if api_response.status_code == 201:
            print(f"Success: {url}")
        else:
            print(f"Error: {url}: {api_response.status_code} {api_response.text}")
            return

    except Exception as error:
        print(f"Error processing {url}: {str(error)}")
        # pass