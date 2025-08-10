import hashlib
import hmac
from datetime import datetime
from sqlalchemy.orm import Session
from models import WebhookEvent, User
import logging

logger = logging.getLogger(__name__)

def process_webhook_event(event_data: dict, db: Session):
    # Extract event data from RevenueCat webhook format
    event = event_data.get('event', {})
    event_type = event.get('type')
    event_id = event.get('id')
    app_user_id = event.get('app_user_id')
    product_id = event.get('product_id')
    
    # Only process RENEWAL events
    if event_type != "RENEWAL":
        logger.info(f"Ignoring non-renewal event type: {event_type}")
        return {"status": "ignored", "event_type": event_type}
    
    # Check if event already processed
    existing_event = db.query(WebhookEvent).filter_by(event_id=event_id).first()
    if existing_event:
        logger.info(f"Event {event_id} already processed")
        return {"status": "already_processed"}
    
    # Store webhook event
    # Handle event_timestamp_ms - RevenueCat sends milliseconds as integer
    event_timestamp_ms = event.get('event_timestamp_ms')
    if event_timestamp_ms:
        if isinstance(event_timestamp_ms, (int, float)):
            # Convert milliseconds to datetime
            event_timestamp = datetime.fromtimestamp(event_timestamp_ms / 1000)
        else:
            # Try to parse as ISO format string if it's a string
            try:
                event_timestamp = datetime.fromisoformat(str(event_timestamp_ms))
            except ValueError:
                event_timestamp = datetime.utcnow()
    else:
        event_timestamp = datetime.utcnow()
    
    webhook_event = WebhookEvent(
        event_id=event_id,
        event_type=event_type,
        app_user_id=app_user_id,
        product_id=product_id,
        environment=event.get('environment', 'production'),
        event_timestamp=event_timestamp,
        payload=event_data
    )
    db.add(webhook_event)
    
    # Process credits for renewal
    if app_user_id and product_id:
        try:
            # Try to parse app_user_id as UUID
            import uuid
            user_uuid = uuid.UUID(app_user_id)
            user = db.query(User).filter(User.id == user_uuid).first()
            
            if user:
                # Add credits based on product_id
                if product_id == "com.vemix.weekly":
                    user.credits += 10
                    logger.info(f"Added 10 credits to user {app_user_id} for weekly subscription renewal")
                elif product_id == "com.vemix.yearly":
                    user.credits += 60
                    logger.info(f"Added 60 credits to user {app_user_id} for yearly subscription renewal")
                else:
                    logger.warning(f"Unknown product_id: {product_id}")
            else:
                logger.error(f"User not found: {app_user_id}")
        except ValueError:
            logger.error(f"Invalid UUID format for app_user_id: {app_user_id}")
    
    webhook_event.processed = True
    db.commit()
    
    return {"status": "processed", "event_id": event_id}