#!/usr/bin/env python3
import json
import requests
from datetime import datetime

# Sample webhook payload
webhook_payload = {
    "api_version": "1.0",
    "event": {
        "aliases": ["C4FD158C-48A9-4BEC-9E00-3364D7E7DDFF"],
        "app_id": "appecb325e35e",
        "app_user_id": "C4FD158C-48A9-4BEC-9E00-3364D7E7DDFF",
        "commission_percentage": 0.3,
        "country_code": "US",
        "currency": "USD",
        "entitlement_id": None,
        "entitlement_ids": ["Pro"],
        "environment": "PRODUCTION",
        "event_timestamp_ms": 1754692278482,
        "expiration_at_ms": 1755292276000,
        "id": "8017020E-44A2-4BC7-AE26-75D20A8C8BF1",
        "is_family_share": False,
        "is_trial_conversion": False,
        "metadata": None,
        "offer_code": None,
        "original_app_user_id": "C4FD158C-48A9-4BEC-9E00-3364D7E7DDFF",
        "original_transaction_id": "480002600407555",
        "period_type": "NORMAL",
        "presented_offering_id": "bentelte",
        "price": 9.99,
        "price_in_purchased_currency": 9.99,
        "product_id": "com.vemix.weekly",
        "purchased_at_ms": 1754687476000,
        "renewal_number": 2,
        "store": "APP_STORE",
        "subscriber_attributes": {
            "$attConsentStatus": {
                "updated_at_ms": 1754082681428,
                "value": "notDetermined"
            }
        },
        "takehome_percentage": 0.7,
        "tax_percentage": 0,
        "transaction_id": "480002610028645",
        "type": "RENEWAL"
    }
}

# Test timestamp conversion
event_timestamp_ms = webhook_payload["event"]["event_timestamp_ms"]
print(f"Original timestamp (ms): {event_timestamp_ms}")

# Convert milliseconds to datetime
event_timestamp = datetime.fromtimestamp(event_timestamp_ms / 1000)
print(f"Converted datetime: {event_timestamp}")
print(f"ISO format: {event_timestamp.isoformat()}")

# Test locally
if __name__ == "__main__":
    print("\nTesting webhook endpoint locally...")
    # Uncomment to test against local server
    # response = requests.post("http://localhost:5000/PostBack", json=webhook_payload)
    # print(f"Response status: {response.status_code}")
    # print(f"Response body: {response.json()}")