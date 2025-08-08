#\!/bin/bash

# 1. Create a new user with 50 credits
echo "1. Creating new user with 50 credits..."
USER_RESPONSE=$(curl -s -X POST http://localhost:5000/create-user \
  -H "Content-Type: application/json" \
  -d '{"credits": 50}')

echo "Response: $USER_RESPONSE"
USER_ID=$(echo $USER_RESPONSE | grep -o '"user_id": "[^"]*' | grep -o '[^"]*$')
echo "Created user ID: $USER_ID"
echo ""

# 2. Check user's current credits
echo "2. Checking user's current credits..."
curl -s -X GET http://localhost:5000/get-credits/$USER_ID | jq '.'
echo ""

# 3. Add 100 credits to the user
echo "3. Adding 100 credits to the user..."
curl -s -X POST http://localhost:5000/add-credits \
  -H "Content-Type: application/json" \
  -d "{\"app_user_id\": \"$USER_ID\", \"credits\": 100}" | jq '.'
echo ""

# 4. Check user's credits again
echo "4. Checking user's credits after addition..."
curl -s -X GET http://localhost:5000/get-credits/$USER_ID | jq '.'
