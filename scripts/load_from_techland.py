import concurrent.futures
import os
from dotenv import load_dotenv
from utils.http_utils import get_urls_of_xml
from utils.product_processor import process_product_url
from utils.product_utils import get_brand_from_name, remove_brand_from_model, set_prices
from functools import partial
import time

def parse_techland_product(soup, url):
    """Parse Techland product data from the BeautifulSoup object."""

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
    name_element = soup.find('div', {'class': 'title page-title'})
    if name_element:
        name = name_element.text.strip()
        # print(f"Name: {name}")

    # Extract category and subcategory
    breadcrumb = soup.find('ul', {'class': 'breadcrumb'})
    if breadcrumb:
        categories = breadcrumb.find_all('a')
        if len(categories) >= 2:
            category = categories[1].text.strip()
            sub_category = categories[2].text.strip()
            # print(f"Category: {category}")
            # print(f"SubCategory: {sub_category}")

    # Extract price, regular price, stock status, brand, model
    details = soup.find('div', {'class': 'product-details'}).find_all('tr')
    for row in details:
        key = row.find_all('td')[0].text.strip().lower()
        value = row.find_all('td')[1].text.strip()
        if key == 'product price':
            try:
                regular_price = int(value.replace(',', '').replace('৳', '').strip())
                # print(f"Regular Price: {regular_price}")
            except:
                regular_price = 0
        elif key == 'special price':
            try:
                price = int(value.replace(',', '').replace('৳', '').strip())
                # print(f"Price: {price}")
            except:
                price = 0
        elif key == 'stock status':
            stock_status = value
            if "discontinued" in stock_status.lower() or "discontinue" in stock_status.lower():
                stock_status = "Discontinued"
            if "pre-order" in stock_status.lower() or "pre order" in stock_status.lower():
                stock_status = "Pre Order"
            # print(f"Stock Status: {stock_status}")
        elif key == 'brand':
            brand_element = row.find_all('td')[1].find('a')
            if brand_element:
                brand = brand_element.text.strip()
                # print(f"Brand: {brand}")
        elif key in ['model', 'product model']:
            model = value
            # print(f"Model: {model}")



    # Extract images
    main_image_container = soup.find('div', {'class': 'swiper main-image'})
    if main_image_container:
        for img in main_image_container.find_all('img'):
            if 'src' in img.attrs:
                images.append(img['src'])
            elif 'data-largeimg' in img.attrs:
                images.append(img['data-largeimg'])
        # print(f"Images: {images}")  

    # Extract features
    feature_table = soup.find('div', {'id': 'tab-specification'})
    if feature_table:
        rows = feature_table.find_all('tr')
        for row in rows:
            name_cell = row.find('td', class_='attribute-name')
            value_cell = row.find('td', class_='attribute-value')
            if name_cell and value_cell:
                feature_name = name_cell.text.strip()
                feature_value = value_cell.text.strip()
                
                # Split feature value by <br> or newline for specific features that need sub-features
                split_features = ['display', 'port', 'features', 'connectivity', 'interface', 'processor', 'battery', 'networking', 'graphics', 'storage', 'memory',]
                if any(f.lower() in feature_name.lower() for f in split_features):
                    sub_features = [f.strip() for f in feature_value.replace('\n', '<br>').split('<br>')]
                    
                    # Process sub-features
                    processed_features = []
                    for sub in sub_features:
                        # Only split if there's a space after the hyphen
                        if ' - ' in sub or '- ' in sub:
                            key, value = sub.split('-', 1)
                            processed_features.append({
                                "name": key.strip(),
                                "value": value.strip()
                            })
                        # Only split if there's a space after or before the colon
                        elif ' : ' in sub or ': ' in sub:
                            key, value = sub.split(':', 1)
                            processed_features.append({
                                "name": key.strip(),
                                "value": value.strip()
                            })
                    if processed_features:
                        features.extend(processed_features)
                        continue
                    
                    # For other features, join with line breaks
                    if len(sub_features) > 1:
                        feature_value = '\r<br>'.join(sub_features)
                    else:
                        feature_value = feature_value.replace('&nbsp;', ' ')
                features.append({
                    "name": feature_name,
                    "value": feature_value
                })
        # print(f"Features: {features}")

    # refine data
    model = remove_brand_from_model(brand, model)
    brand = get_brand_from_name(brand, name)
    price = set_prices(price, regular_price)


    return {
        "shop":{
            "name": "techland",
            "href": "https://www.techlandbd.com",
            "logo": "https://i.imgur.com/AkCgQFa.png"
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

def load_from_techland():
    """Load products from Techland website."""
    start_time = time.time()
    print("Loading from Techland")
    links_data_arr = get_urls_of_xml(os.getenv('TECHLAND_SITEMAP_URL'))

    # Limit to the first 1000 URLs for testing
    # links_data_arr = links_data_arr[:1000]
    
    process_with_parser = partial(process_product_url, parse_function=parse_techland_product)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
        executor.map(process_with_parser, links_data_arr)
    
    execution_time = time.time() - start_time
    print(f"Loading from Techland Complete")
    print(f"Total execution time: {execution_time:.2f} seconds")
    print(f"Processed {len(links_data_arr)} products")
    print(f"Average time per product: {execution_time/len(links_data_arr):.2f} seconds")
