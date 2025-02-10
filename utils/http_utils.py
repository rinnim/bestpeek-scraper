import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    """Fetch HTML content from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    

def get_urls_of_xml(xml_url):
    """Retrieve URLs from an XML sitemap."""
    html = fetch_html(xml_url)
    if html:
        soup = BeautifulSoup(html, features="xml")
        return [link.getText() for link in soup.findAll('loc')]
    return []
