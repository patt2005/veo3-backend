# RevenueCat Webhook Integration

This backend now includes a webhook endpoint for RevenueCat at `/PostBack` that stores subscription data in a PostgreSQL database.

## Setup

1. **Environment Variables**
   Add these to your environment:
   ```
   DATABASE_URL=postgresql://postgres:wMdDBoTrriIEfXSPugzsixIfOwOBtRIi@yamabiko.proxy.rlwy.net:12951/railway
   REVENUECAT_WEBHOOK_SECRET=your_secret_here      # Optional but recommended
   ```

2. **Database Tables**
   The system automatically creates two tables:
   - `subscriptions`: Stores active subscription data
   - `webhook_events`: Logs all webhook events received

3. **RevenueCat Configuration**
   In your RevenueCat dashboard:
   - Go to Project Settings > Webhooks
   - Add webhook URL: `https://veo3-backend-118847640969.europe-west1.run.app/PostBack`
   - Copy the webhook secret and add it to your environment variables

## Supported Events

The webhook handles all RevenueCat event types:
- `INITIAL_PURCHASE` - New subscription created
- `RENEWAL` - Subscription renewed
- `CANCELLATION` - User cancelled (but may still have access until expiration)
- `UNCANCELLATION` - User reactivated cancelled subscription
- `NON_RENEWING_PURCHASE` - One-time purchase
- `EXPIRATION` - Subscription expired
- `PRODUCT_CHANGE` - User changed subscription tier
- `BILLING_ISSUE` - Payment failed
- `SUBSCRIBER_ALIAS` - User ID changed

## Database Schema

### Subscriptions Table
- `id`: Primary key
- `app_user_id`: RevenueCat user ID
- `product_id`: Product identifier
- `entitlement_id`: Entitlement granted
- `store`: APP_STORE, PLAY_STORE, etc.
- `environment`: production/sandbox
- `purchased_at`: Purchase timestamp
- `expires_at`: Expiration timestamp
- `is_active`: Current status
- `is_sandbox`: Test purchase flag
- `is_trial`: Trial subscription flag
- `currency`: Payment currency
- `price`: Amount paid
- `country_code`: User's country

### Webhook Events Table
- `id`: Primary key
- `event_id`: RevenueCat event ID
- `event_type`: Type of event
- `app_user_id`: User affected
- `product_id`: Product involved
- `environment`: production/sandbox
- `event_timestamp`: When event occurred
- `payload`: Full JSON payload
- `processed`: Processing status

## Testing

Use the included `test_webhook.py` script:
```bash
python test_webhook.py
```

## Security

- Webhook signature verification is implemented when `REVENUECAT_WEBHOOK_SECRET` is set
- All events are logged for audit purposes
- Duplicate events are automatically ignored

## Deployment

When deploying to Google Cloud Run:
1. Add DATABASE_URL to your environment (currently configured for Railway PostgreSQL)
2. Add REVENUECAT_WEBHOOK_SECRET to your secrets
3. The endpoint will be available at your Cloud Run URL + `/PostBack`

## Database Connection

The system is configured to use the Railway PostgreSQL database:
- Host: tramway.proxy.rlwy.net
- Port: 40679
- Database: railway
- Connection string is already configured in the code