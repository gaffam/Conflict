# Conflict Map

This project collects news from multiple RSS feeds, converts them into a GeoJSON format and visualizes them on an interactive map.

## Components

- `rss_isleyici.py` – Python script that reads feed URLs from `rss_kaynaklari.txt`, detects locations and severity keywords, and outputs `data.geojson`.
- `server.py` – Flask API serving the GeoJSON, the frontend and simple endpoints to manage feeds.
- `harita.html` – React + Leaflet frontend with marker clustering, language toggle and panels for airport info and emergency numbers.
- `ShelterGame.jsx` – a small React component providing a "Guess the Gibberish" style game (see file for standalone usage).
- `rss_kaynaklari.txt` – list of RSS feed URLs.

## Usage

Install dependencies and start the server:

```bash
pip install -r requirements.txt
gunicorn server:app
```
For local development you can also run `python3 server.py`.

Open `http://localhost:8000` in your browser to view the map. Use the floating panels to manage RSS feeds and refresh data.
