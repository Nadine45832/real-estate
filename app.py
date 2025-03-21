from flask import Flask
from flask_cors import CORS
from backend.routes import routes_dh

app = Flask(__name__)
CORS(app)

app.register_blueprint(routes_dh)

# gunicorn app:app

if __name__ == "__main__":
    app.run(debug=True)
