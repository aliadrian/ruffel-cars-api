from typing import Dict, Any, Tuple, List

REQUIRED_FIELDS = ["regnr", "make", "model", "year"]

def validate_car_payload(payload: Dict[str, Any], partial: bool = False) -> Tuple[bool, List[str]]:
    """
    Validates payload. If partial=True, validates fields that exist.
    Returns (is_valid, errors).
    """
    errors = []

    if not isinstance(payload, dict):
        return False, ["Payload must be a JSON object."]

    # Required fields for create
    if not partial:
        for field in REQUIRED_FIELDS:
            if field not in payload or payload[field] in (None, ""):
                errors.append(f"Missing or empty field: {field}")

    # Validate if present
    if "regnr" in payload:
        if not str(payload["regnr"]).strip():
            errors.append("regnr cannot be empty.")

    if "year" in payload:
        try:
            year = int(payload["year"])
            if year < 1886 or year > 2100:
                errors.append("year must be between 1886 and 2100.")
        except (ValueError, TypeError):
            errors.append("year must be an integer.")

    if "price" in payload:
        try:
            price = int(payload["price"])
            if price < 0:
                errors.append("price must be >= 0.")
        except (ValueError, TypeError):
            errors.append("price must be an integer.")

    return (len(errors) == 0), errors