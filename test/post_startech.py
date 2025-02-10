from scripts.load_from_startech import parse_startech_product
from utils.product_processor import process_product_url

def test_post_product():
    # Test URL from Techland
    url = 'https://www.startech.com.bd/hp-laser-mfp-137fnw-printer'
    # url = input("URL:")
    
    # Use the process_product_url function which handles both parsing and posting
    process_product_url(url, parse_startech_product)
    


test_post_product() 