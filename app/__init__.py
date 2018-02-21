from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load default config
app.config.from_object('config')

# Create a Database object
db = SQLAlchemy(app)

# Import and Register blueprint
from .controllers import api as api_module

app.register_blueprint(api_module, url_prefix='/api')


@app.route('/')
def hello_world():
    return 'Hello, Test!'
