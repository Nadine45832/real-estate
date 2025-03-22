from flask import Flask
from routes import dh_routes
from flask_cors import CORS

# Configure Flask to use "frontend" folder for HTML templates
app = Flask(__name__)
CORS(app)

# Register Blueprint
app.register_blueprint(dh_routes, url_prefix="/")

# gunicorn app:app

if __name__ == "__main__":
    app.run(debug=True)
