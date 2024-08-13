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
    prices = []

    for item in item_elements:
        price_tag = item.find_next('span', class_='money')
        sale_tag = price_tag.find_previous('span', class_='sr-only', text="Sale price") if price_tag else None
        
        if sale_tag:
            prices.append(price_tag.get_text().strip())
        else:
            prices.append(price_tag.get_text().strip() if price_tag else 'N/A')

    if len(prices) < len(item_elements):
        print("Warning: Fewer prices than items found.")
    elif len(prices) > len(item_elements):
        print("Warning: More prices than items found.")
    
    items_with_prices = {}
    for item, price in zip(item_elements, prices):
        item_name = ' '.join(item.stripped_strings)
        items_with_prices[item_name] = price
    
    return items_with_prices

