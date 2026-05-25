from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "field_atlas.db"


FIELD_NOTE_COLUMNS = [
    "title",
    "date",
    "location_name",
    "address",
    "latitude",
    "longitude",
    "city",
    "state",
    "category",
    "note_text",
    "photo_path",
    "audio_path",
    "audio_transcript",
    "ai_summary",
    "ai_context",
    "tags",
    "privacy_level",
]

FARMSTAY_COLUMNS = [
    "date",
    "farm_name",
    "location_name",
    "latitude",
    "longitude",
    "farm_type",
    "work_done",
    "people_met",
    "food_eaten",
    "conversation_topics",
    "lifestyle_observations",
    "labor_intensity",
    "community_feeling",
    "surprises",
    "reflection",
    "ai_summary",
    "public_version",
]

AI_BRIEF_COLUMNS = [
    "destination",
    "state",
    "generated_at",
    "brief_15_sec",
    "historical_background",
    "cultural_signals",
    "local_food",
    "local_institutions",
    "questions_to_ask",
    "field_note_prompts",
    "safety_etiquette",
]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ensure_directories() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "uploads" / "photos").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "uploads" / "audio").mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    ensure_directories()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS field_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                date TEXT,
                location_name TEXT,
                address TEXT,
                latitude REAL,
                longitude REAL,
                city TEXT,
                state TEXT,
                category TEXT,
                note_text TEXT,
                photo_path TEXT,
                audio_path TEXT,
                audio_transcript TEXT,
                ai_summary TEXT,
                ai_context TEXT,
                tags TEXT,
                privacy_level TEXT,
                created_at TEXT,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS farmstay_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                farm_name TEXT,
                location_name TEXT,
                latitude REAL,
                longitude REAL,
                farm_type TEXT,
                work_done TEXT,
                people_met TEXT,
                food_eaten TEXT,
                conversation_topics TEXT,
                lifestyle_observations TEXT,
                labor_intensity INTEGER,
                community_feeling INTEGER,
                surprises TEXT,
                reflection TEXT,
                ai_summary TEXT,
                public_version TEXT,
                created_at TEXT,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS ai_briefs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination TEXT,
                state TEXT,
                generated_at TEXT,
                brief_15_sec TEXT,
                historical_background TEXT,
                cultural_signals TEXT,
                local_food TEXT,
                local_institutions TEXT,
                questions_to_ask TEXT,
                field_note_prompts TEXT,
                safety_etiquette TEXT
            );

            CREATE TABLE IF NOT EXISTS exports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                export_type TEXT,
                source_note_ids TEXT,
                title TEXT,
                content TEXT,
                created_at TEXT
            );
            """
        )


def seed_sample_data() -> None:
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM field_notes").fetchone()[0]

        samples = [
            {
                "title": "Riverfront evening in Louisville",
                "date": "2026-04-02",
                "location_name": "Louisville riverfront",
                "address": "",
                "latitude": 38.2592,
                "longitude": -85.7516,
                "city": "Louisville",
                "state": "Kentucky",
                "category": "landscape",
                "note_text": "At the Louisville riverfront, the Ohio River made the city feel less like a single downtown and more like a crossing point. The bridges, walking paths, and older industrial edges sat beside families, runners, and visitors taking photos near the water. The useful observation was the overlap: infrastructure as scenery, leisure beside logistics, and a regional identity shaped by movement across the river.",
                "tags": "river,city,evening,infrastructure",
            },
            {
                "title": "Knoxville diner counter",
                "date": "2026-04-05",
                "location_name": "Downtown Knoxville",
                "address": "",
                "latitude": 35.9606,
                "longitude": -83.9207,
                "city": "Knoxville",
                "state": "Tennessee",
                "category": "food",
                "note_text": "A Knoxville breakfast counter showed how quickly an everyday food place becomes a civic room. The scene was ordinary: coffee refills, talk about weather and road work, orange sports references, and people moving in and out before work. It felt like a useful place to study how a university town, Appalachian proximity, and downtown redevelopment meet in daily routine.",
                "tags": "breakfast,conversation,sports,downtown",
            },
            {
                "title": "Asheville market morning",
                "date": "2026-04-08",
                "location_name": "Asheville farmers market",
                "address": "",
                "latitude": 35.5951,
                "longitude": -82.5515,
                "city": "Asheville",
                "state": "North Carolina",
                "category": "farm",
                "note_text": "In Asheville, the farmers market mixed practical food shopping with the region's strong visitor economy. The stalls made local agriculture visible, but also raised questions about affordability, land pressure, climate, and the line between regional culture and curated lifestyle. The best detail was how vendors talked about weather and soil as casually as others talk about traffic.",
                "tags": "market,local food,craft,agriculture",
            },
            {
                "title": "Raleigh neighborhood walk",
                "date": "2026-04-12",
                "location_name": "Raleigh neighborhood",
                "address": "",
                "latitude": 35.7796,
                "longitude": -78.6382,
                "city": "Raleigh",
                "state": "North Carolina",
                "category": "neighborhood",
                "note_text": "A Raleigh neighborhood walk showed the layered feel of a fast-growing Southern city: new apartments, shaded older streets, small churches, research-economy confidence, and signs of rising housing pressure. The place did not read as simply old or new. It felt like a city negotiating how much of its older civic texture can remain visible during rapid growth.",
                "tags": "growth,churches,city,housing",
            },
            {
                "title": "Chicago station arrival",
                "date": "2026-04-18",
                "location_name": "Chicago Union Station area",
                "address": "",
                "latitude": 41.8781,
                "longitude": -87.6298,
                "city": "Chicago",
                "state": "Illinois",
                "category": "road",
                "note_text": "Arriving near Chicago Union Station made the city feel dense before it felt tall. The first impression was not the skyline, but rhythm: commuters, luggage, food halls, office workers, and the choreography of trains and streets. The station area worked as a compressed field note on scale, migration, labor, and the everyday machinery of a major American city.",
                "tags": "arrival,transit,city,station",
            },
        ]

        timestamp = now_iso()
        for sample in samples:
            sample.setdefault("photo_path", "")
            sample.setdefault("audio_path", "")
            sample.setdefault("audio_transcript", "")
            sample.setdefault(
                "ai_summary",
                f"This note captures a public-ready field observation about {sample['category']} in {sample['location_name']}. It is useful for reflection on local culture, everyday life, infrastructure, and regional identity.",
            )
            sample.setdefault(
                "ai_context",
                "Historical angle: Look for how older infrastructure shapes the present.\n"
                "Cultural signals: Notice routines, gathering places, local speech, signs, and public institutions.\n"
                "Economic/lifestyle angle: Compare visitor-facing spaces with everyday services, housing, work, and mobility.\n"
                "Questions to revisit: What does this place make easy, and what does it make difficult?",
            )
            sample.setdefault("privacy_level", "public-ready")

            if count:
                conn.execute(
                    """
                    UPDATE field_notes
                    SET note_text = ?, tags = ?, privacy_level = ?, ai_summary = ?, ai_context = ?, updated_at = ?
                    WHERE title = ?
                    """,
                    (
                        sample["note_text"],
                        sample["tags"],
                        sample["privacy_level"],
                        sample["ai_summary"],
                        sample["ai_context"],
                        timestamp,
                        sample["title"],
                    ),
                )
            else:
                values = [sample.get(column, "") for column in FIELD_NOTE_COLUMNS]
                placeholders = ", ".join(["?"] * (len(FIELD_NOTE_COLUMNS) + 2))
                conn.execute(
                    f"""
                    INSERT INTO field_notes ({", ".join(FIELD_NOTE_COLUMNS)}, created_at, updated_at)
                    VALUES ({placeholders})
                    """,
                    [*values, timestamp, timestamp],
                )

        farm_count = conn.execute("SELECT COUNT(*) FROM farmstay_logs").fetchone()[0]
        timestamp = now_iso()
        farm_sample = {
                "date": "2026-04-10",
                "farm_name": "Blue Ridge community lunch",
                "location_name": "Blue Ridge foothills",
                "latitude": 35.5951,
                "longitude": -82.5515,
                "farm_type": "community event",
                "work_done": "Washed greens, helped sort seedlings, and observed how weather shaped the day's work plan.",
                "people_met": "A vendor, a neighbor, and a visitor talked without private names recorded.",
                "food_eaten": "Simple lunch with seasonal vegetables, bread, and coffee.",
                "conversation_topics": "Soil, labor, market prices, rainfall, tourism, and the challenge of keeping local food accessible.",
                "lifestyle_observations": "The day moved by weather, light, tools, shared meals, and practical cooperation rather than by a fixed office rhythm.",
                "labor_intensity": 4,
                "community_feeling": 4,
                "surprises": "The amount of invisible planning behind a small market table.",
                "reflection": "The encounter made local agriculture feel less like scenery and more like a daily negotiation among land, weather, bodies, money, and community.",
                "ai_summary": "This community log connects shared food, local work, rural routines, and the social texture of place.",
                "public_version": "During spring 2026, I spent time in a community food setting in the Blue Ridge foothills. The exact host or organization and private identities are withheld. The public lesson was about how much planning, weather awareness, and cooperation sit behind local food and community life.",
        }
        if farm_count:
            conn.execute(
                """
                UPDATE farmstay_logs
                SET farm_name = ?, farm_type = ?, people_met = ?, reflection = ?, ai_summary = ?, public_version = ?, updated_at = ?
                WHERE farm_name IN ('Public sample vegetable farm', 'Blue Ridge community lunch')
                """,
                (
                    farm_sample["farm_name"],
                    farm_sample["farm_type"],
                    farm_sample["people_met"],
                    farm_sample["reflection"],
                    farm_sample["ai_summary"],
                    farm_sample["public_version"],
                    timestamp,
                ),
            )
        else:
            values = [farm_sample.get(column, "") for column in FARMSTAY_COLUMNS]
            conn.execute(
                f"""
                INSERT INTO farmstay_logs ({", ".join(FARMSTAY_COLUMNS)}, created_at, updated_at)
                VALUES ({", ".join(["?"] * (len(FARMSTAY_COLUMNS) + 2))})
                """,
                [*values, timestamp, timestamp],
            )


def initialize_app() -> None:
    init_db()
    seed_sample_data()


def insert_field_note(data: dict[str, Any]) -> int:
    timestamp = now_iso()
    payload = {column: data.get(column, "") for column in FIELD_NOTE_COLUMNS}
    with get_connection() as conn:
        cursor = conn.execute(
            f"""
            INSERT INTO field_notes ({", ".join(FIELD_NOTE_COLUMNS)}, created_at, updated_at)
            VALUES ({", ".join(["?"] * (len(FIELD_NOTE_COLUMNS) + 2))})
            """,
            [*payload.values(), timestamp, timestamp],
        )
        return int(cursor.lastrowid)


def insert_farmstay_log(data: dict[str, Any]) -> int:
    timestamp = now_iso()
    payload = {column: data.get(column, "") for column in FARMSTAY_COLUMNS}
    with get_connection() as conn:
        cursor = conn.execute(
            f"""
            INSERT INTO farmstay_logs ({", ".join(FARMSTAY_COLUMNS)}, created_at, updated_at)
            VALUES ({", ".join(["?"] * (len(FARMSTAY_COLUMNS) + 2))})
            """,
            [*payload.values(), timestamp, timestamp],
        )
        return int(cursor.lastrowid)


def insert_ai_brief(brief: dict[str, Any]) -> int:
    payload = {column: brief.get(column, "") for column in AI_BRIEF_COLUMNS}
    with get_connection() as conn:
        cursor = conn.execute(
            f"""
            INSERT INTO ai_briefs ({", ".join(AI_BRIEF_COLUMNS)})
            VALUES ({", ".join(["?"] * len(AI_BRIEF_COLUMNS))})
            """,
            list(payload.values()),
        )
        return int(cursor.lastrowid)


def insert_export(export_type: str, source_ids: list[str], title: str, content: str) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO exports (export_type, source_note_ids, title, content, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (export_type, json.dumps(source_ids), title, content, now_iso()),
        )
        return int(cursor.lastrowid)


def fetch_df(table: str) -> pd.DataFrame:
    allowed = {"field_notes", "farmstay_logs", "ai_briefs", "exports"}
    if table not in allowed:
        raise ValueError(f"Unsupported table: {table}")
    with get_connection() as conn:
        return pd.read_sql_query(f"SELECT * FROM {table} ORDER BY id DESC", conn)


def fetch_field_notes() -> pd.DataFrame:
    return fetch_df("field_notes")


def fetch_farmstay_logs() -> pd.DataFrame:
    return fetch_df("farmstay_logs")


def fetch_all_library_items() -> pd.DataFrame:
    notes = fetch_field_notes()
    farms = fetch_farmstay_logs()

    note_items = pd.DataFrame()
    if not notes.empty:
        note_items = notes.assign(
            source_type="Field note",
            source_id=notes["id"].astype(str),
            display_title=notes["title"].fillna("Untitled note"),
            display_location=notes["location_name"].fillna(""),
            display_category=notes["category"].fillna(""),
            display_text=notes["note_text"].fillna(""),
            display_state=notes["state"].fillna(""),
        )

    farm_items = pd.DataFrame()
    if not farms.empty:
        farm_items = farms.assign(
            source_type="Community log",
            source_id=farms["id"].astype(str),
            display_title=farms["farm_name"].fillna("Community log"),
            display_location=farms["location_name"].fillna(""),
            display_category=farms["farm_type"].fillna("community"),
            display_text=farms["reflection"].fillna(""),
            display_state="",
            privacy_level="private",
            category=farms["farm_type"].fillna("community"),
            tags="community",
        )

    return pd.concat([note_items, farm_items], ignore_index=True, sort=False)


def get_field_note(note_id: int) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM field_notes WHERE id = ?", (note_id,)).fetchone()
        return dict(row) if row else None


def get_farmstay_log(log_id: int) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM farmstay_logs WHERE id = ?", (log_id,)).fetchone()
        return dict(row) if row else None
