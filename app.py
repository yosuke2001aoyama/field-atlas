from __future__ import annotations

import html
import json
import shutil
import sqlite3
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import pydeck as pdk
import streamlit as st
import streamlit.components.v1 as components
from streamlit_searchbox import st_searchbox

from ai_utils import (
    generate_ai_context,
    generate_ai_summary,
    generate_destination_brief,
    generate_farmstay_summary,
    geocode_destination,
    normalize_destination,
    search_destination_suggestions,
)
from db import (
    BASE_DIR,
    fetch_all_library_items,
    fetch_farmstay_logs,
    fetch_field_notes,
    get_field_note,
    get_farmstay_log,
    initialize_app,
    insert_ai_brief,
    insert_farmstay_log,
    insert_field_note,
)
from export_utils import generate_export, save_export
from map_utils import build_map_points
from privacy_utils import create_public_version_for_farmstay, create_public_version_for_note


APP_NAME = "Waymark U.S."


st.set_page_config(page_title=APP_NAME, page_icon="US", layout="wide")
initialize_app()


CATEGORIES = [
    "travel",
    "food",
    "people",
    "culture",
    "economy",
    "politics/news",
    "personal reflection",
    "nature",
    "logistics",
    "other",
]

NOTE_THEMES = [
    "travel",
    "food",
    "people",
    "culture",
    "economy",
    "politics/news",
    "personal reflection",
    "nature",
    "logistics",
]

THEME_KEYWORDS = {
    "food": ["food", "meal", "diner", "coffee", "market", "restaurant", "bread", "breakfast"],
    "people": ["people", "conversation", "met", "neighbor", "vendor", "host", "local"],
    "culture": ["music", "church", "festival", "museum", "accent", "school", "tradition"],
    "economy": ["industry", "work", "job", "housing", "price", "warehouse", "factory", "tourism", "labor"],
    "politics/news": ["election", "policy", "mayor", "county", "news", "politic", "protest", "government"],
    "personal reflection": ["felt", "wondered", "realized", "remember", "lonely", "surprised", "thought"],
    "nature": ["river", "mountain", "forest", "trail", "weather", "soil", "rain", "field", "landscape"],
    "logistics": ["train", "bus", "station", "road", "motel", "drive", "parking", "airport", "route"],
    "travel": ["arrived", "road", "trip", "walk", "visited", "drive", "downtown", "stop", "journey"],
}

FARM_TYPES = ["vegetable", "dairy", "livestock", "vineyard", "mixed", "homestead", "market garden", "other"]
PRIVACY_LEVELS = ["private", "semi-private", "public-ready"]
EXPORT_TYPES = [
    "Podcast script",
    "Substack-style essay",
    "Instagram caption",
    "Japanese diary",
    "English field note",
    "Markdown archive",
]

HERO_IMAGE_URL = "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=80"
MAP_IMAGE_URL = "https://images.unsplash.com/photo-1524661135-423995f22d0b?auto=format&fit=crop&w=1600&q=80"

MAJOR_US_CITIES = pd.DataFrame(
    [
        {"title": "New York", "latitude": 40.7128, "longitude": -74.0060, "category": "major city", "summary": "Major U.S. city"},
        {"title": "Chicago", "latitude": 41.8781, "longitude": -87.6298, "category": "major city", "summary": "Major U.S. city"},
        {"title": "Los Angeles", "latitude": 34.0522, "longitude": -118.2437, "category": "major city", "summary": "Major U.S. city"},
        {"title": "Houston", "latitude": 29.7604, "longitude": -95.3698, "category": "major city", "summary": "Major U.S. city"},
        {"title": "Atlanta", "latitude": 33.7490, "longitude": -84.3880, "category": "major city", "summary": "Major U.S. city"},
        {"title": "Denver", "latitude": 39.7392, "longitude": -104.9903, "category": "major city", "summary": "Major U.S. city"},
        {"title": "New Orleans", "latitude": 29.9511, "longitude": -90.0715, "category": "major city", "summary": "Major U.S. city"},
        {"title": "Seattle", "latitude": 47.6062, "longitude": -122.3321, "category": "major city", "summary": "Major U.S. city"},
        {"title": "Miami", "latitude": 25.7617, "longitude": -80.1918, "category": "major city", "summary": "Major U.S. city"},
        {"title": "San Francisco", "latitude": 37.7749, "longitude": -122.4194, "category": "major city", "summary": "Major U.S. city"},
    ]
)

INTERSTATE_ROUTES = pd.DataFrame(
    [
        {"name": "I-90", "path": [[-122.3321, 47.6062], [-104.9903, 39.7392], [-87.6298, 41.8781], [-74.0060, 40.7128]]},
        {"name": "I-10", "path": [[-118.2437, 34.0522], [-95.3698, 29.7604], [-90.0715, 29.9511], [-80.1918, 25.7617]]},
        {"name": "I-95", "path": [[-80.1918, 25.7617], [-84.3880, 33.7490], [-74.0060, 40.7128]]},
        {"name": "I-35", "path": [[-97.7431, 30.2672], [-97.3308, 37.6872], [-93.2650, 44.9778]]},
        {"name": "I-80", "path": [[-122.4194, 37.7749], [-104.9903, 39.7392], [-87.6298, 41.8781], [-74.0060, 40.7128]]},
    ]
)

def apply_style() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:opsz,wght@6..72,500;6..72,700&display=swap');

            :root {
                --atlas-ink: #161411;
                --atlas-muted: #746d62;
                --atlas-paper: #f7f2e8;
                --atlas-card: rgba(255, 252, 246, 0.90);
                --atlas-line: rgba(62, 48, 33, 0.16);
                --atlas-green: #263f35;
                --atlas-rust: #8d5d3e;
                --atlas-gold: #b7965d;
                --atlas-deep: #11100e;
            }

            .stApp {
                background:
                    linear-gradient(90deg, rgba(183, 150, 93, 0.07) 0 1px, transparent 1px 100%),
                    linear-gradient(180deg, #faf7f0 0%, #efe6d7 100%);
                background-size: 64px 100%, auto;
                color: var(--atlas-ink);
                font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }

            .block-container {
                max-width: 1220px;
                padding-top: 1.6rem;
                padding-bottom: 4rem;
            }

            h1, h2, h3 {
                font-family: Newsreader, Georgia, 'Times New Roman', serif;
                letter-spacing: 0;
                color: var(--atlas-ink);
            }

            p, label, div, span {
                letter-spacing: 0;
            }

            [data-testid="stSidebar"] {
                background:
                    linear-gradient(180deg, rgba(255, 252, 246, 0.93), rgba(239, 230, 215, 0.98)),
                    url("https://images.unsplash.com/photo-1524661135-423995f22d0b?auto=format&fit=crop&w=900&q=80");
                background-size: cover;
                background-position: center;
                border-right: 1px solid rgba(23, 33, 28, 0.10);
            }

            [data-testid="stSidebar"]::before {
                content: "";
                position: fixed;
                inset: 0 auto 0 0;
                width: 21rem;
                pointer-events: none;
                background: rgba(250, 247, 240, 0.86);
                backdrop-filter: blur(22px);
            }

            [data-testid="stSidebar"] > div {
                position: relative;
                z-index: 1;
            }

            [data-testid="stSidebar"] h1 {
                font-family: Newsreader, Georgia, serif;
                font-size: 2.35rem;
                line-height: 1;
                margin-bottom: 0.1rem;
            }

            [data-testid="stSidebar"] p {
                font-size: 0.95rem;
            }

            .sidebar-tagline {
                color: rgba(23, 33, 28, 0.62);
                font-size: 0.86rem;
                line-height: 1.35;
                margin: -0.2rem 0 1.2rem;
            }

            .nav-section {
                margin: 1.05rem 0 0.2rem;
                color: var(--atlas-gold);
                font-size: 0.72rem;
                font-weight: 900;
                letter-spacing: 0.12rem;
                text-transform: uppercase;
            }

            .nav-child {
                margin-left: 0.7rem;
                padding-left: 0.7rem;
                border-left: 1px solid rgba(183, 150, 93, 0.26);
            }

            .nav-active {
                border-radius: 0;
                padding: 0.74rem 0.34rem;
                margin: 0.18rem 0 0.18rem 0.15rem;
                color: var(--atlas-ink);
                border-left: 3px solid var(--atlas-gold);
                background: linear-gradient(90deg, rgba(183, 150, 93, 0.13), transparent);
                box-shadow: none;
                font-weight: 800;
            }

            .top-nav-active {
                border-radius: 999px;
                padding: 0.74rem 0.9rem;
                text-align: center;
                color: #ffffff;
                background: linear-gradient(135deg, #17211c, #2f6f58);
                box-shadow: 0 12px 26px rgba(23, 33, 28, 0.14);
                font-weight: 800;
                min-height: 2.7rem;
            }

            .top-nav-wrap {
                margin: 0 0 1.25rem;
                padding: 0.55rem;
                border: 1px solid rgba(23, 33, 28, 0.10);
                border-radius: 24px;
                background: rgba(255, 255, 255, 0.48);
                backdrop-filter: blur(18px);
                box-shadow: 0 14px 34px rgba(23, 33, 28, 0.06);
            }

            [data-testid="stSidebar"] .stButton {
                width: 100%;
            }

            [data-testid="stSidebar"] .stButton > button {
                width: 100%;
                justify-content: flex-start;
                border-radius: 0;
                padding: 0.70rem 0.34rem;
                margin: 0.08rem 0;
                color: var(--atlas-ink);
                background: transparent;
                border: 0;
                border-bottom: 1px solid rgba(62, 48, 33, 0.10);
                box-shadow: none;
                font-weight: 750;
                min-height: 2.7rem;
            }

            [data-testid="stSidebar"] .stButton > button:hover {
                background: rgba(183, 150, 93, 0.09);
                border-color: rgba(183, 150, 93, 0.26);
                transform: translateX(3px);
            }

            .atlas-hero {
                min-height: 50vh;
                display: grid;
                align-items: end;
                overflow: hidden;
                border: 1px solid rgba(255, 252, 246, 0.54);
                border-radius: 0;
                padding: clamp(1.4rem, 4vw, 3.4rem);
                margin-bottom: 1.8rem;
                color: #ffffff;
                background:
                    linear-gradient(180deg, rgba(9, 17, 12, 0.02) 0%, rgba(9, 17, 12, 0.76) 100%),
                    linear-gradient(90deg, rgba(9, 17, 12, 0.86), rgba(9, 17, 12, 0.18) 66%),
                    url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=80");
                background-size: cover;
                background-position: center;
                box-shadow: 0 34px 90px rgba(35, 24, 13, 0.24);
            }

            .atlas-hero h1 {
                color: #ffffff;
                font-size: clamp(3.4rem, 7.4vw, 6.4rem);
                line-height: 0.9;
                margin: 0.35rem 0 0.65rem;
                max-width: 850px;
            }

            .atlas-hero h3 {
                color: rgba(255, 255, 255, 0.92);
                font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                font-size: clamp(1.18rem, 2vw, 1.65rem);
                font-weight: 600;
                max-width: 720px;
            }

            .atlas-hero p {
                color: rgba(255, 255, 255, 0.82);
                max-width: 720px;
                font-size: 1.02rem;
            }

            .atlas-kicker {
                color: rgba(244, 220, 171, 0.94);
                font-size: 0.78rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.14rem;
                margin-bottom: 0.35rem;
            }

            .atlas-card {
                background: var(--atlas-card);
                border: 1px solid var(--atlas-line);
                border-radius: 0;
                padding: 1.1rem;
                margin-bottom: 0.8rem;
                box-shadow: 0 22px 52px rgba(35, 24, 13, 0.08);
                backdrop-filter: blur(16px);
            }

            .atlas-panel {
                background: rgba(255, 252, 246, 0.82);
                border: 1px solid var(--atlas-line);
                border-radius: 0;
                padding: 1.25rem;
                box-shadow: 0 18px 46px rgba(35, 24, 13, 0.07);
            }

            .atlas-action-card {
                min-height: 10.75rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                background: rgba(255, 252, 246, 0.86);
                border: 1px solid var(--atlas-line);
                border-radius: 0;
                padding: 1.16rem;
                box-shadow: 0 16px 38px rgba(35, 24, 13, 0.07);
            }

            .atlas-action-card h4 {
                margin: 0 0 0.35rem;
                font-size: 1.08rem;
                color: var(--atlas-ink);
            }

            .atlas-action-card p {
                margin: 0;
                color: var(--atlas-muted);
                font-size: 0.9rem;
            }

            .atlas-photo-strip {
                min-height: 13rem;
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,0.52);
                background:
                    linear-gradient(180deg, rgba(23,33,28,0.10), rgba(23,33,28,0.42)),
                    url("https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1400&q=80");
                background-size: cover;
                background-position: center;
                box-shadow: 0 18px 44px rgba(23, 33, 28, 0.12);
            }

            .atlas-route-card {
                min-height: 15rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                border: 1px solid rgba(255, 252, 246, 0.56);
                border-radius: 0;
                padding: 1.5rem;
                color: #ffffff;
                background:
                    linear-gradient(180deg, rgba(9, 17, 12, 0.06), rgba(9, 17, 12, 0.72)),
                    url("https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1400&q=80");
                background-size: cover;
                background-position: center;
                box-shadow: 0 26px 68px rgba(35, 24, 13, 0.18);
            }

            .atlas-route-card h3, .atlas-route-card p {
                color: #ffffff;
                margin: 0;
            }

            .atlas-route-card p {
                color: rgba(255, 255, 255, 0.82);
                max-width: 44rem;
            }

            .atlas-choice-label {
                color: var(--atlas-muted);
                font-size: 0.82rem;
                font-weight: 800;
                letter-spacing: 0.12rem;
                text-transform: uppercase;
                margin-bottom: 0.5rem;
            }

            .journey-card {
                min-height: 17rem;
                padding: 1.55rem;
                border: 1px solid rgba(62, 48, 33, 0.16);
                background: rgba(255, 252, 246, 0.88);
                box-shadow: 0 22px 60px rgba(35, 24, 13, 0.08);
            }

            .journey-card h3 {
                font-size: 2rem;
                margin: 0.35rem 0 0.65rem;
            }

            .journey-card p {
                color: var(--atlas-muted);
                line-height: 1.65;
            }

            .brief-hero {
                min-height: 34rem;
                display: grid;
                align-items: end;
                padding: clamp(1.6rem, 4vw, 3.4rem);
                margin: 1.4rem 0 1.6rem;
                color: white;
                border: 1px solid rgba(255, 252, 246, 0.58);
                background-size: cover;
                background-position: center;
                box-shadow: 0 28px 76px rgba(35, 24, 13, 0.20);
            }

            .brief-hero h2 {
                color: white;
                font-size: clamp(2.45rem, 5vw, 4.75rem);
                margin: 0.3rem 0;
            }

            .brief-hero p {
                color: rgba(255,255,255,0.84);
                max-width: 52rem;
            }

            .brief-section {
                min-height: 13rem;
                padding: 1.55rem;
                border-top: 3px solid var(--atlas-gold);
                background:
                    linear-gradient(135deg, rgba(255, 252, 246, 0.94), rgba(246, 237, 220, 0.86)),
                    url("https://images.unsplash.com/photo-1524661135-423995f22d0b?auto=format&fit=crop&w=900&q=60");
                background-size: cover;
                background-blend-mode: screen;
                box-shadow: 0 18px 46px rgba(35, 24, 13, 0.06);
                margin-bottom: 1rem;
            }

            .brief-section h4 {
                margin: 0 0 0.7rem;
                color: var(--atlas-ink);
                font-size: 0.86rem;
                letter-spacing: 0.1rem;
                text-transform: uppercase;
            }

            .brief-section p {
                color: #3a352e;
                line-height: 1.72;
                font-size: 1.02rem;
            }

            .brief-icon {
                display: inline-flex;
                width: 2.1rem;
                height: 2.1rem;
                align-items: center;
                justify-content: center;
                margin-bottom: 0.75rem;
                border-radius: 999px;
                color: #fff;
                background: #17211c;
                font-weight: 900;
                font-size: 0.78rem;
            }

            .voice-dock {
                padding: 1.1rem;
                margin: 0.6rem 0 1rem;
                border: 1px solid rgba(255,255,255,0.32);
                background: linear-gradient(135deg, #17211c, #305c4b);
                color: white;
                box-shadow: 0 20px 48px rgba(23, 33, 28, 0.16);
            }

            .voice-dock h3, .voice-dock p {
                color: white;
                margin: 0;
            }

            .memory-mode-card {
                min-height: 11rem;
                padding: 1.35rem;
                background: rgba(255, 252, 246, 0.88);
                border: 1px solid rgba(62, 48, 33, 0.14);
                box-shadow: 0 16px 42px rgba(35, 24, 13, 0.07);
            }

            .memory-mode-card h3 {
                margin: 0.2rem 0 0.55rem;
                font-size: 1.75rem;
            }

            .map-legend {
                display: flex;
                gap: 0.65rem;
                flex-wrap: wrap;
                margin: 0.4rem 0 1rem;
            }

            .map-legend span {
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                border: 1px solid rgba(62, 48, 33, 0.14);
                background: rgba(255, 252, 246, 0.72);
                padding: 0.45rem 0.7rem;
                border-radius: 999px;
                color: var(--atlas-muted);
                font-size: 0.85rem;
                font-weight: 700;
            }

            .atlas-pill-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin-top: 1rem;
            }

            .atlas-pill {
                border: 1px solid rgba(255, 255, 255, 0.35);
                border-radius: 999px;
                padding: 0.42rem 0.7rem;
                color: rgba(255,255,255,0.88);
                background: rgba(255,255,255,0.12);
                backdrop-filter: blur(10px);
                font-size: 0.83rem;
                font-weight: 700;
            }

            .small-muted {
                color: var(--atlas-muted);
                font-size: 0.92rem;
            }

            div[data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.78);
                border: 1px solid var(--atlas-line);
                border-radius: 18px;
                padding: 1rem 1.1rem;
                box-shadow: 0 16px 34px rgba(23, 33, 28, 0.07);
            }

            div[data-testid="stMetricValue"] {
                font-family: Newsreader, Georgia, serif;
                font-size: 2.25rem;
            }

            div[data-testid="stForm"], div[data-testid="stExpander"], [data-testid="stVerticalBlockBorderWrapper"] {
                border-radius: 18px !important;
            }

            .stButton > button, .stDownloadButton > button, button[kind="primaryFormSubmit"] {
                border-radius: 999px;
                border: 1px solid rgba(23, 33, 28, 0.14);
                background: linear-gradient(135deg, #17211c, #2f6f58);
                color: white;
                font-weight: 800;
                min-height: 2.8rem;
                box-shadow: 0 12px 24px rgba(23, 33, 28, 0.14);
            }

            .stButton > button:hover, button[kind="primaryFormSubmit"]:hover {
                border-color: rgba(47, 111, 88, 0.34);
                filter: brightness(1.05);
            }

            .stTextInput input, .stTextArea textarea, .stNumberInput input {
                border-radius: 12px;
                border-color: rgba(23, 33, 28, 0.14);
                background: rgba(255, 255, 255, 0.82);
            }

            [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.82);
            }

            iframe {
                border-radius: 18px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def save_upload(uploaded_file, folder: str) -> str:
    if not uploaded_file:
        return ""
    target_dir = BASE_DIR / "uploads" / folder
    target_dir.mkdir(parents=True, exist_ok=True)
    safe_name = f"{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name.replace('/', '_')}"
    target = target_dir / safe_name
    with target.open("wb") as out_file:
        shutil.copyfileobj(uploaded_file, out_file)
    return str(target.relative_to(BASE_DIR))


def render_context_block(text: str) -> None:
    if not text:
        return
    for block in text.split("\n\n"):
        if ":" in block:
            label, content = block.split(":", 1)
            st.markdown(f"**{label.strip()}**: {content.strip()}")
        else:
            st.write(block)


def classify_note_theme(text: str, tags: str = "", mood: str = "") -> str:
    haystack = f"{text or ''} {tags or ''} {mood or ''}".lower()
    scores = {theme: 0 for theme in NOTE_THEMES}
    for theme, keywords in THEME_KEYWORDS.items():
        scores[theme] += sum(1 for keyword in keywords if keyword in haystack)
    best_theme, best_score = max(scores.items(), key=lambda item: item[1])
    return best_theme if best_score else "personal reflection"


def generate_public_ready_summary(text: str, location: str, theme: str) -> str:
    cleaned = " ".join((text or "").split())
    seed = cleaned[:220] if cleaned else "This note records a small observation from movement through place."
    return (
        f"An anonymous {theme} field note from {location or 'a U.S. place'}: {seed} "
        "Exact timing, private names, and sensitive details should be reviewed before publication."
    )


def fetch_saved_briefs() -> pd.DataFrame:
    db_path = BASE_DIR / "data" / "field_atlas.db"
    if not db_path.exists():
        return pd.DataFrame()
    try:
        with sqlite3.connect(db_path) as conn:
            return pd.read_sql_query("SELECT * FROM ai_briefs ORDER BY id DESC", conn)
    except Exception:
        return pd.DataFrame()


def render_sidebar(pages: list[str]) -> str:
    nav_labels = {
        "Home": "Home",
        "Memory Map": "Memory Map",
        "Read Reviews": "Read Reviews",
        "Search My Notes": "Search Notes",
        "Capture Note": "Capture Note",
        "Ask About This Place": "Ask About This Place",
        "Community Log": "Community Log",
        "Library": "Library",
        "Export": "Export",
        "Publish Safely": "Publish Safely",
        "Journey Review": "Journey Review",
    }
    st.sidebar.title(APP_NAME)
    st.sidebar.markdown(
        '<div class="sidebar-tagline">A U.S. movement journal for notes, place context, memory maps, and public-ready reflection.</div>',
        unsafe_allow_html=True,
    )
    def nav_button(page_name: str, label_override: str | None = None) -> None:
        display_label = label_override or nav_labels.get(page_name, page_name)
        if page_name == st.session_state.page:
            st.sidebar.markdown(f'<div class="nav-active">{display_label}</div>', unsafe_allow_html=True)
        elif st.sidebar.button(display_label, key=f"side_nav_{page_name}_{display_label}"):
            st.session_state.page = page_name
            st.rerun()

    nav_button("Home")
    st.sidebar.markdown('<div class="nav-section">Understand</div>', unsafe_allow_html=True)
    nav_button("Ask About This Place")
    nav_button("Memory Map")
    nav_button("Read Reviews")
    st.sidebar.markdown('<div class="nav-section">Capture</div>', unsafe_allow_html=True)
    nav_button("Capture Note")
    nav_button("Community Log")
    st.sidebar.markdown('<div class="nav-section">Revisit & Share</div>', unsafe_allow_html=True)
    nav_button("Journey Review")
    nav_button("Publish Safely")
    return st.session_state.page


def go_to(page_name: str) -> None:
    st.session_state.page = page_name
    st.rerun()


def destination_search_options(query: str) -> list[str]:
    suggestions = search_destination_suggestions(query)
    if "destination_payloads" not in st.session_state:
        st.session_state.destination_payloads = {}
    labels = []
    for item in suggestions:
        label = item["label"]
        st.session_state.destination_payloads[label] = item
        labels.append(label)
    return labels


def build_brief_map_points(briefs: pd.DataFrame) -> pd.DataFrame:
    if briefs.empty:
        return pd.DataFrame()
    rows = []
    for brief in briefs.itertuples():
        geo = geocode_destination(str(brief.destination or ""), str(brief.state or ""))
        if not geo.get("latitude") or not geo.get("longitude"):
            continue
        rows.append(
            {
                "source": "Place brief",
                "source_id": str(brief.id),
                "title": str(brief.destination or "Saved brief"),
                "location": geo.get("display_name") or ", ".join(part for part in [brief.destination, brief.state] if part),
                "category": "brief",
                "latitude": geo["latitude"],
                "longitude": geo["longitude"],
                "summary": str(brief.brief_15_sec or ""),
                "color": [183, 150, 93],
            }
        )
    return pd.DataFrame(rows)


def render_compact_map(points: pd.DataFrame, target_payload: dict | None = None, include_routes: bool = False) -> None:
    if points.empty and not include_routes:
        st.info("No mapped records yet.")
        return
    if points.empty and include_routes:
        points = MAJOR_US_CITIES.assign(color=[[110, 84, 46]] * len(MAJOR_US_CITIES))
    if target_payload and target_payload.get("latitude") and target_payload.get("longitude"):
        midpoint = [target_payload["longitude"], target_payload["latitude"]]
        zoom = 6.8
    else:
        midpoint = [points["longitude"].mean(), points["latitude"].mean()]
        zoom = 3.5
    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=points,
            get_position="[longitude, latitude]",
            get_fill_color="color",
            get_radius=10000,
            pickable=True,
            opacity=0.82,
        )
    ]
    if include_routes:
        city_points = MAJOR_US_CITIES.assign(color=[[110, 84, 46]] * len(MAJOR_US_CITIES))
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=city_points,
                get_position="[longitude, latitude]",
                get_fill_color="color",
                get_radius=12500,
                pickable=True,
                opacity=0.52,
            )
        )
        layers.append(
            pdk.Layer(
                "PathLayer",
                data=INTERSTATE_ROUTES,
                get_path="path",
                get_color=[183, 150, 93, 130],
                width_min_pixels=2,
                pickable=True,
            )
        )
    st.pydeck_chart(
        pdk.Deck(
            layers=layers,
            initial_view_state=pdk.ViewState(latitude=midpoint[1], longitude=midpoint[0], zoom=zoom),
            tooltip={
                "html": "<b>{title}</b><br/>{category}<br/>{summary}",
                "style": {"backgroundColor": "#17211c", "color": "white"},
            },
        ),
        use_container_width=True,
    )


def answer_home_question(question: str) -> str:
    q = (question or "").lower()
    if not q.strip():
        return "Ask me what to notice in a place, where your memories cluster, or how to turn notes into a public-safe reflection."
    if "public" in q or "publish" in q or "share" in q:
        return "Start private. When you are ready, use Publish Safely to remove exact addresses, private names, raw transcripts, and real-time details before sharing."
    if "map" in q or "where" in q:
        return "Use Memory Map. Reviews show lived notes; Briefs show context you generated before or during a trip. The two stay separate so memory and research do not blur."
    if "notice" in q or "brief" in q or "place" in q:
        return "Use Ask About This Place. Enter a city, park, landmark, or small town, then generate a visual brief with prompts for what to notice."
    return "Capture the rough thought first. Waymark U.S. will attach place, theme, mood, and privacy status so scattered notes can become searchable memory later."


def home_page() -> None:
    notes = fetch_field_notes()
    farms = fetch_farmstay_logs()
    briefs = fetch_saved_briefs()
    mapped, _ = build_map_points(notes, farms)
    brief_points = build_brief_map_points(briefs)

    st.markdown(
        """
        <div class="atlas-hero">
            <div>
            <div class="atlas-kicker">A U.S. movement-based second brain</div>
            <h1>Waymark U.S.</h1>
            <h3>Turn movement into memory and understanding.</h3>
            <p>Capture messy thoughts while moving, organize them by place and theme, ask what to notice nearby, and later turn private notes into careful public reflections.</p>
            <div class="atlas-pill-row">
                <span class="atlas-pill">Smart travel journal</span>
                <span class="atlas-pill">Place intelligence</span>
                <span class="atlas-pill">Community logs</span>
                <span class="atlas-pill">Private by default</span>
            </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="atlas-choice-label">What do you want to do?</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="journey-card">
                <div class="atlas-choice-label">Understand</div>
                <h3>Learn what to notice</h3>
                <p>Search a city, park, landmark, or neighborhood. Get a sourced brief, map context, and prompts for what to watch as you move.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Learn About a Place", width="stretch"):
            go_to("Ask About This Place")
    with c2:
        st.markdown(
            """
            <div class="journey-card">
                <div class="atlas-choice-label">Capture</div>
                <h3>Save a moving thought</h3>
                <p>Speak in the car, type on a walk, or paste a rough impression. It stays private unless you choose to prepare it for public knowledge.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Record a Thought", width="stretch"):
            go_to("Capture Note")

    st.markdown("### Ask Waymark")
    st.markdown(
        """
        <div class="voice-dock">
            <h3>Talk to your travel memory</h3>
            <p>Ask what to notice, where to look on the map, or how to make a note public-safe.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    question_cols = st.columns([0.7, 1.3])
    with question_cols[0]:
        if hasattr(st, "audio_input"):
            st.audio_input("Ask by voice")
        st.caption("Voice capture is stored only when you save it as a note. For now, type the question below to get a local response.")
    with question_cols[1]:
        home_question = st.text_input("Ask a question", placeholder="What should I notice in New Orleans? How do I publish safely?")
        if home_question:
            st.info(answer_home_question(home_question))

    st.markdown("### Explore the Map")
    home_place_label = st_searchbox(
        destination_search_options,
        placeholder="Search a city, park, landmark, or highway corridor...",
        label=None,
        default="",
        default_use_searchterm=True,
        clear_on_submit=False,
        edit_after_submit="current",
        debounce=450,
        key="home_map_searchbox",
    )
    home_place_payload = st.session_state.get("destination_payloads", {}).get(home_place_label)
    if home_place_label and not home_place_payload:
        home_place_payload = geocode_destination(home_place_label)
    review_tab, brief_tab = st.tabs(["Reviews", "Briefs + U.S. Routes"])
    with review_tab:
        render_compact_map(mapped, home_place_payload, include_routes=False)
    with brief_tab:
        brief_layer = brief_points if not brief_points.empty else pd.DataFrame()
        render_compact_map(brief_layer, home_place_payload, include_routes=True)

    left, right = st.columns([1.2, 0.8])
    with left:
        st.markdown(
            """
            <div class="atlas-panel">
                <h3>Designed for the private-to-public workflow</h3>
                <p class="small-muted">Waymark U.S. keeps raw observations separate from organized knowledge and public storytelling. Exact places, raw transcripts, personal names, and real-time movement stay private unless you deliberately transform them.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown('<div class="atlas-photo-strip"></div>', unsafe_allow_html=True)


def add_field_note_page() -> None:
    st.title("Capture Note")
    st.caption("Capture a moving thought from the car, a sidewalk, a station, or a quiet room. Everything is private first; selected notes can later become public knowledge.")
    st.markdown(
        """
        <div class="atlas-panel">
            <h3>Private first, useful later</h3>
            <p class="small-muted">Waymark U.S. is built for small voice notes and rough thoughts: say what you notice, attach the place, and let the system organize it. Public sharing is always a later choice, never the default.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Where are you noticing this?**")
    selected_location_label = st_searchbox(
        destination_search_options,
        placeholder="City, park, landmark...",
        label=None,
        default="",
        default_use_searchterm=True,
        clear_on_submit=False,
        edit_after_submit="current",
        debounce=450,
        key="capture_location_searchbox",
    )
    st.caption("Start typing, then choose a suggested U.S. place. Example: Grand Canyon, Shelbyville Indiana, New Orleans.")
    selected_location_payload = st.session_state.get("destination_payloads", {}).get(selected_location_label)
    if selected_location_label and not selected_location_payload:
        selected_location_payload = geocode_destination(selected_location_label)

    default_location = ""
    default_city = ""
    default_state = ""
    default_latitude = None
    default_longitude = None
    if selected_location_payload:
        default_location = selected_location_payload.get("destination") or selected_location_label
        default_city = selected_location_payload.get("city", "")
        default_state = selected_location_payload.get("state", "")
        default_latitude = selected_location_payload.get("latitude")
        default_longitude = selected_location_payload.get("longitude")
        st.markdown(
            f'<div class="atlas-card"><div class="atlas-choice-label">Place locked</div><strong>{html.escape(default_location)}</strong><br><span class="small-muted">{html.escape(selected_location_payload.get("display_name", default_state))}</span></div>',
            unsafe_allow_html=True,
        )

    with st.form("field_note_form", clear_on_submit=False):
        title = st.text_input("Optional title", placeholder="Leave blank and Waymark will treat this as a quick note.")
        note_text = st.text_area("Raw note", height=190, placeholder="Type a thought, paste a voice transcript, or jot down what you just noticed.")
        mood_col, privacy_col = st.columns(2)
        mood = mood_col.selectbox(
            "Feeling",
            ["curious", "calm", "energized", "uncertain", "moved", "overwhelmed", "reflective", "practical", "other"],
        )
        publishing_choice = privacy_col.selectbox(
            "Keep it...",
            [
                "Private",
                "Working note",
                "Public-ready draft",
            ],
            help="Private is the default. Public-ready drafts should still be reviewed before publishing.",
        )
        if hasattr(st, "audio_input"):
            audio = st.audio_input("Record voice memo")
            backup_audio = st.file_uploader("Or upload audio", type=["mp3", "m4a", "wav", "aac", "webm"])
            audio = audio or backup_audio
        else:
            audio = st.file_uploader("Voice memo upload", type=["mp3", "m4a", "wav", "aac", "webm"])
        photo = st.file_uploader("Optional photo", type=["png", "jpg", "jpeg", "webp"])
        audio_transcript = st.text_area(
            "Voice transcript / dictated text",
            height=120,
            placeholder="For now, paste a transcript here. Future versions can connect Whisper or on-device transcription.",
        )
        tags = st.text_input("Optional tags", placeholder="Waymark can classify later; tags are optional.")
        preview_text = "\n\n".join(part for part in [note_text, audio_transcript] if part)
        auto_category = classify_note_theme(preview_text, tags, mood) if preview_text or tags else "personal reflection"
        st.caption(f"Auto theme preview: {auto_category}")
        submitted = st.form_submit_button("Save Note")

    if submitted:
        note_date = date.today()
        note_time = datetime.now().time().replace(second=0, microsecond=0)
        location_name = default_location or selected_location_label
        address = ""
        city = default_city
        state = default_state
        latitude = default_latitude
        longitude = default_longitude
        captured_text = "\n\n".join(part for part in [note_text.strip(), audio_transcript.strip()] if part)
        if not title.strip() and not captured_text.strip() and not audio:
            st.error("Please add a title, note text, transcript, or voice memo.")
            return
        photo_path = save_upload(photo, "photos")
        audio_path = save_upload(audio, "audio")
        location = location_name or city or state
        category = classify_note_theme(captured_text, tags, mood)
        ai_summary = generate_public_ready_summary(captured_text, location, category)
        ai_context = generate_ai_context(captured_text, category, location)
        privacy_level = {
            "Private": "private",
            "Working note": "semi-private",
            "Public-ready draft": "public-ready",
        }[publishing_choice]
        note_id = insert_field_note(
            {
                "title": title or "Untitled field note",
                "date": datetime.combine(note_date, note_time).isoformat(timespec="minutes"),
                "location_name": location_name,
                "address": address,
                "latitude": latitude,
                "longitude": longitude,
                "city": city,
                "state": state,
                "category": category,
                "note_text": captured_text,
                "photo_path": photo_path,
                "audio_path": audio_path,
                "audio_transcript": audio_transcript,
                "mood": mood,
                "ai_summary": ai_summary,
                "ai_context": ai_context,
                "tags": tags,
                "privacy_level": privacy_level,
            }
        )
        st.success(f"Saved field note #{note_id}.")
        with st.container(border=True):
            st.subheader(title or "Untitled field note")
            st.caption(f"{location or 'No location'} | {category} | {mood} | {privacy_level}")
            st.write(captured_text or "Voice memo saved. Add a transcript later for search and summaries.")
            st.markdown("**Organized summary**")
            st.write(ai_summary)
            render_context_block(ai_context)


def map_view_page() -> None:
    st.title("Memory Map")
    st.caption("Explore saved memories and saved place briefs without mixing them up. Reviews are what you experienced; briefs are context you asked for.")
    notes = fetch_field_notes()
    farms = fetch_farmstay_logs()
    briefs = fetch_saved_briefs()
    mapped, needs_location = build_map_points(notes, farms)
    brief_points = build_brief_map_points(briefs)

    st.markdown("**Search a place**")
    map_place_label = st_searchbox(
        destination_search_options,
        placeholder="City, park, landmark...",
        label=None,
        default="",
        default_use_searchterm=True,
        clear_on_submit=False,
        edit_after_submit="current",
        debounce=450,
        key="map_place_searchbox",
    )
    map_place_payload = st.session_state.get("destination_payloads", {}).get(map_place_label)
    if map_place_label and not map_place_payload:
        map_place_payload = geocode_destination(map_place_label)

    st.markdown(
        '<div class="map-legend"><span>Reviews: your lived notes</span><span>Briefs: place context you generated</span></div>',
        unsafe_allow_html=True,
    )

    review_tab, brief_tab = st.tabs(["Reviews & Notes", "Saved Briefs"])

    with review_tab:
        search = st.text_input("Search saved notes and reviews", placeholder="Try: market, Knoxville, food, station")
        category_options = ["All"]
        if not mapped.empty:
            category_options += sorted({str(value) for value in mapped["category"].dropna() if str(value)})
        selected_category = st.selectbox("Map category", category_options)

        visible = mapped.copy()
        if selected_category != "All":
            visible = visible[visible["category"].astype(str) == selected_category]
        if search:
            query = search.lower()
            visible = visible[
                visible[["title", "location", "category", "summary"]]
                .fillna("")
                .astype(str)
                .agg(" ".join, axis=1)
                .str.lower()
                .str.contains(query, na=False)
            ]
        render_memory_map(visible, map_place_payload, map_place_label, needs_location)

    with brief_tab:
        brief_search = st.text_input("Search saved briefs", placeholder="Try: New Orleans, history, local food")
        visible_briefs = brief_points.copy()
        if brief_search and not visible_briefs.empty:
            query = brief_search.lower()
            visible_briefs = visible_briefs[
                visible_briefs[["title", "location", "summary"]]
                .fillna("")
                .astype(str)
                .agg(" ".join, axis=1)
                .str.lower()
                .str.contains(query, na=False)
            ]
        render_brief_map(visible_briefs, map_place_payload, map_place_label)


def render_memory_map(visible: pd.DataFrame, map_place_payload: dict | None, map_place_label: str, needs_location: pd.DataFrame) -> None:
    if visible.empty:
        st.info("No mapped reviews match the current search.")
    else:
        if map_place_payload and map_place_payload.get("latitude") and map_place_payload.get("longitude"):
            midpoint = [map_place_payload["longitude"], map_place_payload["latitude"]]
            zoom = 8.4
        else:
            midpoint = [visible["longitude"].mean(), visible["latitude"].mean()]
            zoom = 4.2
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=visible,
            get_position="[longitude, latitude]",
            get_fill_color="color",
            get_radius=9000,
            pickable=True,
            opacity=0.82,
        )
        layers = [layer]
        if map_place_payload and map_place_payload.get("latitude") and map_place_payload.get("longitude"):
            target_df = pd.DataFrame(
                [
                    {
                        "latitude": map_place_payload["latitude"],
                        "longitude": map_place_payload["longitude"],
                        "label": map_place_payload.get("display_name") or map_place_label,
                    }
                ]
            )
            layers.append(
                pdk.Layer(
                    "ScatterplotLayer",
                    data=target_df,
                    get_position="[longitude, latitude]",
                    get_fill_color=[183, 150, 93, 240],
                    get_radius=14000,
                    pickable=True,
                    opacity=0.92,
                )
            )
        tooltip = {
            "html": "<b>{title}</b><br/>{location}<br/>{category}<br/><br/>{summary}<br/><em>Open details in Library.</em>",
            "style": {"backgroundColor": "#1f2a24", "color": "white"},
        }
        st.pydeck_chart(
            pdk.Deck(
                layers=layers,
                initial_view_state=pdk.ViewState(latitude=midpoint[1], longitude=midpoint[0], zoom=zoom),
                tooltip=tooltip,
            ),
            use_container_width=True,
        )
        if map_place_payload and map_place_payload.get("display_name"):
            st.caption(f"Map centered on: {map_place_payload['display_name']}")

        labels = {
            f"{row.source}:{row.source_id}": f"{row.source} | {row.title} | {row.location}"
            for row in visible.itertuples()
        }
        selected_record = st.selectbox(
            "Open mapped record",
            list(labels.keys()),
            format_func=lambda value: labels[value],
        )
        selected_row = visible[
            (visible["source"] + ":" + visible["source_id"].astype(str)) == selected_record
        ].iloc[0]
        with st.container(border=True):
            st.subheader(selected_row["title"])
            st.write(f"{selected_row['location']} | {selected_row['category']}")
            st.write(selected_row["summary"])
            c1, c2 = st.columns(2)
            if c1.button("Create Public Version", key=f"map_public_{selected_record}"):
                st.session_state.selected_public = (
                    "Field note" if selected_row["source"] == "Field note" else "Community log",
                    int(selected_row["source_id"]),
                )
                st.session_state.page = "Publish Safely"
                st.rerun()
            if c2.button("Export This Record", key=f"map_export_{selected_record}"):
                source_type = "Field note" if selected_row["source"] == "Field note" else "Community log"
                st.session_state.export_selection = [f"{source_type}:{selected_row['source_id']}"]
                st.session_state.page = "Export"
                st.rerun()

    if not needs_location.empty:
        st.subheader("Needs Location Data")
        st.dataframe(needs_location[["source", "title", "location", "category"]], width="stretch")


def render_brief_map(visible: pd.DataFrame, map_place_payload: dict | None, map_place_label: str) -> None:
    if visible.empty:
        st.info("No saved briefs with map coordinates yet. Generate and save a brief from Ask About This Place.")
        return
    if map_place_payload and map_place_payload.get("latitude") and map_place_payload.get("longitude"):
        midpoint = [map_place_payload["longitude"], map_place_payload["latitude"]]
        zoom = 8.4
    else:
        midpoint = [visible["longitude"].mean(), visible["latitude"].mean()]
        zoom = 4.2
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=visible,
        get_position="[longitude, latitude]",
        get_fill_color="color",
        get_radius=12000,
        pickable=True,
        opacity=0.88,
    )
    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=pdk.ViewState(latitude=midpoint[1], longitude=midpoint[0], zoom=zoom),
            tooltip={
                "html": "<b>{title}</b><br/>{location}<br/><br/>{summary}<br/><em>Open Ask About This Place to generate a new brief.</em>",
                "style": {"backgroundColor": "#3a2c19", "color": "white"},
            },
        ),
        use_container_width=True,
    )
    labels = {
        f"{row.source_id}": f"{row.title} | {row.location}"
        for row in visible.itertuples()
    }
    selected_brief = st.selectbox("Open saved brief", list(labels.keys()), format_func=lambda value: labels[value])
    selected_row = visible[visible["source_id"].astype(str) == selected_brief].iloc[0]
    with st.container(border=True):
        st.subheader(selected_row["title"])
        st.write(selected_row["location"])
        st.write(selected_row["summary"])


def ai_companion_page() -> None:
    st.title("Ask About This Place")
    st.markdown(
        f"""
        <div class="brief-hero" style="min-height:20rem;background-image: linear-gradient(180deg, rgba(9,8,6,0.16), rgba(9,8,6,0.74)), linear-gradient(90deg, rgba(9,8,6,0.82), rgba(9,8,6,0.12)), url('{MAP_IMAGE_URL}');">
            <div>
                <div class="atlas-kicker">Place intelligence</div>
                <h2>Ask About This Place</h2>
                <p>Search a U.S. city, park, small town, landmark, or corridor. Waymark builds a sourced visual brief for what to notice before you arrive.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Destination**")
    selected_label = st_searchbox(
        destination_search_options,
        placeholder="City, park, landmark...",
        label=None,
        default="",
        default_use_searchterm=True,
        clear_on_submit=False,
        edit_after_submit="current",
        debounce=450,
        key="destination_searchbox",
    )
    st.caption("Examples: Shelbyville Indiana, New Orleans, Yellowstone, Independence National Historical Park.")
    selected_payload = st.session_state.get("destination_payloads", {}).get(selected_label)
    destination = ""

    if selected_payload:
        corrected = selected_payload.get("destination", "")
        suggested_state = selected_payload.get("state", "")
        destination = corrected
        st.markdown(
            f'<div class="atlas-card"><div class="atlas-choice-label">Selected place</div><strong>{html.escape(corrected)}</strong><br><span class="small-muted">{html.escape(selected_payload.get("display_name", suggested_state))}</span></div>',
            unsafe_allow_html=True,
        )
        suggested_geo = selected_payload
    else:
        destination = selected_label or ""
        corrected = normalize_destination(destination)
        suggested_geo = geocode_destination(corrected) if corrected else {}
        suggested_state = suggested_geo.get("state", "")
        if corrected:
            c1, c2 = st.columns(2)
            c1.info(f"Destination: {corrected}")
            c2.info(f"Suggested state: {suggested_state or 'Not found yet'}")
            if corrected != destination.strip():
                st.caption(f"Autocorrected destination: {corrected}")
    trip_purpose = st.selectbox(
        "What are you trying to understand?",
        ["General field observation", "Road trip stop", "Walk or commute", "Study abroad memory", "Community visit", "Food research", "Essay/podcast research", "Public field note"],
    )
    interests = st.multiselect(
        "Optional interests",
        ["history", "food", "race/community", "agriculture", "music", "religion", "economy", "small-town life", "nature", "sports"],
        default=["history", "food", "economy"],
    )
    custom_question = st.text_input(
        "Optional question",
        placeholder="What should I notice here? Why does this town feel this way? What industries dominate this region?",
    )
    generate = st.button("Generate Place Brief", width="stretch")

    if generate:
        if not (corrected or destination).strip():
            st.error("Please enter a destination first.")
        else:
            brief = generate_destination_brief(corrected or destination, suggested_state, trip_purpose, interests)
            if custom_question:
                brief["questions_to_ask"] = f"{custom_question} Start by asking locals what has changed, what outsiders miss, and which institutions still shape daily life."
            if selected_payload and not brief.get("latitude"):
                brief.update(
                    {
                        "latitude": selected_payload.get("latitude"),
                        "longitude": selected_payload.get("longitude"),
                        "display_name": selected_payload.get("display_name", brief.get("display_name")),
                    }
                )
            st.session_state.current_brief = brief

    brief = st.session_state.get("current_brief")
    if brief:
        title_line = ", ".join(part for part in [brief.get("destination"), brief.get("state")] if part)
        image_url = brief.get("image_url") or HERO_IMAGE_URL
        safe_title = html.escape(title_line)
        safe_location = html.escape(brief.get("display_name") or title_line)
        safe_brief = html.escape(brief.get("brief_15_sec", ""))
        st.markdown(
            f"""
            <div class="brief-hero" style="background-image: linear-gradient(180deg, rgba(9, 8, 6, 0.05), rgba(9, 8, 6, 0.74)), linear-gradient(90deg, rgba(9, 8, 6, 0.82), rgba(9, 8, 6, 0.08)), url('{image_url}');">
                <div>
                    <div class="atlas-kicker">Before You Arrive</div>
                    <h2>{safe_title}</h2>
                    <p>{safe_brief}</p>
                    <div class="atlas-pill-row"><span class="atlas-pill">{safe_location}</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if brief.get("latitude") and brief.get("longitude"):
            map_df = pd.DataFrame(
                [{"lat": brief["latitude"], "lon": brief["longitude"], "label": title_line}]
            )
            st.pydeck_chart(
                pdk.Deck(
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=map_df,
                            get_position="[lon, lat]",
                            get_radius=13000,
                            get_fill_color=[47, 111, 88, 210],
                            pickable=True,
                        )
                    ],
                    initial_view_state=pdk.ViewState(
                        latitude=brief["latitude"],
                        longitude=brief["longitude"],
                        zoom=9,
                    ),
                    tooltip={"text": "{label}"},
                ),
                use_container_width=True,
            )

        speech_text = " ".join(
            brief.get(key, "")
            for key in ["brief_15_sec", "historical_background", "cultural_signals", "local_food", "questions_to_ask", "safety_etiquette"]
        )
        speech_json = json.dumps(speech_text)
        components.html(
            f"""
            <div style="display:flex;gap:10px;align-items:center;">
              <button id="listen-brief" style="border:0;border-radius:999px;padding:12px 18px;background:#17211c;color:white;font-weight:800;cursor:pointer;">Listen to brief</button>
              <button id="stop-brief" style="border:1px solid rgba(23,33,28,.2);border-radius:999px;padding:11px 16px;background:white;color:#17211c;font-weight:800;cursor:pointer;">Stop</button>
            </div>
            <script>
              const briefText = {speech_json};
              const listen = document.getElementById("listen-brief");
              const stop = document.getElementById("stop-brief");
              listen.addEventListener("click", () => {{
                const utterance = new SpeechSynthesisUtterance(briefText);
                utterance.lang = "en-US";
                utterance.rate = 0.92;
                utterance.pitch = 1.0;
                const voices = window.speechSynthesis.getVoices();
                const nativeVoice = voices.find(v => v.lang === "en-US" && /Samantha|Alex|Google US English|Microsoft.*English/i.test(v.name))
                  || voices.find(v => v.lang === "en-US")
                  || voices.find(v => v.lang && v.lang.startsWith("en"));
                if (nativeVoice) utterance.voice = nativeVoice;
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(utterance);
              }});
              stop.addEventListener("click", () => window.speechSynthesis.cancel());
            </script>
            """,
            height=60,
        )

        section_labels = [
            ("historical_background", "Historical Background"),
            ("cultural_signals", "Cultural Signals"),
            ("local_food", "Food & Institutions"),
            ("questions_to_ask", "Questions To Ask"),
            ("field_note_prompts", "Field Note Prompts"),
            ("safety_etiquette", "Safety & Etiquette"),
        ]
        for row_start in range(0, len(section_labels), 2):
            cols = st.columns(2)
            for col, (key, label) in zip(cols, section_labels[row_start : row_start + 2]):
                with col:
                    icon = label.split()[0][:2].upper()
                    st.markdown(
                        f"""
                        <div class="brief-section">
                            <div class="brief-icon">{html.escape(icon)}</div>
                            <h4>{html.escape(label)}</h4>
                            <p>{html.escape(str(brief.get(key, "")))}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        with st.container(border=True):
            st.markdown("**Local institutions**")
            st.write(brief["local_institutions"])
        if brief.get("source_summaries"):
            with st.container(border=True):
                st.markdown("**Reference snapshots**")
                for item in brief["source_summaries"]:
                    st.markdown(f"- [{item.get('title')}]({item.get('url')}) - {item.get('description') or 'public reference'}")
        if brief.get("sources"):
            st.markdown("**Sources**")
            for source in brief["sources"]:
                st.markdown(f"- [{source['name']}]({source['url']})")
        if st.button("Save this brief"):
            brief_id = insert_ai_brief(brief)
            st.success(f"Saved brief #{brief_id}.")


def farmstay_log_page() -> None:
    st.title("Community Log")
    st.caption("A lightweight place-based memory for conversations, hospitality, local encounters, or community moments. Write freely; Waymark organizes later.")
    selected_location_label = st_searchbox(
        destination_search_options,
        placeholder="Where did this happen?",
        label=None,
        default="",
        default_use_searchterm=True,
        clear_on_submit=False,
        edit_after_submit="current",
        debounce=450,
        key="community_location_searchbox",
    )
    selected_location_payload = st.session_state.get("destination_payloads", {}).get(selected_location_label)
    if selected_location_label and not selected_location_payload:
        selected_location_payload = geocode_destination(selected_location_label)
    default_location = selected_location_payload.get("destination", selected_location_label) if selected_location_payload else selected_location_label
    default_latitude = selected_location_payload.get("latitude") if selected_location_payload else None
    default_longitude = selected_location_payload.get("longitude") if selected_location_payload else None

    with st.form("farmstay_form"):
        farm_name = st.text_input("Optional title", placeholder="Market conversation, dinner with hosts, town meeting...")
        farm_type = st.selectbox(
            "Moment type",
            ["local conversation", "community event", "farmstay", "market visit", "homestay", "volunteer day", "religious or civic gathering", "workshop", "other"],
        )
        reflection = st.text_area("What happened?", height=220, placeholder="Write it messily. Who was there, what was said, what surprised you, what should stay private?")
        people_met = st.text_input("Private people note", placeholder="Optional. Roles are safer than names.")
        community_feeling = st.slider("How strong did the community feeling seem?", 1, 5, 3)
        submitted = st.form_submit_button("Save Community Log")

    if submitted:
        work_done = reflection
        food_eaten = ""
        conversation_topics = reflection
        lifestyle_observations = reflection
        surprises = ""
        labor_intensity = 3
        payload = {
            "date": date.today().isoformat(),
            "farm_name": farm_name,
            "location_name": default_location,
            "latitude": default_latitude,
            "longitude": default_longitude,
            "farm_type": farm_type,
            "work_done": work_done,
            "people_met": people_met,
            "food_eaten": food_eaten,
            "conversation_topics": conversation_topics,
            "lifestyle_observations": lifestyle_observations,
            "labor_intensity": labor_intensity,
            "community_feeling": community_feeling,
            "surprises": surprises,
            "reflection": reflection,
        }
        payload["ai_summary"] = generate_farmstay_summary(payload)
        payload["public_version"] = create_public_version_for_farmstay(payload)
        log_id = insert_farmstay_log(payload)
        st.success(f"Saved community log #{log_id}.")
        with st.container(border=True):
            st.subheader(farm_name or "Community log")
            st.write(payload["ai_summary"])
            st.markdown("**Anonymized public version preview**")
            st.write(payload["public_version"])


def filter_library(items: pd.DataFrame) -> pd.DataFrame:
    filtered = items.copy()
    c1, c2, c3, c4 = st.columns(4)
    category = c1.selectbox("Category", ["All"] + sorted({str(x) for x in filtered["display_category"].dropna() if str(x)}))
    state = c2.selectbox("State", ["All"] + sorted({str(x) for x in filtered.get("display_state", pd.Series()).dropna() if str(x)}))
    privacy = c3.selectbox("Privacy", ["All"] + sorted({str(x) for x in filtered.get("privacy_level", pd.Series()).dropna() if str(x)}))
    tag = c4.text_input("Tag search")
    keyword = st.text_input("Search title, place, summary, and note text")

    if category != "All":
        filtered = filtered[filtered["display_category"].astype(str) == category]
    if state != "All":
        filtered = filtered[filtered["display_state"].astype(str) == state]
    if privacy != "All":
        filtered = filtered[filtered.get("privacy_level", "").astype(str) == privacy]
    if tag:
        filtered = filtered[filtered.get("tags", "").fillna("").str.contains(tag, case=False, na=False)]
    if keyword:
        searchable = filtered[
            ["display_title", "display_location", "display_category", "display_text", "ai_summary"]
        ].fillna("").astype(str).agg(" ".join, axis=1)
        filtered = filtered[searchable.str.contains(keyword, case=False, na=False)]
    return filtered


def render_review_text(item: pd.Series) -> str:
    text = str(item.get("display_text") or item.get("note_text") or "").strip()
    if not text and str(item.get("source_type")) == "Community log":
        parts = [
            item.get("work_done", ""),
            item.get("conversation_topics", ""),
            item.get("lifestyle_observations", ""),
            item.get("reflection", ""),
        ]
        text = " ".join(str(part).strip() for part in parts if str(part).strip())
    if not text:
        text = str(item.get("ai_summary") or "No review text recorded yet.").strip()
    return text[:700] + ("..." if len(text) > 700 else "")


def note_library_page() -> None:
    st.title("Search Notes")
    st.caption("Find private notes, community logs, and public-ready reflections by place, theme, tag, or keyword.")
    items = fetch_all_library_items()
    if items.empty:
        st.info("No notes yet.")
        return
    filtered = filter_library(items)
    st.caption(f"{len(filtered)} item(s)")

    for _, item in filtered.iterrows():
        with st.container(border=True):
            cols = st.columns([3, 1])
            cols[0].subheader(item.get("display_title") or "Untitled")
            cols[1].markdown(f"**{item.get('source_type')}**")
            st.write(f"{item.get('date', '')} | {item.get('display_location', '')} | {item.get('display_category', '')}")
            st.caption(f"Privacy: {item.get('privacy_level', 'private')}")
            st.markdown("**Field review**")
            st.write(render_review_text(item))
            if item.get("ai_summary"):
                st.caption(f"AI context: {item.get('ai_summary')}")
            b1, b2, b3 = st.columns(3)
            detail_key = f"detail_{item.get('source_type')}_{item.get('source_id')}"
            public_key = f"public_{item.get('source_type')}_{item.get('source_id')}"
            if b1.button("View Details", key=detail_key):
                st.session_state.selected_detail = (item.get("source_type"), int(item.get("source_id")))
            if b2.button("Create Public Version", key=public_key):
                st.session_state.selected_public = (item.get("source_type"), int(item.get("source_id")))
                st.session_state.page = "Publish Safely"
                st.rerun()
            if b3.button("Export", key=f"export_{item.get('source_type')}_{item.get('source_id')}"):
                st.session_state.export_selection = [f"{item.get('source_type')}:{item.get('source_id')}"]
                st.session_state.page = "Export"
                st.rerun()

    if st.session_state.get("selected_detail"):
        source_type, source_id = st.session_state.selected_detail
        st.divider()
        st.subheader("Readable Details")
        record = get_field_note(source_id) if source_type == "Field note" else None
        if source_type == "Community log":
            farms = fetch_farmstay_logs()
            match = farms[farms["id"] == source_id]
            record = match.iloc[0].to_dict() if not match.empty else None
        if record:
            for label, value in record.items():
                if value not in (None, ""):
                    st.markdown(f"**{label.replace('_', ' ').title()}**")
                    st.write(value)


def journey_review_page() -> None:
    st.title("Journey Review")
    st.caption("A simple reflection view: choose a set of notes, see the strongest places and themes, then draft a private or public reflection.")
    items = fetch_all_library_items()
    if items.empty:
        st.info("Capture a note first, then come back here to review the journey.")
        return

    c1, c2 = st.columns(2)
    places = sorted({str(value) for value in items["display_location"].dropna() if str(value)})
    themes = sorted({str(value) for value in items["display_category"].dropna() if str(value)})
    selected_place = c1.selectbox("Place", ["All"] + places)
    selected_theme = c2.selectbox("Theme", ["All"] + themes)
    max_items = 6

    filtered = items.copy()
    if selected_place != "All":
        filtered = filtered[filtered["display_location"].astype(str) == selected_place]
    if selected_theme != "All":
        filtered = filtered[filtered["display_category"].astype(str) == selected_theme]
    filtered = filtered.head(max_items)
    if filtered.empty:
        st.info("No notes match this review filter.")
        return

    notice_lines = []
    for _, row in filtered.iterrows():
        text = render_review_text(row)
        notice_lines.append(f"{row.get('display_location')}: {text}")
    place_counts = filtered["display_location"].fillna("Unknown place").value_counts()
    theme_counts = filtered["display_category"].fillna("personal reflection").value_counts()

    st.markdown("### Notes in This Reflection")
    for line in notice_lines[:5]:
        st.markdown(f"- {line}")

    st.markdown("### Places That Mattered")
    st.write(", ".join(place_counts.index[:6]))

    st.markdown("### Recurring Themes")
    st.write(", ".join(f"{theme} ({count})" for theme, count in theme_counts.items()))

    public_draft = (
        "I moved through a set of U.S. places with a notebook mindset rather than a checklist. "
        f"The strongest memories clustered around {', '.join(place_counts.index[:3])}. "
        f"Recurring themes included {', '.join(theme_counts.index[:4])}. "
        "The public version should keep the feeling of movement and observation while removing exact addresses, private names, raw transcripts, and real-time details."
    )
    st.markdown("### Reflection Draft")
    st.text_area("Draft", public_draft, height=220)


def get_selected_items(selection: list[str], items: pd.DataFrame) -> list[dict]:
    selected: list[dict] = []
    for token in selection:
        try:
            source_type, source_id = token.split(":", 1)
        except ValueError:
            continue
        match = items[(items["source_type"] == source_type) & (items["source_id"].astype(str) == source_id)]
        if not match.empty:
            selected.append(match.iloc[0].to_dict())
    return selected


def export_center_page() -> None:
    st.title("Export")
    items = fetch_all_library_items()
    if items.empty:
        st.info("Add notes before exporting.")
        return

    options = [f"{row.source_type}:{row.source_id}" for row in items.itertuples()]
    labels = {f"{row.source_type}:{row.source_id}": f"{row.source_type} | {row.display_title} | {row.display_location}" for row in items.itertuples()}
    default = st.session_state.pop("export_selection", [])
    selection = st.multiselect("Select one or more notes", options, default=default, format_func=lambda value: labels.get(value, value))
    export_type = st.selectbox("Export format", EXPORT_TYPES)

    if st.button("Generate Export"):
        selected_items = get_selected_items(selection, items)
        if not selected_items:
            st.error("Please select at least one note.")
            return
        title, content = generate_export(export_type, selected_items)
        st.session_state.generated_export = {"title": title, "content": content, "items": selected_items, "type": export_type}

    generated = st.session_state.get("generated_export")
    if generated:
        st.subheader(generated["title"])
        st.text_area("Generated content", generated["content"], height=420)
        if st.button("Save Export Record"):
            export_id = save_export(generated["type"], generated["items"], generated["content"], generated["title"])
            st.success(f"Saved export #{export_id}.")


def privacy_page() -> None:
    st.title("Publish Safely")
    st.warning("Public versions are drafts. Please manually review before publishing.")
    st.markdown(
        """
        Select a note, generate an anonymous public version, then review what was removed.
        Exact place, exact date, raw transcript, names, affiliations, and real-time movement stay private by default.
        """
    )

    if st.session_state.get("selected_public") and st.session_state.selected_public[0] == "Community log":
        log = get_farmstay_log(int(st.session_state.selected_public[1]))
        if log:
            st.subheader("Community public version")
            st.text_area("Public text", create_public_version_for_farmstay(log), height=320)
            st.markdown("**Removed/private details checklist**")
            for item in [
                "Exact farm name generalized",
                "Exact date generalized",
                "Private people and affiliations removed where detected",
                "Written as an anonymous travel reflection",
                "Manual review still required before publishing",
            ]:
                st.checkbox(item, value=True, disabled=True)
            st.divider()

    notes = fetch_field_notes()
    if notes.empty:
        st.info("No field notes available.")
        return

    options = notes["id"].astype(str).tolist()
    labels = {str(row.id): f"{row.title} | {row.location_name} | {row.date}" for row in notes.itertuples()}
    default_id = None
    if st.session_state.get("selected_public") and st.session_state.selected_public[0] == "Field note":
        default_id = str(st.session_state.selected_public[1])
    selected = st.selectbox(
        "Select a field note",
        options,
        index=options.index(default_id) if default_id in options else 0,
        format_func=lambda value: labels.get(value, value),
    )

    if st.button("Create anonymized public version"):
        note = get_field_note(int(selected))
        if note:
            st.session_state.public_version = create_public_version_for_note(note)

    public = st.session_state.get("public_version")
    if public:
        st.subheader(public["public_title"])
        st.caption(f"Public location level: {public['public_location']}")
        st.text_area("Public text", public["public_text"], height=320)
        st.markdown("**Removed/private details checklist**")
        for item in public["removed_checklist"]:
            st.checkbox(item, value=True, disabled=True)


def main() -> None:
    apply_style()
    pages = [
        "Home",
        "Memory Map",
        "Read Reviews",
        "Search My Notes",
        "Capture Note",
        "Ask About This Place",
        "Community Log",
        "Journey Review",
        "Library",
        "Export",
        "Publish Safely",
    ]
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if st.session_state.page not in pages:
        st.session_state.page = "Home"
    page = render_sidebar(pages)
    st.session_state.page = page

    if page == "Home":
        home_page()
    elif page == "Memory Map":
        map_view_page()
    elif page == "Read Reviews":
        note_library_page()
    elif page == "Capture Note":
        add_field_note_page()
    elif page == "Search My Notes":
        note_library_page()
    elif page == "Ask About This Place":
        ai_companion_page()
    elif page == "Community Log":
        farmstay_log_page()
    elif page == "Journey Review":
        journey_review_page()
    elif page == "Library":
        note_library_page()
    elif page == "Export":
        export_center_page()
    elif page == "Publish Safely":
        privacy_page()


if __name__ == "__main__":
    main()
