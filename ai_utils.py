from __future__ import annotations

import difflib
import re
from datetime import datetime
from urllib.parse import quote

import requests


HTTP_HEADERS = {
    "User-Agent": "FieldAtlas/1.0 (public Streamlit app; educational field-note tool)"
}

KNOWN_US_DESTINATIONS = [
    "Louisville",
    "Knoxville",
    "Asheville",
    "Raleigh",
    "Chicago",
    "New Orleans",
    "Nashville",
    "Memphis",
    "Charleston",
    "Savannah",
    "Detroit",
    "Pittsburgh",
    "Santa Fe",
    "Tucson",
    "Portland",
    "Seattle",
    "Austin",
    "Marfa",
    "Burlington",
    "Boise",
]

INTEREST_PROMPTS = {
    "history": "older settlement patterns, public memory, preserved buildings, and what local museums choose to emphasize",
    "food": "markets, diners, regional ingredients, farm stands, bakeries, and who gathers around food",
    "race/community": "neighborhood boundaries, civic organizations, churches, schools, migration stories, and whose histories are visible",
    "agriculture": "soil, water, farm supply stores, seasonality, labor, land prices, and local food infrastructure",
    "music": "venues, record shops, church music, festivals, street sound, and regional performance traditions",
    "religion": "church signs, sacred buildings, community calendars, and the social services tied to congregations",
    "economy": "main streets, warehouses, universities, hospitals, logistics, tourism, energy, and housing pressure",
    "small-town life": "courthouses, diners, schools, libraries, local papers, volunteer groups, and informal gathering places",
    "nature": "rivers, ridgelines, fields, trails, weather, ecological edges, and how outdoor life shapes identity",
    "sports": "school colors, stadiums, local teams, sports bars, radio talk, and weekend rhythms",
}

def _first_sentence(text: str, fallback: str = "No raw note text was provided yet.") -> str:
    cleaned = " ".join((text or "").split())
    if not cleaned:
        return fallback
    end = cleaned.find(".")
    return cleaned[: end + 1] if end > 30 else cleaned[:220]


def normalize_destination(destination: str) -> str:
    cleaned = re.sub(r"\s+", " ", (destination or "").strip())
    if not cleaned:
        return ""
    titled = cleaned.title()
    match = difflib.get_close_matches(titled, KNOWN_US_DESTINATIONS, n=1, cutoff=0.78)
    return match[0] if match else titled


def geocode_destination(destination: str, state: str = "") -> dict:
    query = ", ".join(part for part in [destination, state, "United States"] if part)
    if not query.strip():
        return {}
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": query, "format": "jsonv2", "addressdetails": 1, "limit": 1},
            headers=HTTP_HEADERS,
            timeout=8,
        )
        response.raise_for_status()
        results = response.json()
    except Exception:
        return {}
    if not results:
        return {}
    result = results[0]
    address = result.get("address", {})
    return {
        "display_name": result.get("display_name", ""),
        "latitude": float(result["lat"]) if result.get("lat") else None,
        "longitude": float(result["lon"]) if result.get("lon") else None,
        "city": address.get("city") or address.get("town") or address.get("village") or destination,
        "state": address.get("state") or state,
        "source_url": "https://nominatim.openstreetmap.org/",
    }


def search_destination_suggestions(query: str, limit: int = 8) -> list[dict]:
    cleaned = re.sub(r"\s+", " ", (query or "").strip())
    if len(cleaned) < 3:
        return []
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": f"{cleaned}, United States",
                "format": "jsonv2",
                "addressdetails": 1,
                "namedetails": 1,
                "countrycodes": "us",
                "limit": limit,
            },
            headers=HTTP_HEADERS,
            timeout=8,
        )
        response.raise_for_status()
        results = response.json()
    except Exception:
        return []

    suggestions: list[dict] = []
    seen = set()
    for result in results:
        address = result.get("address", {})
        state = address.get("state", "")
        name = (
            result.get("namedetails", {}).get("name")
            or address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
            or address.get("county")
            or result.get("name")
            or cleaned.title()
        )
        place_type = result.get("type") or result.get("class") or "place"
        if result.get("class") in {"leisure", "boundary", "tourism"} or "park" in place_type:
            place_type = "park / landmark"
        key = (name, state, round(float(result.get("lat", 0)), 3), round(float(result.get("lon", 0)), 3))
        if key in seen:
            continue
        seen.add(key)
        label = " — ".join(part for part in [name, state] if part)
        if place_type:
            label = f"{label} · {place_type}"
        suggestions.append(
            {
                "label": label,
                "destination": name,
                "state": state,
                "display_name": result.get("display_name", label),
                "latitude": float(result["lat"]) if result.get("lat") else None,
                "longitude": float(result["lon"]) if result.get("lon") else None,
                "source_url": "https://nominatim.openstreetmap.org/",
            }
        )
    return suggestions


def fetch_wikipedia_summary(title: str) -> dict:
    if not title:
        return {}
    try:
        response = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title.replace(' ', '_'))}",
            headers=HTTP_HEADERS,
            timeout=8,
        )
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        data = response.json()
    except Exception:
        return {}
    if data.get("type") == "disambiguation":
        return {}
    image_url = (
        data.get("originalimage", {}).get("source")
        or data.get("thumbnail", {}).get("source", "")
    )
    return {
        "title": data.get("title", title),
        "extract": data.get("extract", ""),
        "description": data.get("description", ""),
        "url": data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{quote(title)}"),
        "image_url": image_url,
        "source_name": "Wikipedia",
    }


def fetch_related_wikipedia_topics(destination: str, state: str, interests: list[str]) -> list[dict]:
    topics = [destination]
    if state:
        topics.append(state)
        topics.append(f"{destination}, {state}")
    for interest in interests[:4]:
        if interest == "food":
            topics.append(f"Cuisine of {state}" if state else "Cuisine of the United States")
        elif interest == "agriculture":
            topics.append(f"Agriculture in {state}" if state else "Agriculture in the United States")
        elif interest == "music":
            topics.append(f"Music of {state}" if state else "Music of the United States")
        elif interest == "history":
            topics.append(f"History of {state}" if state else f"History of {destination}")
    summaries = []
    seen_urls = set()
    for topic in topics:
        summary = fetch_wikipedia_summary(topic)
        if summary and summary.get("url") not in seen_urls and summary.get("extract"):
            summaries.append(summary)
            seen_urls.add(summary["url"])
        if len(summaries) >= 4:
            break
    return summaries


def build_source_list(*source_groups: list[dict]) -> list[dict]:
    sources: list[dict] = []
    seen = set()
    for group in source_groups:
        for item in group:
            url = item.get("url") or item.get("source_url")
            if url and url not in seen:
                if item.get("source_name") and item.get("title"):
                    name = f"{item['source_name']}: {item['title']}"
                else:
                    name = item.get("source_name") or item.get("name") or item.get("title") or url
                sources.append({"name": name, "url": url})
                seen.add(url)
    return sources


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
    farm_type = data.get("farm_type") or "community encounter"
    location = data.get("location_name") or "the area"
    work = _first_sentence(data.get("work_done", ""), "what happened")
    return (
        f"This {farm_type} near {location} records {work.lower()} "
        "It connects local interaction, hospitality, work or daily routines, and the social texture of place."
    )


def generate_destination_brief(
    destination: str,
    state: str,
    trip_purpose: str = "",
    interests: list[str] | None = None,
) -> dict[str, str]:
    interests = interests or []
    corrected_destination = normalize_destination(destination)
    geo = geocode_destination(corrected_destination, state)
    suggested_state = geo.get("state") or state
    place = ", ".join(part for part in [corrected_destination, suggested_state] if part)
    purpose = trip_purpose or "field observation"
    summaries = fetch_related_wikipedia_topics(corrected_destination, suggested_state, interests)
    primary = summaries[0] if summaries else {}
    interest_text = ", ".join(interests) if interests else "history, food, economy, and everyday life"
    source_notes = " ".join(item.get("extract", "") for item in summaries[:3])
    if not source_notes:
        source_notes = f"{place} should be approached through public institutions, roads, foodways, work routines, and local memory."
    image_url = next((item.get("image_url") for item in summaries if item.get("image_url")), "")
    sources = build_source_list(
        summaries,
        [{"name": "OpenStreetMap Nominatim", "source_url": "https://nominatim.openstreetmap.org/"}],
    )

    return {
        "destination": corrected_destination,
        "state": suggested_state,
        "latitude": geo.get("latitude"),
        "longitude": geo.get("longitude"),
        "display_name": geo.get("display_name", place),
        "image_url": image_url,
        "source_summaries": summaries,
        "sources": sources,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "brief_15_sec": (
            f"Arrive in {place or 'this destination'} as a careful observer: use the streets, food places, public institutions, landscape, and work rhythms as clues to how local life is organized."
        ),
        "historical_background": (
            f"Public reference material frames {place or 'this place'} through these starting points: {source_notes[:900]}"
        ),
        "cultural_signals": (
            f"Watch signs, school colors, local newspapers, murals, church boards, storefronts, accents, music, and the gap between visitor imagery and daily routine. Your stated interests: {interest_text}."
        ),
        "local_food": (
            "Look for diners, markets, gas-station food, seasonal produce, regional specialties, immigrant foodways, bakeries, and who seems to gather there at different times of day."
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
