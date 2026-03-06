import os
import time
import requests
from twilio.rest import Client

URL = "https://tapcaps.com/products/xxxxxx-mystery-box"

ACCOUNT_SID = os.environ["ACCOUNT_SID"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]
TWILIO_PHONE = os.environ["TWILIO_PHONE"]
YOUR_PHONE = os.environ["YOUR_PHONE"]

client = Client(ACCOUNT_SID, AUTH_TOKEN)

called = False

while True:
    try:
        r = requests.get(URL)

        if r.status_code == 200 and not called:
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

            called = True

        else:
            print("Still not live:", r.status_code)

    except Exception as e:
        print("Error:", e)

    time.sleep(3)
