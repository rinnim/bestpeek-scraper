from bs4 import BeautifulSoup
from scripts.load_from_skyland import parse_skyland_product
from utils.http_utils import fetch_html
import json

def test_parse_product():
    # Test URL from Skyland
    url = 'https://www.skyland.com.bd/components/processor/amd-processor/amd-ryzen-5-pro-4650g-processor/'
    
    # Fetch and parse HTML
    html = fetch_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Parse product data
        product_data = parse_skyland_product(soup, url)
        
        # Print parsed data in a readable format
        print(f"Parsed product data: \n{json.dumps(product_data, indent=2)}")


test_parse_product()  