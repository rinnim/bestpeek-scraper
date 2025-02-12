import concurrent.futures
import os
from dotenv import load_dotenv
from utils.http_utils import get_urls_of_xml
from utils.send_to_api import send_to_api
from utils.product_utils import get_brand_from_name, remove_brand_from_model, set_prices
from functools import partial
import time

def parse_startech_product(soup, url):
    """Parse Startech product data from the BeautifulSoup object."""

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
    name_element = soup.find('h1', {'class': 'product-name', 'itemprop': 'name'})
    if name_element:
            name= name_element.text.strip() 
    

    price_element = soup.find('td', {'class': 'product-info-data product-price'})
    if price_element:
        try:
            price = int(price_element.text.split('৳')[0].replace(',', '').strip())
        except:
            price = 0
    
    regular_price_element = soup.find('td', {'class': 'product-info-data product-regular-price'})
    if regular_price_element:
        try:
            regular_price = int(regular_price_element.text.replace(',', '').replace('৳', '').strip())
        except:
            regular_price = 0


    # Extract stock status
    stock_element = soup.find('td', {'class': 'product-info-data product-status'})
    if stock_element:
        stock_status=stock_element.text.strip()
        if "discontinued" in stock_status.lower() or "discontinue" in stock_status.lower():
            stock_status = "Discontinued"
        if "pre-order" in stock_status.lower() or "pre order" in stock_status.lower():
            stock_status = "Pre Order"

    # Extract brand
    brand_element = soup.find('td', {'class': 'product-info-data product-brand'})
    if brand_element:
        brand = brand_element.text.strip()
    
    # Extract model
    key_features = soup.find('div', {'class': 'short-description'})
    if key_features:
        for li in key_features.find_all('li'):
            if li.text.startswith('Model:'):
                model = li.text.replace('Model:', '').strip()
                break

    # Extract images
    main_image = soup.find('img', {'class': 'main-img'})
    if main_image and 'src' in main_image.attrs:
        images.append(main_image['src'])

    # Extract category and subcategory
    breadcrumb = soup.find('ul', {'class': 'breadcrumb'})
    if breadcrumb:
        categories = breadcrumb.find_all('a')
        if len(categories) >= 2:
            category = categories[1].text.strip()
            sub_category = categories[2].text.strip()

    # Extract features
    feature_table = soup.find('table', {'class': 'data-table'})
    if feature_table:
        rows = feature_table.find_all('tr')
        for row in rows:
            name_cell = row.find('td', class_='name')
            value_cell = row.find('td', class_='value')
            if name_cell and value_cell:
                feature_name = name_cell.text.strip()
                feature_value = value_cell.text.strip().replace('\n', '<br>').replace(';', '<br>')
                features.append({
                    "name": feature_name,
                    "value": feature_value
                })

    
    # refine data
    model = remove_brand_from_model(brand, model)
    brand = get_brand_from_name(brand, name)
    price = set_prices(price, regular_price)

    return {
        "shop":{
            "name": "startech",
            "href": "https://www.startech.com.bd",
            "logo": "https://www.startech.com.bd/image/catalog/logo.png"
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


def load_from_startech():
    """Load products from Star Tech website."""
    start_time = time.time()
    print("\n\nLoading from Star Tech")
    links_data_arr = get_urls_of_xml(os.getenv('STARTECH_SITEMAP_URL'))

    links_data_arr=links_data_arr[1568:]

    # Limit to the first 1000 URLs for testing
    # links_data_arr = links_data_arr[:1000]
    
    process_with_parser = partial(send_to_api, parse_function=parse_startech_product)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
        executor.map(process_with_parser, links_data_arr)
    
    execution_time = time.time() - start_time
    print(f"Loading from Star Tech Complete")
    print(f"Total execution time: {execution_time:.2f} seconds")
    print(f"Processed {len(links_data_arr)} products")
    print(f"Average time per product: {execution_time/len(links_data_arr):.2f} seconds")