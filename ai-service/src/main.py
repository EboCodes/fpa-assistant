# ai-service/src/main.py
"""
AI/NLP Microservice for Educational Assistant
Handles NLP processing, intent recognition, and response generation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

from nlp_processor import NLPProcessor
from intent_recognizer import IntentRecognizer
from response_generator import ResponseGenerator

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize AI components
nlp_processor = NLPProcessor()
intent_recognizer = IntentRecognizer()
response_generator = ResponseGenerator()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'AI Service is running',
        'version': '1.0.0'
    }), 200

@app.route('/api/process', methods=['POST'])
def process_message():
    """
    Process user message and generate response
    
    Expected JSON:
    {
        "message": "user's question",
        "conversationId": "optional conversation ID",
        "context": "optional context"
    }
    """
    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversationId')
        context = data.get('context', {})
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Step 1: Process message with NLP
        logger.info(f"Processing message: {user_message[:50]}...")
        processed = nlp_processor.process(user_message)
        
        # Step 2: Recognize intent
        intent = intent_recognizer.recognize(processed)
        
        # Step 3: Generate response
        response = response_generator.generate(
            user_message=user_message,
            intent=intent,
            context=context
        )
        
        return jsonify({
            'success': True,
            'conversationId': conversation_id,
            'original_message': user_message,
            'processed_message': processed,
            'intent': intent['name'],
            'confidence': intent['confidence'],
            'response': response,
            'suggested_kb_entries': intent.get('suggestions', [])
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({'error': f'Failed to process message: {str(e)}'}), 500

@app.route('/api/intent', methods=['POST'])
def recognize_intent():
    """
    Recognize intent from user message
    
    Expected JSON:
    {
        "message": "user's question"
    }
    """
    try:
        data = request.get_json(silent=True) or {}
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        processed = nlp_processor.process(message)
        intent = intent_recognizer.recognize(processed)
        
        return jsonify({
            'success': True,
            'original_message': message,
            'processed_message': processed,
            'intent': intent['name'],
            'confidence': intent['confidence']
        }), 200
        
    except Exception as e:
        logger.error(f"Error recognizing intent: {str(e)}")
        return jsonify({'error': f'Failed to recognize intent: {str(e)}'}), 500

@app.route('/api/embeddings', methods=['POST'])
def get_embeddings():
    """
    Generate embeddings for semantic search
    
    Expected JSON:
    {
        "texts": ["text1", "text2", ...]
    }
    """
    try:
        data = request.get_json(silent=True) or {}
        texts = data.get('texts', [])
        
        if not texts:
            return jsonify({'error': 'Texts cannot be empty'}), 400
        
        embeddings = nlp_processor.get_embeddings(texts)
        
        return jsonify({
            'success': True,
            'embeddings': embeddings
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        return jsonify({'error': f'Failed to generate embeddings: {str(e)}'}), 500

@app.route('/api/similarity', methods=['POST'])
def calculate_similarity():
    """
    Calculate similarity between texts for KB retrieval
    
    Expected JSON:
    {
        "query": "user's question",
        "kb_entries": [
            {"id": 1, "question": "...", "answer": "..."},
            {"id": 2, "question": "...", "answer": "..."}
        ]
    }
    """
    try:
        data = request.get_json(silent=True) or {}
        query = data.get('query', '').strip()
        kb_entries = data.get('kb_entries', [])
        
        if not query or not kb_entries:
            return jsonify({'error': 'Query and KB entries required'}), 400
        
        # Get embeddings
        query_embedding = nlp_processor.get_embeddings([query])[0]
        
        # Calculate similarity scores
        results = []
        for entry in kb_entries:
            kb_embedding = nlp_processor.get_embeddings([entry['question']])[0]
            similarity = nlp_processor.calculate_cosine_similarity(
                query_embedding, 
                kb_embedding
            )
            results.append({
                'id': entry['id'],
                'question': entry['question'],
                'answer': entry['answer'],
                'similarity_score': float(similarity)
            })
        
        # Sort by similarity score
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results[:5]  # Top 5 matches
        }), 200
        
    except Exception as e:
        logger.error(f"Error calculating similarity: {str(e)}")
        return jsonify({'error': f'Failed to calculate similarity: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', os.getenv('AI_SERVICE_PORT', '5001')))
    DEBUG = os.getenv('DEBUG', 'false').strip().lower() in {'1', 'true', 'yes', 'on'}
    
    logger.info(f"🚀 AI Service starting on http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
