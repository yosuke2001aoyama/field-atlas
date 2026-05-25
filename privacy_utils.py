from __future__ import annotations

import re
from datetime import datetime


SENSITIVE_PATTERNS = [
    (re.compile(r"\b\d{1,6}\s+[A-Z][A-Za-z0-9.\s]+(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr|Boulevard|Blvd|Highway|Hwy)\b"), "[exact address removed]"),
    (re.compile(r"\b(?:diplomat|embassy|consulate|government official|foreign service officer)\b", re.I), "[affiliation removed]"),
    (re.compile(r"\b(?:employer|school|university|agency|department)\s*:\s*[\w\s&.-]+", re.I), "[affiliation removed]"),
    (re.compile(r"\b(?:tomorrow|next week|next month|tonight|later today)\b", re.I), "[future timing removed]"),
    (re.compile(r"\b(?:Democrat|Republican|MAGA|socialist|communist)\b", re.I), "[political detail generalized]"),
]


def generalize_date(date_text: str) -> str:
    if not date_text:
        return "a later, non-real-time moment"
    try:
        parsed = datetime.fromisoformat(date_text)
    except ValueError:
        return "a generalized date"
    month = parsed.strftime("%B")
    if parsed.month in {12, 1, 2}:
        season = "winter"
    elif parsed.month in {3, 4, 5}:
        season = "spring"
    elif parsed.month in {6, 7, 8}:
        season = "summer"
    else:
        season = "fall"
    return f"{month} {parsed.year} ({season})"


def generalize_location(city: str = "", state: str = "", location_name: str = "") -> str:
    state_regions = {
        "North Carolina": "western North Carolina",
        "Tennessee": "eastern Tennessee",
        "Kentucky": "northern Kentucky",
        "Illinois": "northeastern Illinois",
    }
    if state in state_regions:
        return state_regions[state]
    if state:
        return f"a community in {state}"
    if city:
        return f"the broader {city} area"
    if location_name:
        return "a rural or small-town stop in the United States"
    return "a place in the United States"


def redact_private_names(text: str) -> tuple[str, bool]:
    before = text
    text = re.sub(r"\b(?:Mr\.|Mrs\.|Ms\.|Dr\.)\s+[A-Z][a-z]+\b", "[name removed]", text)
    text = re.sub(r"\b[A-Z][a-z]+\s+(?:said|told me|mentioned|explained)\b", "[a person] said", text)
    return text, text != before


def anonymize_text(text: str) -> tuple[str, list[str]]:
    removed: list[str] = []
    public = text or ""

    for pattern, replacement in SENSITIVE_PATTERNS:
        public, count = pattern.subn(replacement, public)
        if count:
            removed.append(replacement.strip("[]"))

    public, names_changed = redact_private_names(public)
    if names_changed:
        removed.append("private names")

    if not public.strip():
        public = "A private raw note was converted into a generalized public reflection."

    return public, sorted(set(removed))


def create_public_version_for_note(note: dict) -> dict[str, object]:
    source_text = "\n\n".join(
        part
        for part in [
            note.get("note_text", ""),
            note.get("audio_transcript", ""),
            note.get("ai_summary", ""),
        ]
        if part
    )
    redacted, removed = anonymize_text(source_text)
    public_location = generalize_location(
        city=note.get("city", ""),
        state=note.get("state", ""),
        location_name=note.get("location_name", ""),
    )
    public_date = generalize_date(note.get("date", ""))

    public_text = (
        f"In {public_location}, during {public_date}, I noticed a small scene that opened onto larger questions about local life.\n\n"
        f"{redacted}\n\n"
        "This public version is intentionally delayed, generalized, and separated from private schedules, exact addresses, and personal identities."
    )

    checklist = [
        "Exact address removed or omitted",
        "Exact date generalized",
        "Private names redacted where detected",
        "Affiliation disclosure avoided",
        "Real-time or future itinerary language removed where detected",
        "Raw transcript treated as private source material",
    ]
    checklist.extend(f"Detected and removed: {item}" for item in removed)

    return {
        "public_title": f"Field note from {public_location}",
        "public_location": public_location,
        "public_text": public_text,
        "removed_checklist": checklist,
    }


def create_public_version_for_farmstay(log: dict) -> str:
    source = "\n\n".join(
        part
        for part in [
            log.get("work_done", ""),
            log.get("people_met", ""),
            log.get("food_eaten", ""),
            log.get("conversation_topics", ""),
            log.get("lifestyle_observations", ""),
            log.get("surprises", ""),
            log.get("reflection", ""),
        ]
        if part
    )
    redacted, _ = anonymize_text(source)
    public_date = generalize_date(log.get("date", ""))
    location = "a community encounter in the United States"
    if log.get("location_name"):
        location = f"a community encounter near {log.get('location_name')}"

    return (
        f"During {public_date}, I spent time at {location}. The exact host, organization, and private identities are withheld.\n\n"
        f"{redacted}\n\n"
        "This version is written as an anonymous travel reflection rather than a real-time report."
    )
