from bs4 import BeautifulSoup
from scripts.load_from_startech import parse_startech_product
from utils.http_utils import fetch_html
import json

def test_parse_product():
    # Test URL from StarTech
    # url = "https://www.startech.com.bd/apple-macbook-pro-16-inch-m3-pro"
    # url = 'https://www.startech.com.bd/avita-liber-v14-core-i5-11th-gen-laptop-anchor-grey'
    # url = 'https://www.startech.com.bd/lenovo-ideapad-flex-5-14alc7-amd-ryzen-7-laptop'
    url = 'https://www.startech.com.bd/lenovo-thinkpad-bluetooth-silent-mouse'
    
    # Fetch and parse HTML
    html = fetch_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Parse product data
        product_data = parse_startech_product(soup, url)
        
        # Print parsed data in a readable format
        print(f"Parsed product data: \n{json.dumps(product_data, indent=2)}")


test_parse_product()  