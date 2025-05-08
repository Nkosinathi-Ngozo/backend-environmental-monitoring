from flask import Blueprint, jsonify
import logging


main = Blueprint('main', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@main.route('/api/hello', methods=['GET'])
def hello():
    try:
        return jsonify({'message': 'Hello, World!'})
    except Exception as e:
        logger.error(f"Error toggling alert: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500    