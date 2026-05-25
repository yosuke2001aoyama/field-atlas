from __future__ import annotations

from db import insert_export


def _combine_notes(items: list[dict]) -> str:
    chunks = []
    for item in items:
        title = item.get("display_title") or item.get("title") or item.get("farm_name") or "Untitled"
        location = item.get("display_location") or item.get("location_name") or ""
        text = item.get("display_text") or item.get("note_text") or item.get("reflection") or ""
        summary = item.get("ai_summary") or ""
        chunks.append(f"{title} — {location}\n{text}\n{summary}".strip())
    return "\n\n".join(chunks)


def generate_export(export_type: str, items: list[dict]) -> tuple[str, str]:
    source = _combine_notes(items)
    first_title = items[0].get("display_title") if items else "Waymark U.S. Notes"
    title = f"{export_type}: {first_title}"

    if export_type == "Podcast script":
        content = (
            "Opening hook:\nWhat can one road stop reveal about American life?\n\n"
            f"Scene description:\n{source}\n\n"
            "What I noticed:\nThe details point toward food, work, movement, memory, and local institutions.\n\n"
            "Why it matters:\nSmall observations can show how national stories become daily routines.\n\n"
            "Reflection:\nThe strongest field notes preserve uncertainty while naming what changed in the observer.\n\n"
            "Closing line:\nThis is Waymark U.S., listening to America one place at a time."
        )
    elif export_type == "Substack-style essay":
        content = (
            f"# {first_title}\n\n"
            "## Intro\nA road note often begins as a small scene and becomes a question about place.\n\n"
            f"## Scene\n{source}\n\n"
            "## Observation\nThe useful details are the ordinary ones: what people eat, where they gather, what work structures the day.\n\n"
            "## Broader context\nThis draft can later be expanded with researched history and interviews.\n\n"
            "## Reflection\nThe point is not to explain a place too quickly, but to stay with what it reveals.\n\n"
            "## Ending\nThe atlas grows through careful attention."
        )
    elif export_type == "Instagram caption":
        content = (
            f"{first_title}: a small field note from the road.\n\n"
            "- One local detail changed the mood of the stop.\n"
            "- Food, work, and public space carried more context than expected.\n"
            "- The best observation is still a question.\n\n"
            "#WaymarkUS #RoadNotes #AmericanPlaces #FieldJournal #TravelWriting"
        )
    elif export_type == "Japanese diary":
        content = (
            "今日は、旅先で見た小さな場面がずっと心に残った。華やかな観光地というより、"
            "人々の日常の動きや、食べ物、働く場所、街の空気から、その土地の輪郭が少し見えた気がする。\n\n"
            f"{source}\n\n"
            "まだ結論は出さずに、この違和感や発見を次の場所へ持っていきたい。"
        )
    elif export_type == "English field note":
        content = (
            f"{first_title}\n\n"
            f"{source}\n\n"
            "Field interpretation: This note should remain observational, specific, and modest. It is a record of what was noticed, not a final explanation of the place."
        )
    else:
        content = f"# Waymark U.S. Markdown Archive\n\n{source}"

    return title, content


def save_export(export_type: str, items: list[dict], content: str, title: str) -> int:
    source_ids = [f"{item.get('source_type', 'item')}:{item.get('source_id', item.get('id'))}" for item in items]
    return insert_export(export_type, source_ids, title, content)


# Future hook: write selected exports to Markdown files or publish approved public notes to a website.
