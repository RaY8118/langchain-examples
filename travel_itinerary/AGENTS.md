# Travel Itinerary

> **NOTE:** I will not modify any code unless you explicitly request it. I’m here to answer your questions and guide you.

## Setup
- Requires Python 3.12 or newer.
- Install deps: `pip install -r requirements.txt`.
- Create a local `.env` from `.env.example` and set your **OpenAI** and **Anthropic** API keys.

## Running the Demo
- `streamlit run app.py`  - Shows a simple text extractor demo; needs a valid OpenRouter key.
- Test extraction from the CLI:  

  ```bash
  python - <<'PY'
  from chains.extractor import extract_from_text
  print(extract_from_text("My trip to Paris..."))
  PY
  ```

## Data
- Sample itineraries are in `data/sample_itineraries/`.
- Loader utilities are in `utils/data_loader.py`.

## Model Code
- All data models live in `models/itinerary.py` and are Pydantic‑based.

## Development
- Code is formatted with Ruff/Black (run `ruff .` if needed).
- No tests are bundled; add them and run via `pytest` when necessary.
