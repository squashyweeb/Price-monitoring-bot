import time
import json
import os
from src.fetcher import fetch_page, parse_items
from src.notifier import notify_price_change
from config.settings import BASE_URL, TOTAL_PAGES, CHECK_INTERVAL

def scrape_items(base_url, total_pages):
    all_items = {}
    for page in range(1, total_pages + 1):
        print(f"Scraping page {page}...")
        url = f"{base_url}?page={page}"
        page_content = fetch_page(url)
        if page_content:
            items = parse_items(page_content)
            all_items.update(items)
        time.sleep(1)
    return all_items

def monitor_prices():
    # Check if the old_prices.json file exists and is not empty
    if os.path.exists('data/old_prices.json') and os.path.getsize('data/old_prices.json') > 0:
        with open('data/old_prices.json', 'r') as f:
            try:
                old_prices = json.load(f)
            except json.JSONDecodeError:
                print("Error: old_prices.json is not a valid JSON file. Recreating it.")
                old_prices = scrape_items(BASE_URL, TOTAL_PAGES)
    else:
        old_prices = scrape_items(BASE_URL, TOTAL_PAGES)
    
    while True:
        new_prices = scrape_items(BASE_URL, TOTAL_PAGES)
        
        for item_name, new_price in new_prices.items():
            old_price = old_prices.get(item_name)
            if old_price and old_price != new_price:
                notify_price_change(item_name, old_price, new_price)
        
        old_prices = new_prices
        
        with open('data/old_prices.json', 'w') as f:
            json.dump(old_prices, f)
        
        time.sleep(CHECK_INTERVAL)
