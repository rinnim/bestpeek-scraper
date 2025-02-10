from scripts.load_from_ryans import parse_ryans_product
from utils.product_processor import process_product_url

def test_post_product():
    # Test URL from Techland
    url = 'https://www.ryanscomputers.com/amd-ryzen-5-pro-4650g-processor'
    # url = input("URL:")
    
    # Use the process_product_url function which handles both parsing and posting
    process_product_url(url, parse_ryans_product)
    


test_post_product() 