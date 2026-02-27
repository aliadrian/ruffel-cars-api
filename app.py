# app.py
from flask import Flask, jsonify
from myblueprints.cars_bp import cars_bp

app = Flask(__name__)

@app.get("/")
def home():
    """
    Start endpoint
    Shows API info and endpoints, now including blueprint prefix
    """
    return jsonify({
        "message": "Ruffel och Båg Cars API",
        "endpoints": {
            "GET /api/v1/cars": "List all cars",
            "GET /api/v1/cars/<regnr>": "Get a car by regnr",
            "POST /api/v1/cars": "Create a car",
            "PUT /api/v1/cars/<regnr>": "Full update",
            "PATCH /api/v1/cars/<regnr>": "Partial update",
            "DELETE /api/v1/cars/<regnr>": "Delete a car"
        }
    }), 200

# Register blueprint with url_prefix
app.register_blueprint(cars_bp, url_prefix="/api/v1/cars")

if __name__ == "__main__":
    app.run(debug=True)