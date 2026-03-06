import os
import requests
from twilio.rest import Client

PRODUCT_URL = "https://tapcaps.com/products/xxxxxx-mystery-box.js"

PLACEHOLDER_PRICE = "1111.99"

ACCOUNT_SID = os.environ["ACCOUNT_SID"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]
TWILIO_PHONE = os.environ["TWILIO_PHONE"]
YOUR_PHONE = os.environ["YOUR_PHONE"]

client = Client(ACCOUNT_SID, AUTH_TOKEN)

try:
    r = requests.get(PRODUCT_URL, timeout=10)

    if r.status_code != 200:
        print("Product not live yet:", r.status_code)

    else:
        data = r.json()
        variants = data.get("variants", [])

        live = False

        for v in variants:

            price = f'{v["price"] / 100:.2f}'
            inventory = v.get("inventory_quantity", 0)
            available = v.get("available", False)

            print("Price:", price, "| Inventory:", inventory, "| Available:", available)

            if price != PLACEHOLDER_PRICE or inventory > 0 or available:
                live = True

        if live:

            print("DROP DETECTED")

            client.calls.create(
                to=YOUR_PHONE,
                from_=TWILIO_PHONE,
                twiml="""
                <Response>
                    <Say>The TapCaps drop is live. Check the site now.</Say>
                </Response>
                """
            )

        else:
            print("Still placeholder")

except Exception as e:
    print("Error:", e)
