import concurrent.futures
import os
from dotenv import load_dotenv
from utils.http_utils import get_urls_of_xml
from utils.send_to_api import send_to_api
from utils.product_utils import get_brand_from_name, remove_brand_from_model, set_prices
from functools import partial
import time

def parse_ryans_product(soup, url):
    """Parse Ryans product data from the BeautifulSoup object."""

    # Initialize default values
    name = ""
    price = 0
    regular_price = 0
    stock_status = ""
    brand = ""
    model = ""
    category = ""
    sub_category = ""
    images = []
    features = []


    # Extract name
    name_element = soup.find('h1', {'itemprop': 'name'}).text.strip() 
    if name_element:
        name = name_element
    

    # Extract price 
    price_element = soup.find('span', {'class': 'new-sp-text'})
    if price_element:
        try:
            price_text = price_element.text.strip()
            price = int(price_text.replace('Tk', '').replace(',', '').strip())
        except:
            price = 0
    
    # Extract regular price
    regular_price_element = soup.find('span', {'class': 'new-reg-text'})
    if regular_price_element:
        try:
            regular_price_text = regular_price_element.text.strip()
            regular_price = int(regular_price_text.replace('Tk', '').replace(',', '').strip())
        except:
            regular_price = 0


    # Extract stock status
    stock_element = soup.find('p', {'class': 'text-danger'}).text.strip()
    if not stock_element:
        stock_element = soup.find('span', {'class': 'stock-text'}).text.strip()
    if stock_element:
        stock_status = "Discontinued" if "discontinued" in stock_element.lower() else "Out of Stock" if price == 0 else "In Stock"
    

    # Extract images
    slideshow_container = soup.find('div', {'id': 'slideshow-items-container'})
    if slideshow_container:
        for img in slideshow_container.find_all('img'):
            if 'src' in img.attrs:
                images.append(img['src'])

    # Extract category and subcategory
    category_element = soup.find('div', {'class': 'category-pagination-section'})
    if category_element:
        category = category_element.find_all('a')[1].text.strip()
        sub_category = category_element.find_all('a')[2].text.strip()
        

    # Extract features
    feature_table = soup.find_all('div', {'class': 'row table-hr-remove'})
    for row in feature_table:
        name_cell = row.find('span', {'class': 'att-title'})
        value_cell = row.find('span', {'class': 'att-value'})
        if name_cell and value_cell:
            feature_name = name_cell.text.strip()
            feature_value = value_cell.text.strip()
            features.append({
                "name": feature_name,
                "value": feature_value
            })

    # Extract brand, model
    for feature in features:
        if feature['name'].lower() == 'brand':
            brand = feature['value']
        elif feature['name'].lower() == 'model':
            model = feature['value']
    
    # refine data
    model = remove_brand_from_model(brand, model)
    brand = get_brand_from_name(brand, name)
    price = set_prices(price, regular_price)

    return {
        "shop": {
            "name": "ryans",
            "href": "https://www.ryanscomputers.com",
            "logo": "https://www.ryanscomputers.com/assets/images/ryans-logo.svg"
        },
        "product": {
            "href": url,
            "category": category,
            "subCategory": sub_category,
            "name": name,
            "price": price,
            "brand": brand,
            "status": stock_status.lower(),
            "model": model,
            "images": images,
            "features": features,
        }
    }

# Load environment variables
load_dotenv()


def load_from_ryans():
    """Load products from Ryans website."""
    start_time = time.time()
    print("Loading from Ryans")
    links_data_arr = get_urls_of_xml(os.getenv('RYANS_SITEMAP_URL'))

    # Limit to the first 1000 URLs for testing
    # links_data_arr = links_data_arr[:1000]
    
    process_with_parser = partial(send_to_api, parse_function=parse_ryans_product)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
        executor.map(process_with_parser, links_data_arr)
    
    execution_time = time.time() - start_time
    print(f"Loading from Ryans Complete")
    print(f"Total execution time: {execution_time:.2f} seconds")
    print(f"Processed {len(links_data_arr)} products")
    print(f"Average time per product: {execution_time/len(links_data_arr):.2f} seconds")