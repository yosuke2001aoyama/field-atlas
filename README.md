# Field Atlas

Field Atlas is a local Streamlit MVP for personal road-trip and farmstay field notes in the United States.

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

This MVP stores notes, transcripts, photos, audio, and generated outputs locally. Local SQLite files and upload folders may contain private information. Review public versions manually before publishing.

Recommended `.gitignore` entries:

```gitignore
.env
.streamlit/secrets.toml
uploads/
data/*.db
```

## Current MVP Features

- Add field notes with location, category, uploads, transcript, tags, and privacy level
- Add structured farmstay logs
- Seed sample field notes for Louisville, Knoxville, Asheville, Raleigh, and Chicago
- Map notes and farmstay logs with coordinates
- Generate mock AI summaries, context, and before-arrival destination briefs
- Search and filter field notes and farmstay logs
- Generate template exports: podcast script, Substack-style essay, Instagram caption, Japanese diary, English field note, and Markdown archive
- Create rule-based anonymized public versions

## Future Hooks

The code includes clear extension points for:

- OpenAI API integration for real summaries and briefs
- Whisper or other audio transcription
- Address geocoding to latitude/longitude
- Markdown file export
- Publishing selected public notes to a website
- Mobile shortcut capture for quick field notes
