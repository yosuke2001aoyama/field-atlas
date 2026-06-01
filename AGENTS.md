# AGENTS.md

## Project

Waymark U.S. is a private AI field journal for curious travelers.

## Product Rules

- Private-first.
- No public/community features in MVP.
- No Google Form ingestion in MVP.
- No public review functionality.
- Do not drift into a GPS audio tour, trip planner, route tracker, photo journal, or generic AI diary.
- Distinguish user notes from AI-generated briefs.
- Distinguish private notes from public-safe drafts.
- Do not add publishing functionality unless explicitly requested.

## Always Emphasize

- Understand what you see.
- Remember what you notice.
- Ask about what I’m seeing.
- Field notes.
- Memory map of observations.
- Journey synthesis.
- Compare places.
- Export selected insights.

## Tone

- Curious.
- Reflective.
- Observational.
- Practical.
- Private-first.

## Required Navigation

- Home
- Understand
- Ask
- Capture
- Memory Map
- Synthesize
- Library
- Export

## Privacy Rules

- Do not expose exact real-time location.
- Do not expose future itinerary.
- Do not expose private names.
- Do not expose raw transcripts in public-safe drafts.
- Do not expose employer, school, government, or diplomatic affiliation.
- All public outputs are drafts requiring manual review.

## Coding Rules

- Keep Streamlit UI simple and readable.
- Prefer reliable built-in Streamlit inputs over fragile custom components.
- Ensure app runs with `streamlit run app.py`.
- Update `requirements.txt` whenever imports change.
- Avoid hardcoded secrets.
- Do not require `data/` or `uploads/` to exist in GitHub.

## Required Checks

- App runs with `streamlit run app.py`.
- No public/community features reintroduced.
- No audio-tour framing.
- No itinerary-planner framing.
- No route-tracker framing.
- Ask and Synthesize are visible core features.
