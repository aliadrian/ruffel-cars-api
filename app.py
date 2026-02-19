from flask import Flask, request, jsonify
from storage import load_cars, save_cars, find_car_by_regnr
from validators import validate_car_payload

app = Flask(__name__)

@app.get("/")
def home():
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
    cars = load_cars()
    return jsonify(cars), 200

@app.get("/cars/<regnr>")
def get_car(regnr: str):
    cars = load_cars()
    car = find_car_by_regnr(cars, regnr)
    if not car:
        return jsonify({"error": "Car not found", "regnr": regnr}), 404
    return jsonify(car), 200

@app.post("/cars")
def create_car():
    payload = request.get_json(silent=True)
    is_valid, errors = validate_car_payload(payload, partial=False)
    if not is_valid:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    cars = load_cars()
    regnr = str(payload["regnr"]).strip().upper()

    if find_car_by_regnr(cars, regnr):
        return jsonify({"error": "Car already exists", "regnr": regnr}), 409

    new_car = {
        "regnr": regnr,
        "make": payload.get("make"),
        "model": payload.get("model"),
        "year": int(payload.get("year")),
        "color": payload.get("color", ""),
        "price": int(payload["price"]) if "price" in payload and payload["price"] is not None else None
    }

    cars.append(new_car)
    save_cars(cars)

    return jsonify(new_car), 201

@app.put("/cars/<regnr>")
def update_car_put(regnr: str):
    payload = request.get_json(silent=True)
    # PUT: we expect full object (recommended)
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

    save_cars(cars)
    return jsonify(existing), 200

@app.patch("/cars/<regnr>")
def update_car_patch(regnr: str):
    payload = request.get_json(silent=True)
    is_valid, errors = validate_car_payload(payload, partial=True)
    if not is_valid:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    cars = load_cars()
    existing = find_car_by_regnr(cars, regnr)
    if not existing:
        return jsonify({"error": "Car not found", "regnr": regnr}), 404

    # Update only provided fields (except regnr)
    for key, value in payload.items():
        if key == "regnr":
            continue
        if key == "year" and value is not None:
            existing["year"] = int(value)
        elif key == "price":
            existing["price"] = int(value) if value is not None else None
        else:
            existing[key] = value

    save_cars(cars)
    return jsonify(existing), 200

@app.delete("/cars/<regnr>")
def delete_car(regnr: str):
    cars = load_cars()
    car = find_car_by_regnr(cars, regnr)
    if not car:
        return jsonify({"error": "Car not found", "regnr": regnr}), 404

    cars.remove(car)
    save_cars(cars)
    return jsonify({"message": "Car deleted", "regnr": regnr}), 200

if __name__ == "__main__":
    app.run(debug=True)