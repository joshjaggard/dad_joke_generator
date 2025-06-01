from flask import Flask, render_template, jsonify
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

from joke_grabber import joke_grabber

# Configure logging
logging.basicConfig(level=logging.WARNING)

app = Flask(__name__)

# Below is used if a proxy is in front of flask
# If only using WSGI set to 1
# If using a reverse proxy with WSGI set to 2
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/joke')
def api_joke():
    """API endpoint to get a dad joke"""
    try:
        joke_api = 'https://icanhazdadjoke.com'
        joke_text, joke_url = joke_grabber(joke_api)
        
        response_data = {
            'joke': joke_text,
            'source': joke_url,
            'success': True
        }
        
        if joke_url:
            response_data['url'] = joke_url
            
        return jsonify(response_data)
    
    except Exception as e:
        logging.error(f'Error in API endpoint: {e}')
        return jsonify({
            'joke': "Why don't scientists trust atoms? Because they make up everything!",
            'source': None,
            'success': False,
            'error': 'Failed to fetch joke from API'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
