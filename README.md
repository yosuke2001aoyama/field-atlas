# Waymark U.S.

Waymark U.S. is a private AI field journal for curious travelers.

It is not a GPS audio tour, trip planner, route tracker, photo journal, public review app, or generic AI diary. Waymark helps you understand what you see, remember what you notice, and turn rough road notes into maps, comparisons, essays, scripts, diary entries, and field reports.

Core tagline:

> Understand what you see. Remember what you notice.

## Core Features

- Understand a place with "How to read this place" briefs
- Ask about what you are seeing
- Capture private voice/text field notes
- Map questions and observations
- Synthesize recurring themes after a trip
- Export selected insights as essays, scripts, diaries, or public-safe drafts

## What This MVP Is Not

- Not an audio tour
- Not a route tracker
- Not a trip planner
- Not a public review app
- Not a community submission platform
- Not a generic AI diary
- Does not publish content

Public-safe drafts are for manual review and external use only.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app creates its local database and upload folders automatically on first run.

## Files

- `app.py` - Streamlit UI and page navigation
- `db.py` - SQLite schema, sample data, and database helpers
- `ai_utils.py` - deterministic mock AI summaries, observation responses, synthesis hooks, and place briefs
- `privacy_utils.py` - rule-based redaction and public-safe draft helpers
- `export_utils.py` - template-based export generation
- `map_utils.py` - map point preparation and category colors
- `data/` - local SQLite database directory
- `uploads/` - local upload directories

## Privacy Warning

This app stores notes, transcripts, photos, audio, and generated outputs locally. Local SQLite files and upload folders may contain private information.

Do not commit local databases, uploads, `.env` files, or secrets.

Recommended `.gitignore` entries:

```gitignore
.env
.streamlit/secrets.toml
uploads/
data/*.db
```

## Future Work

- Mobile-first capture
- Real OpenAI integration
- Offline note capture
- Better map interactions
- Compare places more deeply
- Fieldwork templates
- Public-safe export pipeline
