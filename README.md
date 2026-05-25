# Waymark Atlas

Waymark Atlas is a Streamlit web app for personal road-trip, community, and place-based field notes in the United States.

It is designed around three layers:

1. Private raw field notes
2. AI-organized personal knowledge
3. Carefully anonymized public storytelling

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
- `ai_utils.py` - deterministic mock AI summaries, context, and destination briefs
- `privacy_utils.py` - rule-based redaction and public-version helpers
- `export_utils.py` - template-based export generation
- `map_utils.py` - map point preparation and category colors
- `data/` - local SQLite database directory
- `uploads/photos/` - uploaded photos
- `uploads/audio/` - uploaded audio

## Privacy Warning

This app stores notes, transcripts, photos, audio, and generated outputs locally. Local SQLite files and upload folders may contain private information. Review public versions manually before publishing.

Recommended `.gitignore` entries:

```gitignore
.env
.streamlit/secrets.toml
uploads/
data/*.db
```

## Current Features

- Add field notes with location, category, uploads, transcript, tags, and a publishing choice
- Add structured community logs for farmstays, local conversations, shared meals, events, and meaningful encounters
- Seed sample field notes for Louisville, Knoxville, Asheville, Raleigh, and Chicago
- Start from two top-level modes: planning a future journey or reflecting on a completed one
- Search notes and community logs directly from a map-first view
- Generate sourced, high-resolution, photo-backed before-arrival destination briefs with live place suggestions from OpenStreetMap
- Search and filter field notes and community logs
- Generate template exports: podcast script, Substack-style essay, Instagram caption, Japanese diary, English field note, and Markdown archive
- Create rule-based anonymized public versions with a manual review warning

## Future Hooks

The code includes clear extension points for:

- OpenAI API integration for real summaries and briefs
- Whisper or other audio transcription
- Address geocoding to latitude/longitude
- Markdown file export
- Publishing selected public notes to a website
- Mobile shortcut capture for quick field notes
