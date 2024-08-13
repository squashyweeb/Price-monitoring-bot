import requests
from config.settings import DISCORD_WEBHOOK_URL

def notify_price_change(item_name, old_price, new_price):
    message = {
        "content": f"**Price Change Detected**\nItem: {item_name}\nOld Price: {old_price}\nNew Price: {new_price}",
    }
    requests.post(DISCORD_WEBHOOK_URL, json=message)
