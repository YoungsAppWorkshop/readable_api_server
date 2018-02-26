from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Load default config
app.config.from_object('config')

# Create a Database object
db = SQLAlchemy(app)

# Import api blueprint
from .controllers import api as api_module

# Register blueprint, set its url prefix: app.url/api
app.register_blueprint(api_module, url_prefix='/api')


@app.errorhandler(404)
def route_not_found(e):
    """ Return an error message in JSON when clients trying
        to get access to unavailable API endpoints
    """
    return jsonify({'error': 'No Result Found'}), 404
