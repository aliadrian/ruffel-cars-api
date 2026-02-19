import json
import os
from typing import List, Dict, Any

FILE_PATH = "cars.json"

def ensure_file_exists() -> None:
    # Creates cars.json if it doesn't exist.
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def load_cars() -> List[Dict[str, Any]]:
    # Loads cars from cars.json.
    ensure_file_exists()
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            # If file is corrupted/empty, fallback to empty list
            return []

def save_cars(cars: List[Dict[str, Any]]) -> None:
    # Saves cars to cars.json.
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)

def find_car_by_regnr(cars: List[Dict[str, Any]], regnr: str):
    regnr_upper = regnr.strip().upper()
    for car in cars:
        if str(car.get("regnr", "")).strip().upper() == regnr_upper:
            return car
    return None