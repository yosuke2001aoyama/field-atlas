# AGENTS.md

## Project
This repository contains Field Atlas, a Streamlit app for collecting, mapping, analyzing, and anonymizing roadtrip and farmstay field notes.

## Product philosophy
Field Atlas is not a social media app.
It is a private field-note and knowledge system that helps the user understand places, preserve observations, and later create carefully anonymized public outputs.

Always preserve the distinction between:
1. Private raw notes
2. AI-organized personal knowledge
3. Anonymized public storytelling

## Privacy rules
Never expose:
- exact addresses
- exact real-time location
- precise future itinerary
- private names
- raw voice transcripts
- employer, school, government, or diplomatic affiliation
- sensitive personal or political comments

When generating public versions:
- generalize location
- generalize date
- remove names
- remove affiliation
- rewrite as anonymous travel reflection
- include a manual review warning

## Coding style
- Use clear, modular Python
- Keep Streamlit UI readable and simple
- Prefer SQLite for MVP storage
- Avoid external paid API requirements
- Do not hardcode secrets
- Do not commit uploads, local databases, or secrets

## Required checks
Before finishing a task:
- Ensure the app can run with `streamlit run app.py`
- Ensure imports are reflected in requirements.txt
- Ensure new folders are created if missing
- Summarize files changed and remaining TODOs
