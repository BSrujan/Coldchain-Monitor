# Medication Safety Checker (PBL-III starter)

A small Flask application for demonstrating a healthcare-themed DevSecOps workflow.

## Important safety boundary
The included `data/interactions.json` contains fictional demonstration records only. This is not clinical decision-support software, is not medically validated, and must not be used to make treatment decisions. Do not replace the sample data with real clinical claims without an appropriately qualified clinical review and authoritative data source.

## Files
- `app.py` — Flask web app and JSON API
- `templates/index.html` — browser interface
- `data/interactions.json` — clearly labelled illustrative demo rules
- `Dockerfile` — container build instructions
- `requirements.txt` — Python dependencies

## Run locally
Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Try the demo
Enter these two names:
- Demo Medicine Alpha
- Demo Medicine Beta

The sample data also includes:
- Demo Medicine Gamma + Demo Medicine Delta
- Demo Medicine Alpha + Demo Medicine Epsilon

## API
- `GET /health` — health check
- `POST /api/check` — checks all unique pairs in the submitted list

Example request:

```bash
curl -X POST http://127.0.0.1:5000/api/check \
  -H "Content-Type: application/json" \
  -d '{"medicines":["Demo Medicine Alpha","Demo Medicine Beta"]}'
```

## Build and run with Docker

```bash
docker build -t medication-safety-checker:1.0 .
docker run --rm -p 5000:5000 medication-safety-checker:1.0
```

Open `http://localhost:5000`.

## GitHub upload
Upload the extracted project contents, keeping the `templates` and `data` folders intact. Do not upload `.venv`, passwords, access keys, or other secrets.
