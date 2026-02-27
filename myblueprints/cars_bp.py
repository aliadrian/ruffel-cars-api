from flask import Blueprint, request, jsonify
from storage import load_cars, save_cars, find_car_by_regnr
from validators import validate_car_payload

cars_bp = Blueprint("cars_bp", __name__)

@cars_bp.get("/")
def list_cars():
    """GET /api/v1/cars/ - List all cars."""
    cars = load_cars()
    return jsonify(cars), 200

@cars_bp.get("/<regnr>")
def get_car(regnr: str):
    """GET /api/v1/cars/<regnr> - Get one car by registration number."""
    cars = load_cars()
    car = find_car_by_regnr(cars, regnr)
    if not car:
        return jsonify({"error": "Car not found", "regnr": regnr}), 404
    return jsonify(car), 200

@cars_bp.post("/")
def create_car():
    """POST /api/v1/cars/ - Create a new car."""
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

@cars_bp.put("/<regnr>")
def update_car_put(regnr: str):
    """PUT /api/v1/cars/<regnr> - Full update (replace) of a car."""
    payload = request.get_json(silent=True)
    is_valid, errors = validate_car_payload(payload, partial=False)
    if not is_valid:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    cars = load_cars()
    existing = find_car_by_regnr(cars, regnr)
    if not existing:
        return jsonify({"error": "Car not found", "regnr": regnr}), 404

    existing["regnr"] = str(regnr).strip().upper()
    existing["make"] = payload.get("make")
    existing["model"] = payload.get("model")
    existing["year"] = int(payload.get("year"))
    existing["color"] = payload.get("color", "")
    existing["price"] = int(payload["price"]) if "price" in payload and payload["price"] is not None else None

    save_cars(cars)
    return jsonify(existing), 200

@cars_bp.patch("/<regnr>")
def update_car_patch(regnr: str):
    """PATCH /api/v1/cars/<regnr> - Partial update of a car."""
    payload = request.get_json(silent=True)
    is_valid, errors = validate_car_payload(payload, partial=True)
    if not is_valid:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    cars = load_cars()
    existing = find_car_by_regnr(cars, regnr)
    if not existing:
        return jsonify({"error": "Car not found", "regnr": regnr}), 404

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

@cars_bp.delete("/<regnr>")
def delete_car(regnr: str):
    """DELETE /api/v1/cars/<regnr> - Delete a car by regnr."""
    cars = load_cars()
    car = find_car_by_regnr(cars, regnr)
    if not car:
        return jsonify({"error": "Car not found", "regnr": regnr}), 404

    cars.remove(car)
    save_cars(cars)
    return jsonify({"message": "Car deleted", "regnr": regnr}), 200