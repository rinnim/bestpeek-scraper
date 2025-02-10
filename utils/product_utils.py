import re

def remove_brand_from_model(brand, model):
    """Remove brand from model."""
    brand = brand.lower().replace(' ', '').replace('-', '').strip()
    model = model.lower().replace(brand, '').strip().upper()
    return re.sub(r'\([^()]*\)', '', model)

def set_prices(price, regular_price):
    """Set the price based on business rules."""
    if price > regular_price:
        price = regular_price
    if price == 0:
        price = regular_price
    return price

def get_brand_from_name(brand, name):
    """Get brand from name if brand is empty."""
    if not brand and name:
        return name.split()[0]
    return brand
