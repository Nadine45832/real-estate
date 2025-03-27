from flask import Flask, jsonify
from routes import dh_routes
from flask_cors import CORS
import traceback
from werkzeug.exceptions import NotFound

# Configure Flask to use "frontend" folder for HTML templates
app = Flask(__name__)
CORS(app)

# Register Blueprint
app.register_blueprint(dh_routes, url_prefix="/")

# gunicorn app:app



@app.errorhandler(Exception)
def handle_exception(e):
    traceback.print_exc()  # show errors from console
    return jsonify({"error": str(e)}), 500

@app.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)