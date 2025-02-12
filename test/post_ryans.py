from scripts.load_from_ryans import parse_ryans_product
from utils.send_to_api import send_to_api

def test_post_product():
    # Test URL from Techland
    url = 'https://www.ryanscomputers.com/amd-ryzen-5-pro-4650g-processor'
    # url = input("URL:")
    
    # Use the send_to_api function which handles both parsing and posting
    send_to_api(url, parse_ryans_product)
    


test_post_product() 