from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import logging
import uuid
from models import get_db, User
from webhook_handler import process_webhook_event

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_ID = os.getenv('PROJECT_ID', 'daring-runway-465515-i2')
LOCATION = os.getenv('LOCATION', 'us-central1')

def get_access_token():
    return "Hello, world"

@app.route('/')
def hello_world():
    return jsonify({
        'status': 'active',
        'service': 'Vertex AI Veo Proxy',
        'project_id': PROJECT_ID,
        'supported_models': [
            'veo-2.0-generate-001',
            'veo-3.0-generate-preview',
            'veo-3.0-fast-generate-001'
        ]
    })

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy api'}), 200

@app.route('/projects/<project_id>/locations/<location>/publishers/google/models/<model_id>:predictLongRunning', methods=['POST'])
def predict_long_running(project_id, location, model_id):
    try:
        access_token = get_access_token()
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        model_id = "veo-3.0-fast-generate-001"
        valid_models = ['veo-2.0-generate-001', 'veo-3.0-generate-preview', 'veo-3.0-fast-generate-001']
        if model_id not in valid_models:
            return jsonify({'error': f'Invalid model ID. Must be one of: {valid_models}'}), 400
        
        url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{model_id}:predictLongRunning"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        
        # Log the request details
        print(f"\n=== VERTEX AI REQUEST ===")
        print(f"URL: {url}")
        print(f"Model: {model_id}")
        print(f"Request Body:")
        print(json.dumps(data, indent=2))
        print(f"========================\n")
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n=== VERTEX AI RESPONSE SUCCESS ===")
            print(json.dumps(result, indent=2))
            print(f"==================================\n")
            return jsonify(result)
        else:
            print(f"\n=== VERTEX AI RESPONSE ERROR ===")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            print(f"=================================\n")
            return jsonify({
                'error': 'Failed to generate video',
                'status_code': response.status_code,
                'message': response.text
            }), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/projects/<project_id>/locations/<location>/publishers/google/models/<model_id>:fetchPredictOperation', methods=['POST'])
def fetch_predict_operation(project_id, location, model_id):
    try:
        access_token = get_access_token()

        model_id = "veo-3.0-fast-generate-001"
        
        data = request.get_json()
        if not data or 'operationName' not in data:
            return jsonify({'error': 'operationName is required'}), 400
        
        url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{model_id}:fetchPredictOperation"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                'error': 'Failed to fetch operation status',
                'status_code': response.status_code,
                'message': response.text
            }), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        access_token = get_access_token()
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        model_id = 'veo-3.0-fast-generate-001'
        
        # Build instances array
        instance = {}
        
        # Handle prompt
        if 'prompt' in data:
            instance['prompt'] = data['prompt']

        if 'image' in data:
            image_data = data['image']
            if isinstance(image_data, dict):
                instance['image'] = image_data
            elif isinstance(image_data, str):
                # Assume it's base64 encoded
                instance['image'] = {
                    'bytesBase64Encoded': image_data,
                    'mimeType': data.get('imageMimeType', 'image/jpeg')
                }

        parameters = {
            'aspectRatio': data.get('aspectRatio', '16:9'),
            'durationSeconds': data.get('durationSeconds', 8),
            'enhancePrompt': data.get('enhancePrompt', True),
            'personGeneration': data.get('personGeneration', 'allow_adult'),
            'sampleCount': data.get('sampleCount', 1)
        }

        if 'generateAudio' in data:
            parameters['generateAudio'] = data['generateAudio']
        if 'negativePrompt' in data:
            parameters['negativePrompt'] = data['negativePrompt']
        if 'seed' in data:
            parameters['seed'] = data['seed']
        if 'storageUri' in data:
            parameters['storageUri'] = data['storageUri']
        
        # Construct the request
        veo_request = {
            'instances': [instance],
            'parameters': parameters
        }

        url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{model_id}:predictLongRunning"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        
        # Log the request details
        print(f"\n=== GENERATE VIDEO REQUEST ===")
        print(f"URL: {url}")
        print(f"Model: {model_id}")
        print(f"Request Body:")
        print(json.dumps(veo_request, indent=2))
        print(f"=============================\n")
        
        response = requests.post(url, headers=headers, json=veo_request)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n=== GENERATE VIDEO RESPONSE SUCCESS ===")
            print(json.dumps(result, indent=2))
            print(f"=======================================\n")
            return jsonify(result)
        else:
            print(f"\n=== GENERATE VIDEO RESPONSE ERROR ===")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            print(f"======================================\n")
            return jsonify({
                'error': 'Failed to generate video',
                'status_code': response.status_code,
                'message': response.text
            }), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check-operation', methods=['POST'])
def check_operation_simple():
    try:
        access_token = get_access_token()
        
        data = request.get_json()
        if not data or 'operationName' not in data:
            return jsonify({'error': 'operationName is required'}), 400
        
        operation_name = data['operationName']

        model_id = 'veo-3.0-fast-generate-001'
        if 'veo-2.0-generate-001' in operation_name:
            model_id = 'veo-2.0-generate-001'
        elif 'veo-3.0-generate-preview' in operation_name:
            model_id = 'veo-3.0-generate-preview'
        
        url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{model_id}:fetchPredictOperation"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        
        print(f"\n=== CHECK OPERATION REQUEST ===")
        print(f"URL: {url}")
        print(f"Model: {model_id}")
        print(f"Operation Name: {operation_name}")
        print(f"===============================\n")
        
        response = requests.post(url, headers=headers, json={'operationName': operation_name})
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n=== CHECK OPERATION RESPONSE SUCCESS ===")
            print(json.dumps(result, indent=2))
            print(f"========================================\n")
            return jsonify(result)
        else:
            print(f"\n=== CHECK OPERATION RESPONSE ERROR ===")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            print(f"======================================\n")
            return jsonify({
                'error': 'Failed to check operation status',
                'status_code': response.status_code,
                'message': response.text
            }), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/register-user', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        app_user_id = data.get('app_user_id')
        credits = data.get('credits', 0)
        
        if not app_user_id:
            return jsonify({'error': 'app_user_id is required'}), 400
        
        try:
            user_uuid = uuid.UUID(app_user_id)
        except ValueError:
            return jsonify({'error': 'Invalid UUID format for app_user_id'}), 400
        
        db = next(get_db())
        try:
            existing_user = db.query(User).filter(User.id == user_uuid).first()
            if existing_user:
                return jsonify({'error': 'User already exists', 'user_id': str(existing_user.id)}), 409
            
            new_user = User(
                id=user_uuid,
                credits=credits
            )
            db.add(new_user)
            db.commit()
            
            logger.info(f"Registered new user: {app_user_id} with {credits} credits")
            
            return jsonify({
                'message': 'User registered successfully',
                'user_id': str(new_user.id),
                'credits': new_user.credits
            }), 201
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/get-credits/<app_user_id>', methods=['GET'])
def get_credits(app_user_id):
    try:
        try:
            user_uuid = uuid.UUID(app_user_id)
        except ValueError:
            return jsonify({'error': 'Invalid UUID format for app_user_id'}), 400
        
        db = next(get_db())
        try:
            user = db.query(User).filter(User.id == user_uuid).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            logger.info(f"Retrieved credits for user: {app_user_id} - Credits: {user.credits}")
            
            return jsonify({
                'user_id': str(user.id),
                'credits': user.credits,
                'created_at': user.created_at.isoformat()
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error getting credits: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/add-credits', methods=['POST'])
def add_credits():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        app_user_id = data.get('app_user_id')
        credits_to_add = data.get('credits', 0)
        
        if not app_user_id:
            return jsonify({'error': 'app_user_id is required'}), 400
        
        if credits_to_add <= 0:
            return jsonify({'error': 'Credits must be greater than 0'}), 400
        
        try:
            user_uuid = uuid.UUID(app_user_id)
        except ValueError:
            return jsonify({'error': 'Invalid UUID format for app_user_id'}), 400
        
        db = next(get_db())
        try:
            user = db.query(User).filter(User.id == user_uuid).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            user.credits += credits_to_add
            db.commit()
            
            logger.info(f"Added {credits_to_add} credits for user: {app_user_id} - Total: {user.credits}")
            
            return jsonify({
                'message': 'Credits added successfully',
                'user_id': str(user.id),
                'credits_added': credits_to_add,
                'total_credits': user.credits
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error adding credits: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/use-credits', methods=['POST'])
def use_credits():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        app_user_id = data.get('app_user_id')
        credits_to_use = data.get('credits', 1)
        
        if not app_user_id:
            return jsonify({'error': 'app_user_id is required'}), 400
        
        if credits_to_use <= 0:
            return jsonify({'error': 'Credits must be greater than 0'}), 400
        
        # Validate UUID format
        try:
            user_uuid = uuid.UUID(app_user_id)
        except ValueError:
            return jsonify({'error': 'Invalid UUID format for app_user_id'}), 400
        
        db = next(get_db())
        try:
            # Find user
            user = db.query(User).filter(User.id == user_uuid).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Check if user has enough credits
            if user.credits < credits_to_use:
                return jsonify({
                    'error': 'Insufficient credits',
                    'available_credits': user.credits,
                    'requested_credits': credits_to_use
                }), 400
            
            # Subtract credits
            user.credits -= credits_to_use
            db.commit()
            
            logger.info(f"Used {credits_to_use} credits for user: {app_user_id} - Remaining: {user.credits}")
            
            return jsonify({
                'message': 'Credits used successfully',
                'user_id': str(user.id),
                'credits_used': credits_to_use,
                'remaining_credits': user.credits
            }), 200
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error using credits: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/PostBack', methods=['POST'])
def revenuecat_webhook():
    try:
        event_data = request.get_json()
        if not event_data:
            return jsonify({'error': 'No event data provided'}), 400
        
        event_type = event_data.get('event', {}).get('type', 'Unknown')
        logger.info(f"Received RevenueCat webhook: {event_type}")
        
        logger.debug(f"Full webhook payload: {json.dumps(event_data, indent=2)}")
        
        db = next(get_db())
        try:
            result = process_webhook_event(event_data, db)
            return jsonify(result), 200
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
