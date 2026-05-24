from __future__ import annotations

from datetime import datetime


def _first_sentence(text: str, fallback: str = "No raw note text was provided yet.") -> str:
    cleaned = " ".join((text or "").split())
    if not cleaned:
        return fallback
    end = cleaned.find(".")
    return cleaned[: end + 1] if end > 30 else cleaned[:220]


def generate_ai_summary(note_text: str, category: str, location: str) -> str:
    location_label = location or "this place"
    category_label = category or "local life"
    return (
        f"This note captures an observation about {category_label} in {location_label}. "
        "It may be useful for later reflection on local culture, everyday life, and regional identity."
    )


def generate_ai_context(note_text: str, category: str, location: str) -> str:
    seed = _first_sentence(note_text)
    return (
        f"Historical angle: Ask what older settlement, industry, migration, or infrastructure patterns still shape {location or 'the area'}.\n\n"
        f"Cultural signals: Watch how people gather, talk, eat, worship, commute, and mark belonging around {category or 'daily life'}.\n\n"
        "Economic/lifestyle angle: Notice the balance between visitor-facing spaces, working routines, housing, food access, and local institutions.\n\n"
        f"Questions to revisit: What did this scene make visible? Start from this detail: {seed}"
    )


def generate_farmstay_summary(data: dict) -> str:
    farm_type = data.get("farm_type") or "farm"
    location = data.get("location_name") or "the area"
    work = _first_sentence(data.get("work_done", ""), "the day's work")
    return (
        f"This {farm_type} farmstay near {location} records {work.lower()} "
        "It connects physical labor, food systems, rural routines, and the social texture of farm life."
    )


def generate_destination_brief(
    destination: str,
    state: str,
    trip_purpose: str = "",
    interests: list[str] | None = None,
) -> dict[str, str]:
    interests = interests or []
    interest_text = ", ".join(interests) if interests else "local history, food, economy, and everyday life"
    place = ", ".join(part for part in [destination, state] if part)
    purpose = trip_purpose or "field observation"

    return {
        "destination": destination,
        "state": state,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "brief_15_sec": (
            f"Arrive in {place or 'this destination'} as a careful observer: look for the institutions, foods, roads, "
            "work rhythms, and public spaces that explain how people live here."
        ),
        "historical_background": (
            f"For MVP purposes, treat {place or 'this place'} through a layered template: Indigenous history, settlement, "
            "transportation routes, industry, migration, and recent economic change. Later this section can be filled by a real AI call."
        ),
        "cultural_signals": (
            f"Pay attention to signs, church boards, school colors, local newspapers, murals, music, accents, and the gap between tourist images and daily routines. Interests: {interest_text}."
        ),
        "local_food": (
            "Look for diners, markets, gas-station food, seasonal produce, barbecue or regional specialties, and who seems to gather there at different times of day."
        ),
        "local_institutions": (
            "Notice libraries, courthouses, churches, extension offices, farm supply stores, union halls, colleges, sports fields, and community bulletin boards."
        ),
        "questions_to_ask": (
            f"What has changed here in the last ten years? What do outsiders misunderstand? Where do people gather? What work keeps this place running? How does {purpose} change what I notice?"
        ),
        "field_note_prompts": (
            "Record one sound, one sign, one overheard phrase, one meal, one texture of work, one public institution, and one contradiction."
        ),
        "safety_etiquette": (
            "Do not record private conversations without permission. Avoid real-time posting. Ask before photographing people, homes, farms, or workplaces."
        ),
    }


# Future hook: replace deterministic templates with OpenAI API calls once credentials and model policy are configured.
# Future hook: add Whisper or another transcription pipeline for uploaded audio.
