## Cars REST API (Flask)

Ett enkelt Flask REST API med CRUD för att hantera bilar. Data lagras i `cars.json`.
Registreringsnummer (`regnr`) används som unik nyckel för uppdatering och borttagning.

## Installera och starta lokalt

```bash
python -m venv venv
source venv/bin/activate  # mac/linux
# venv\Scripts\activate   # windows

pip install -r requirements.txt
python app.py

```

## Endpoints

    •	GET / – start/info
    •	GET /cars – lista alla bilar
    •	GET /cars/<regnr> – hämta en bil
    •	POST /cars – skapa bil (regnr måste vara unikt)
    •	PUT /cars/<regnr> – full uppdatering
    •	PATCH /cars/<regnr> – delvis uppdatering
    •	DELETE /cars/<regnr> – radera bil
