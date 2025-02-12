from scripts.load_from_startech import parse_startech_product
from utils.send_to_api import send_to_api

def test_post_product():
    # Test URL from Techland
    url = 'https://www.startech.com.bd/hp-laser-mfp-137fnw-printer'
    # url = input("URL:")
    
    # Use the send_to_api function which handles both parsing and posting
    send_to_api(url, parse_startech_product)
    


test_post_product() 