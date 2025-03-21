# app.py
import sys
import os
from flask import Flask
from routes import dh_routes
from flask_cors import CORS

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Configure Flask to use "frontend" folder for HTML templates
app = Flask(__name__)
CORS(app)

app.secret_key = "your_secret_key"

# Register Blueprint
app.register_blueprint(dh_routes, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True)
