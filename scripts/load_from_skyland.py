import concurrent.futures
import os

from dotenv import load_dotenv
from utils.http_utils import get_urls_of_xml
from utils.product_processor import process_product_url
from utils.product_utils import get_brand_from_name, remove_brand_from_model, set_prices
from functools import partial
import time

def parse_skyland_product(soup, url):
    """Parse Skyland product data from the BeautifulSoup object."""

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
    name_element = soup.find('h1', {'class': 'title page-title'})
    if name_element:
        name = name_element.text.strip()


    # Extract price, regular price, stock status, brand, model
    short_info = soup.find('div', {'class': 'short-info'})
    if short_info:
        price_element = short_info.find('li',{'class':'product-mpn'})
        if price_element:
            try:
                price_text = price_element.find_all('span')[1].text.strip()
                price = int(price_text.replace('৳', '').replace(',', '').strip())
            except:
                price = 0 

        regular_price_element = short_info.find_all('li', {'class':'product-mpn'})[1]
        if regular_price_element:
            try:
                regular_price_text = regular_price_element.find_all('span')[1].text.strip()
                regular_price = int(regular_price_text.replace('৳', '').replace(',', '').strip())
            except:
                regular_price = 0

        stock_element = short_info.find('li', {'class':'product-model'})
        if stock_element:
            stock_status = stock_element.find_all('span')[1].text.strip()

        brand_element = short_info.find('li', {'class':'product-manufacturer'})
        if brand_element:
            brand = brand_element.find('a').text.strip()

        model_element = short_info.find_all('li', {'class':'product-model'})[1]
        if model_element:
            model = model_element.find_all('span')[1].text.strip()

    # Extract category and subcategory 
    breadcrumb = soup.find('ul', {'class': 'breadcrumb'})
    if breadcrumb:
        categories = breadcrumb.find_all('a')
        if len(categories) >= 2:
            category = categories[1].text.strip()
            sub_category = categories[2].text.strip()

    # Extract images
    images = []
    main_image_element = soup.find('div', {'class': 'main-image'})
    if main_image_element:
        main_image = main_image_element.find('img')
        if main_image and 'src' in main_image.attrs:
            images.append(main_image['src'])

    # Keep unique images
    images = list(set(images))

    # Extract features
    features = []
    spec_table = soup.find('table')
    if spec_table:
        for row in spec_table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2:
                feature_name = cells[0].text.strip()
                feature_value = cells[1].text.strip().replace('\n', '<br>').replace(';', '<br>').replace('\r', '').replace('&nbsp;', ' ')
                features.append({
                    "name": feature_name,
                    "value": feature_value
                })

    
    # refine data
    model = remove_brand_from_model(brand, model)
    brand = get_brand_from_name(brand, name)
    price = set_prices(price, regular_price)

    return {
        "shop": {
            "name": "skyland",
            "href": "https://www.skyland.com.bd",
            "logo": "https://www.skyland.com.bd/image/cache/wp/gp/skyland-logo-200x42.webp"
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


def load_from_skyland():
    """Load products from Sky Land website."""
    start_time = time.time()
    print("Loading from Sky Land")
    links_data_arr = get_urls_of_xml(os.getenv('SKYLAND_SITEMAP_URL'))

    # Limit to the first 1000 URLs for testing
    # links_data_arr = links_data_arr[:1000]
    
    process_with_parser = partial(process_product_url, parse_function=parse_skyland_product)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
        executor.map(process_with_parser, links_data_arr)
    
    execution_time = time.time() - start_time
    print(f"Loading from Sky Land Complete")
    print(f"Total execution time: {execution_time:.2f} seconds")
    print(f"Processed {len(links_data_arr)} products")
    print(f"Average time per product: {execution_time/len(links_data_arr):.2f} seconds")