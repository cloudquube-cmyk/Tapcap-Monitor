import os
import requests
from twilio.rest import Client

SEARCH_URL = "https://tapcaps.com/search?q=xxxxxx"

ACCOUNT_SID = os.environ["ACCOUNT_SID"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]
TWILIO_PHONE = os.environ["TWILIO_PHONE"]
YOUR_PHONE = os.environ["YOUR_PHONE"]

client = Client(ACCOUNT_SID, AUTH_TOKEN)

try:
    r = requests.get(SEARCH_URL, timeout=10)

    text = r.text.lower()

    print("Search page checked")

    trigger_words = [
        "add to cart",
        "buy now",
        "available",
        "in stock"
    ]

    if any(word in text for word in trigger_words):
        print("SEARCH SIGNAL DETECTED")

        client.calls.create(
            to=YOUR_PHONE,
            from_=TWILIO_PHONE,
            twiml="""
            <Response>
                <Say>The TapCaps search listing changed. Check the site now.</Say>
            </Response>
            """
        )
    else:
        print("No search signal yet")

except Exception as e:
    print("Error:", e)
