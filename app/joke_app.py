import logging
from pathlib import Path
from flask import Flask, render_template, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

from joke_grabber import joke_grabber

# Configure logging
logging.basicConfig(level=logging.WARNING)

def get_version():
    """Get app version"""
    # Look for app_version file from Docker build arg
    version_file = Path('app_version')
    if version_file.exists():
        return version_file.read_text().strip()

    # Return default version value if file doesn't exist
    return 'flask-dev-build'

APP_VERSION = get_version()
logging.debug(f'APP_VERSION var = {APP_VERSION}')

app = Flask(__name__)

# Below is used if a proxy is in front of flask
# If only using WSGI set to 1
# If using a reverse proxy with WSGI set to 2
proxy_num = 1
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=proxy_num, x_proto=proxy_num, x_host=proxy_num, x_prefix=proxy_num
)

@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html', joke_app_version=APP_VERSION)

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
