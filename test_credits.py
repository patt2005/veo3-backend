import requests
import json

BASE_URL = "http://localhost:5000"

def test_credits_flow():
    print("=== Testing Credits Flow ===\n")
    
    # 1. Create a new user with 50 credits
    print("1. Creating new user with 50 credits...")
    try:
        response = requests.post(f"{BASE_URL}/create-user", json={"credits": 50})
        if response.status_code == 201:
            user_data = response.json()
            user_id = user_data['user_id']
            print(f"✓ User created successfully")
            print(f"  User ID: {user_id}")
            print(f"  Initial credits: {user_data['credits']}")
        else:
            print(f"✗ Failed to create user: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure Flask app is running on port 5000")
        print("  Run: python3 app.py")
        return
    
    print("\n2. Checking user's current credits...")
    response = requests.get(f"{BASE_URL}/get-credits/{user_id}")
    if response.status_code == 200:
        credits_data = response.json()
        print(f"✓ Current credits: {credits_data['credits']}")
    else:
        print(f"✗ Failed to get credits: {response.text}")
    
    print("\n3. Adding 100 credits to the user...")
    response = requests.post(f"{BASE_URL}/add-credits", json={
        "app_user_id": user_id,
        "credits": 100
    })
    if response.status_code == 200:
        add_data = response.json()
        print(f"✓ Credits added successfully")
        print(f"  Credits added: {add_data['credits_added']}")
        print(f"  Total credits: {add_data['total_credits']}")
    else:
        print(f"✗ Failed to add credits: {response.text}")
    
    print("\n4. Verifying final credit balance...")
    response = requests.get(f"{BASE_URL}/get-credits/{user_id}")
    if response.status_code == 200:
        credits_data = response.json()
        print(f"✓ Final credits: {credits_data['credits']}")
        print(f"  Expected: 150 (50 initial + 100 added)")
        print(f"  Actual: {credits_data['credits']}")
        if credits_data['credits'] == 150:
            print("✓ Credit addition working correctly!")
        else:
            print("✗ Credit calculation error!")
    else:
        print(f"✗ Failed to get final credits: {response.text}")

if __name__ == "__main__":
    test_credits_flow()