# app.py
# Flask REST API for "Ruffel och Båg", manages cars with CRUD operations.
# Data is saved in a JSON file (cars.json) via helper functions in storage.py.

from flask import Flask, request, jsonify

# Import functions for reading/writing and searching in cars.json
from storage import load_cars, save_cars, find_car_by_regnr

# Import validation helper for incoming JSON payloads
from validators import validate_car_payload

# Create Flask application instance
app = Flask(__name__)


@app.get("/")
def home():
    """
    Start endpoint.
    Returns a simple description of the API and available endpoints.
    """
    return jsonify({
        "message": "Ruffel och Båg Cars API",
        "endpoints": {
            "GET /cars": "List all cars",
            "GET /cars/<regnr>": "Get a car by regnr",
            "POST /cars": "Create a car",
            "PUT /cars/<regnr>": "Replace/update a car (full update recommended)",
            "PATCH /cars/<regnr>": "Partial update",
            "DELETE /cars/<regnr>": "Delete a car"
        }
    }), 200


@app.get("/cars")
def get_all_cars():
    """
    READ: Returns all cars stored in cars.json.
    """
    cars = load_cars()
    return jsonify(cars), 200


@app.get("/cars/<regnr>")
def get_car(regnr: str):
    """
    READ: Returns one car by registration number.
    If no car is found, return 404.
    """
    cars = load_cars()
    car = find_car_by_regnr(cars, regnr)

    if not car:
        return jsonify({"error": "Car not found", "regnr": regnr}), 404

    return jsonify(car), 200


@app.post("/cars")
def create_car():
    """
    CREATE: Adds a new car to cars.json.
    - Validates the JSON body
    - Ensures regnr is unique
    - Normalizes regnr
    """
    # Read JSON body safely (silent=True avoids Flask throwing an exception)
    payload = request.get_json(silent=True)

    # Validate full payload (partial=False means required fields must exist)
    is_valid, errors = validate_car_payload(payload, partial=False)
    if not is_valid:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    cars = load_cars()

    # Normalize regnr to avoid duplicates like "abc123" vs "ABC123"
    regnr = str(payload["regnr"]).strip().upper()

    # If regnr already exists, return conflict
    if find_car_by_regnr(cars, regnr):
        return jsonify({"error": "Car already exists", "regnr": regnr}), 409

    # Create the new car object
    new_car = {
        "regnr": regnr,
        "make": payload.get("make"),
        "model": payload.get("model"),
        "year": int(payload.get("year")),
        "color": payload.get("color", ""),
        "price": int(payload["price"]) if "price" in payload and payload["price"] is not None else None
    }

    # Add to list and save to file
    cars.append(new_car)
    save_cars(cars)

    return jsonify(new_car), 201

@app.put("/cars/<regnr>")
def update_car_put(regnr: str):
    """
    PUT: Updates a car by regnr.
    PUT is treated as a full update: required fields must be present.
    If the car does not exist, return 404.
    """
    payload = request.get_json(silent=True)

    # PUT expects full object, partial=False
    is_valid, errors = validate_car_payload(payload, partial=False)
    if not is_valid:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    cars = load_cars()
    existing = find_car_by_regnr(cars, regnr)

    if not existing:
        return jsonify({"error": "Car not found", "regnr": regnr}), 404

    # Keep regnr stable and normalized 
    existing["regnr"] = str(regnr).strip().upper()
    existing["make"] = payload.get("make")
    existing["model"] = payload.get("model")
    existing["year"] = int(payload.get("year"))
    existing["color"] = payload.get("color", "")
    existing["price"] = int(payload["price"]) if "price" in payload and payload["price"] is not None else None

    # Save changes
    save_cars(cars)
    return jsonify(existing), 200


@app.patch("/cars/<regnr>")
def update_car_patch(regnr: str):
    """
    PATCH: Partially updates a car by regnr.
    Only fields included in the payload are updated.
    regnr itself is not allowed to be changed through PATCH.
    """
    payload = request.get_json(silent=True)

    # PATCH allows partial payload, partial=True
    is_valid, errors = validate_car_payload(payload, partial=True)
    if not is_valid:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    cars = load_cars()
    existing = find_car_by_regnr(cars, regnr)

    if not existing:
        return jsonify({"error": "Car not found", "regnr": regnr}), 404

    # Update only provided fields
    for key, value in payload.items():
        if key == "regnr":
            continue

        # Convert numeric fields to int when needed
        if key == "year" and value is not None:
            existing["year"] = int(value)
        elif key == "price":
            existing["price"] = int(value) if value is not None else None
        else:
            existing[key] = value

    # Save changes
    save_cars(cars)
    return jsonify(existing), 200


@app.delete("/cars/<regnr>")
def delete_car(regnr: str):
    """
    DELETE: Removes a car from cars.json by regnr.
    If no car exists, return 404.
    """
    cars = load_cars()
    car = find_car_by_regnr(cars, regnr)

    if not car:
        return jsonify({"error": "Car not found", "regnr": regnr}), 404

    # Remove and save
    cars.remove(car)
    save_cars(cars)

    return jsonify({"message": "Car deleted", "regnr": regnr}), 200


if __name__ == "__main__":
    # Only used when running locally (python app.py).
    # On PythonAnywhere, WSGI will import `app` and serve it as `application`.
    app.run(debug=True)