import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def parse_items(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    item_elements = soup.find_all('a', href=lambda x: x and '/products/' in x)
    item_price_elements = soup.find_all('div', class_='text-on-sale span.money')

    prices = [price_element.get_text().strip() for price_element in item_price_elements if price_element.get_text().strip()]

    if len(prices) < len(item_elements):
        print("Warning: Fewer prices than items found.")
    
    prices = prices[-len(item_elements):]

    return dict((item.get_text().strip(), price) for item, price in zip(item_elements, prices))