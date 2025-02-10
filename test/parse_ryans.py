from bs4 import BeautifulSoup
from scripts.load_from_ryans import parse_ryans_product
from utils.http_utils import fetch_html
import json

def test_parse_product():
    # Test URL from Ryans
    url = 'https://www.ryanscomputers.com/amd-ryzen-5-pro-4650g-processor'
    
    # Fetch and parse HTML
    html = fetch_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Parse product data
        product_data = parse_ryans_product(soup, url)
        
        # Print parsed data in a readable format
        print(f"Parsed product data: \n{json.dumps(product_data, indent=2)}")


test_parse_product()  