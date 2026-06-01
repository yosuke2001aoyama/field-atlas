from __future__ import annotations

import html
import json
import re
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
    CURATED_US_DESTINATIONS,
    STATE_CITY_SUGGESTIONS,
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
    "food": ["food", "meal", "diner", "coffee", "market", "restaurant", "bread", "breakfast", "pizza", "cuisine", "dish", "ate"],
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
GUIDEBOOK_INTERESTS = [
    "history",
    "food",
    "race/community",
    "agriculture",
    "music",
    "religion",
    "economy",
    "politics",
    "small-town life",
    "nature",
    "sports",
]

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
        {"name": "I-5", "path": [[-117.1611, 32.7157], [-118.2437, 34.0522], [-122.4194, 37.7749], [-122.3321, 47.6062]]},
        {"name": "I-90", "path": [[-122.3321, 47.6062], [-104.9903, 39.7392], [-87.6298, 41.8781], [-74.0060, 40.7128]]},
        {"name": "I-10", "path": [[-118.2437, 34.0522], [-95.3698, 29.7604], [-90.0715, 29.9511], [-80.1918, 25.7617]]},
        {"name": "I-15", "path": [[-117.1611, 32.7157], [-115.1398, 36.1699], [-111.8910, 40.7608], [-112.0391, 46.5891]]},
        {"name": "I-25", "path": [[-106.6504, 35.0844], [-104.9903, 39.7392], [-104.8214, 41.1400]]},
        {"name": "I-40", "path": [[-118.2437, 34.0522], [-112.0740, 33.4484], [-97.5164, 35.4676], [-86.7816, 36.1627], [-78.6382, 35.7796], [-77.9447, 34.2257]]},
        {"name": "I-70", "path": [[-111.8910, 40.7608], [-104.9903, 39.7392], [-94.5786, 39.0997], [-86.1581, 39.7684], [-77.0369, 38.9072]]},
        {"name": "I-75", "path": [[-80.1918, 25.7617], [-84.3880, 33.7490], [-84.5120, 39.1031], [-83.0458, 42.3314]]},
        {"name": "I-81", "path": [[-83.9207, 35.9606], [-80.8431, 35.2271], [-77.4360, 37.5407], [-76.1474, 43.0481]]},
        {"name": "I-94", "path": [[-93.2650, 44.9778], [-87.6298, 41.8781], [-83.0458, 42.3314], [-77.0369, 38.9072]]},
        {"name": "I-95", "path": [[-80.1918, 25.7617], [-84.3880, 33.7490], [-74.0060, 40.7128]]},
        {"name": "I-35", "path": [[-97.7431, 30.2672], [-97.3308, 37.6872], [-93.2650, 44.9778]]},
        {"name": "I-80", "path": [[-122.4194, 37.7749], [-104.9903, 39.7392], [-87.6298, 41.8781], [-74.0060, 40.7128]]},
    ]
)

STATE_CENTERS = {
    "Alabama": (32.8067, -86.7911), "Alaska": (61.3707, -152.4044), "Arizona": (33.7298, -111.4312),
    "Arkansas": (34.9697, -92.3731), "California": (36.1162, -119.6816), "Colorado": (39.0598, -105.3111),
    "Connecticut": (41.5978, -72.7554), "Delaware": (39.3185, -75.5071), "Florida": (27.7663, -81.6868),
    "Georgia": (33.0406, -83.6431), "Hawaii": (21.0943, -157.4983), "Idaho": (44.2405, -114.4788),
    "Illinois": (40.3495, -88.9861), "Indiana": (39.8494, -86.2583), "Iowa": (42.0115, -93.2105),
    "Kansas": (38.5266, -96.7265), "Kentucky": (37.6681, -84.6701), "Louisiana": (31.1695, -91.8678),
    "Maine": (44.6939, -69.3819), "Maryland": (39.0639, -76.8021), "Massachusetts": (42.2302, -71.5301),
    "Michigan": (43.3266, -84.5361), "Minnesota": (45.6945, -93.9002), "Mississippi": (32.7416, -89.6787),
    "Missouri": (38.4561, -92.2884), "Montana": (46.9219, -110.4544), "Nebraska": (41.1254, -98.2681),
    "Nevada": (38.3135, -117.0554), "New Hampshire": (43.4525, -71.5639), "New Jersey": (40.2989, -74.5210),
    "New Mexico": (34.8405, -106.2485), "New York": (42.1657, -74.9481), "North Carolina": (35.6301, -79.8064),
    "North Dakota": (47.5289, -99.7840), "Ohio": (40.3888, -82.7649), "Oklahoma": (35.5653, -96.9289),
    "Oregon": (44.5720, -122.0709), "Pennsylvania": (40.5908, -77.2098), "Rhode Island": (41.6809, -71.5118),
    "South Carolina": (33.8569, -80.9450), "South Dakota": (44.2998, -99.4388), "Tennessee": (35.7478, -86.6923),
    "Texas": (31.0545, -97.5635), "Utah": (40.1500, -111.8624), "Vermont": (44.0459, -72.7107),
    "Virginia": (37.7693, -78.1700), "Washington": (47.4009, -121.4905), "West Virginia": (38.4912, -80.9545),
    "Wisconsin": (44.2685, -89.6165), "Wyoming": (42.7560, -107.3025),
}

PLACE_BRIEF_CANDIDATES = pd.DataFrame(
    [
        {
            "source": "Brief candidate",
            "source_id": f"curated-{idx}",
            "title": item["destination"],
            "location": f'{item["destination"]}, {item["state"]}',
            "state": item["state"],
            "category": item["kind"],
            "latitude": item["latitude"],
            "longitude": item["longitude"],
            "summary": "Click to open a guidebook-style place brief.",
            "color": [183, 150, 93],
        }
        for idx, item in enumerate(CURATED_US_DESTINATIONS)
    ]
    + [
        {"source": "Brief candidate", "source_id": "tourism-acadia", "title": "Acadia National Park", "location": "Acadia National Park, Maine", "state": "Maine", "category": "national park", "latitude": 44.3386, "longitude": -68.2733, "summary": "Click to open a guidebook-style place brief.", "color": [183, 150, 93]},
        {"source": "Brief candidate", "source_id": "tourism-smokies", "title": "Great Smoky Mountains National Park", "location": "Great Smoky Mountains National Park, Tennessee", "state": "Tennessee", "category": "national park", "latitude": 35.6532, "longitude": -83.5070, "summary": "Click to open a guidebook-style place brief.", "color": [183, 150, 93]},
        {"source": "Brief candidate", "source_id": "tourism-zion", "title": "Zion National Park", "location": "Zion National Park, Utah", "state": "Utah", "category": "national park", "latitude": 37.2982, "longitude": -113.0263, "summary": "Click to open a guidebook-style place brief.", "color": [183, 150, 93]},
        {"source": "Brief candidate", "source_id": "tourism-yosemite", "title": "Yosemite National Park", "location": "Yosemite National Park, California", "state": "California", "category": "national park", "latitude": 37.8651, "longitude": -119.5383, "summary": "Click to open a guidebook-style place brief.", "color": [183, 150, 93]},
        {"source": "Brief candidate", "source_id": "tourism-independence", "title": "Independence National Historical Park", "location": "Independence National Historical Park, Pennsylvania", "state": "Pennsylvania", "category": "historical park", "latitude": 39.9489, "longitude": -75.1500, "summary": "Click to open a guidebook-style place brief.", "color": [183, 150, 93]},
        {"source": "Brief candidate", "source_id": "tourism-gettysburg", "title": "Gettysburg National Military Park", "location": "Gettysburg National Military Park, Pennsylvania", "state": "Pennsylvania", "category": "historical park", "latitude": 39.8309, "longitude": -77.2311, "summary": "Click to open a guidebook-style place brief.", "color": [183, 150, 93]},
        {"source": "Brief candidate", "source_id": "tourism-grand-teton", "title": "Grand Teton National Park", "location": "Grand Teton National Park, Wyoming", "state": "Wyoming", "category": "national park", "latitude": 43.7904, "longitude": -110.6818, "summary": "Click to open a guidebook-style place brief.", "color": [183, 150, 93]},
        {"source": "Brief candidate", "source_id": "tourism-everglades", "title": "Everglades National Park", "location": "Everglades National Park, Florida", "state": "Florida", "category": "national park", "latitude": 25.2866, "longitude": -80.8987, "summary": "Click to open a guidebook-style place brief.", "color": [183, 150, 93]},
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
                overflow-x: hidden;
            }

            .block-container {
                width: min(1220px, calc(100vw - 2rem));
                max-width: 100%;
                padding-top: 1.6rem;
                padding-bottom: 4rem;
            }

            #MainMenu, footer, header,
            [data-testid="stToolbar"],
            [data-testid="stDecoration"],
            [data-testid="stStatusWidget"],
            [data-testid="stHeader"],
            .stDeployButton {
                visibility: hidden;
                height: 0;
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
                width: 100%;
                max-width: 100%;
                min-height: 46vh;
                display: grid;
                align-items: end;
                overflow: hidden;
                box-sizing: border-box;
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
                font-size: clamp(3rem, 6.4vw, 5.8rem);
                line-height: 0.9;
                margin: 0.35rem 0 0.65rem;
                max-width: 850px;
                overflow-wrap: break-word;
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
                min-height: 19rem;
                padding: 1.55rem;
                border: 1px solid rgba(62, 48, 33, 0.16);
                background: rgba(255, 252, 246, 0.88);
                background-size: cover;
                background-position: center;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
                box-shadow: 0 22px 60px rgba(35, 24, 13, 0.08);
            }

            .journey-card.before-card {
                background:
                    linear-gradient(180deg, rgba(255,252,246,0.90), rgba(255,252,246,0.96)),
                    url("https://images.unsplash.com/photo-1524661135-423995f22d0b?auto=format&fit=crop&w=1200&q=70");
            }

            .journey-card.after-card {
                background:
                    linear-gradient(180deg, rgba(255,252,246,0.88), rgba(255,252,246,0.96)),
                    url("https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=70");
            }

            .journey-icon {
                width: 3rem;
                height: 3rem;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 1.1rem;
                color: #ffffff;
                background: #17211c;
                border-radius: 999px;
            }

            .journey-icon svg {
                width: 1.45rem;
                height: 1.45rem;
                fill: none;
                stroke: currentColor;
                stroke-width: 1.8;
                stroke-linecap: round;
                stroke-linejoin: round;
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

            .brief-section strong,
            .guide-strong {
                color: #8d5d3e;
                font-weight: 900;
                background: rgba(183, 150, 93, 0.14);
                padding: 0.02rem 0.22rem;
                border-radius: 0.2rem;
            }

            .browser-voice-box {
                border: 1px solid rgba(62, 48, 33, 0.16);
                background: rgba(255, 252, 246, 0.82);
                padding: 1rem;
                margin: 0.4rem 0 0.8rem;
            }

            .browser-voice-box button {
                border: 0;
                border-radius: 999px;
                padding: 0.84rem 1.2rem;
                background: #17211c;
                color: #fff;
                font-weight: 800;
                cursor: pointer;
            }

            .browser-voice-box audio {
                width: 100%;
                margin-top: 0.85rem;
            }

            .quick-record-panel {
                margin: 0 0 1.25rem;
                padding: 1.05rem;
                border: 1px solid rgba(62, 48, 33, 0.16);
                background: rgba(255, 252, 246, 0.86);
                box-shadow: 0 18px 46px rgba(35, 24, 13, 0.07);
                min-height: 10.4rem;
            }

            .quick-record-panel h3 {
                margin: 0 0 0.2rem;
                font-size: 1.35rem;
            }

            .quick-record-panel p {
                color: var(--atlas-muted);
                margin: 0;
            }

            .brief-icon {
                display: inline-flex;
                width: 2.45rem;
                height: 2.45rem;
                align-items: center;
                justify-content: center;
                margin-bottom: 0.75rem;
                border-radius: 999px;
                color: #fff;
                background: #17211c;
            }

            .brief-icon svg {
                width: 1.28rem;
                height: 1.28rem;
                fill: none;
                stroke: currentColor;
                stroke-width: 1.9;
                stroke-linecap: round;
                stroke-linejoin: round;
            }

            .field-anchor-card {
                overflow: hidden;
                border: 1px solid rgba(62, 48, 33, 0.16);
                background: rgba(255, 252, 246, 0.92);
                box-shadow: 0 22px 58px rgba(35, 24, 13, 0.08);
                margin-bottom: 1.1rem;
            }

            .field-anchor-card img {
                width: 100%;
                aspect-ratio: 16 / 9;
                object-fit: cover;
                display: block;
            }

            .field-anchor-card div {
                padding: 1.2rem;
            }

            .field-anchor-card h4 {
                font-family: Newsreader, Georgia, serif;
                margin: 0 0 0.45rem;
                font-size: 1.5rem;
            }

            .field-anchor-card p {
                color: var(--atlas-muted);
                line-height: 1.62;
                margin: 0;
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

            @media (max-width: 820px) {
                .block-container {
                    width: calc(100vw - 1.4rem);
                    max-width: calc(100vw - 1.4rem);
                    padding: 0.8rem 0.7rem 4.5rem;
                }

                [data-testid="stSidebar"]::before {
                    display: none;
                }

                [data-testid="stSidebar"] {
                    background: rgba(250, 247, 240, 0.96);
                }

                .atlas-hero {
                    min-height: 31rem;
                    padding: 1.15rem;
                    margin: 0 0 1.1rem;
                }

                .atlas-hero h1 {
                    font-size: 3rem;
                    line-height: 0.95;
                }

                .atlas-hero h3 {
                    font-size: 1.18rem;
                }

                .atlas-hero p {
                    font-size: 0.96rem;
                    line-height: 1.55;
                }

                .atlas-pill-row {
                    gap: 0.4rem;
                }

                .atlas-pill {
                    font-size: 0.72rem;
                    padding: 0.38rem 0.55rem;
                }

                .journey-card {
                    min-height: 12rem;
                    padding: 1.05rem;
                    margin-bottom: 0.7rem;
                }

                .journey-card h3 {
                    font-size: 1.55rem;
                }

                .brief-hero {
                    min-height: 24rem;
                    padding: 1.1rem;
                }

                .brief-hero h2 {
                    font-size: 2.35rem;
                }

                .brief-section {
                    min-height: auto;
                    padding: 1rem;
                }

                .quick-record-panel {
                    display: block;
                    padding: 0.95rem;
                }
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


def update_field_note_privacy_local(note_id: int, privacy_level: str) -> None:
    db_path = BASE_DIR / "data" / "field_atlas.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "UPDATE field_notes SET privacy_level = ?, updated_at = ? WHERE id = ?",
            (privacy_level, datetime.now().isoformat(timespec="seconds"), note_id),
        )


def render_sidebar(pages: list[str]) -> str:
    nav_labels = {
        "Home": "Home",
        "Memory Map": "Memory Map",
        "Search My Notes": "Search Notes",
        "Capture Note": "Capture Note",
        "Ask About This Place": "Ask About This Place",
        "Community Log": "Capture",
        "Personal Log": "Personal Log",
        "Library": "Library",
        "Export": "Export",
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
    st.sidebar.markdown('<div class="nav-section">Before</div>', unsafe_allow_html=True)
    nav_button("Ask About This Place")
    nav_button("Memory Map")
    st.sidebar.markdown('<div class="nav-section">After</div>', unsafe_allow_html=True)
    nav_button("Capture Note")
    nav_button("Personal Log")
    nav_button("Journey Review")
    return st.session_state.page


def render_top_nav(pages: list[str]) -> None:
    with st.expander("Navigate Waymark U.S.", expanded=False):
        st.markdown('<div class="top-nav-wrap">', unsafe_allow_html=True)
        rows = [
            [("Home", "Home"), ("Ask About This Place", "Read a Place Brief"), ("Memory Map", "Memory Map")],
            [("Capture Note", "Mic / Capture"), ("Personal Log", "Personal Log"), ("Library", "Library")],
            [("Journey Review", "Journey Review"), ("Export", "Export")],
        ]
        for row in rows:
            cols = st.columns(len(row))
            for col, (page, label) in zip(cols, row):
                with col:
                    if page == st.session_state.page:
                        st.markdown(f'<div class="top-nav-active">{html.escape(label)}</div>', unsafe_allow_html=True)
                    elif st.button(label, key=f"top_nav_{page}", width="stretch"):
                        st.session_state.page = page
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def go_to(page_name: str) -> None:
    st.session_state.page = page_name
    st.rerun()


def guide_text_html(text: str) -> str:
    safe = html.escape(str(text or ""))
    return re.sub(r"\*\*(.+?)\*\*", r'<strong class="guide-strong">\1</strong>', safe)


def clean_voice_text(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", (text or "").strip())
    replacements = {
        "why do i need to do": "what do I need to do",
        "why do i need to see": "what do I need to see",
        "why should i visit": "what should I visit",
        "way mark": "Waymark",
        "waymarks": "Waymark",
        "new orleans": "New Orleans",
        "chicargo": "Chicago",
        "chicago illinois": "Chicago, Illinois",
        "boston massachusetts": "Boston, Massachusetts",
        "grand canyon": "Grand Canyon",
    }
    lowered = cleaned.lower()
    for wrong, right in replacements.items():
        lowered = re.sub(rf"\b{re.escape(wrong)}\b", right, lowered, flags=re.IGNORECASE)
    for item in CURATED_US_DESTINATIONS:
        lowered = re.sub(
            rf"\b{re.escape(item['destination'])}\b",
            item["destination"],
            lowered,
            flags=re.IGNORECASE,
        )
    for state_name, cities in STATE_CITY_SUGGESTIONS.items():
        lowered = re.sub(rf"\b{re.escape(state_name)}\b", state_name, lowered, flags=re.IGNORECASE)
        for city_name in cities:
            lowered = re.sub(rf"\b{re.escape(city_name)}\b", city_name, lowered, flags=re.IGNORECASE)
    if lowered:
        lowered = lowered[0].upper() + lowered[1:]
    return lowered


def is_voice_question(text: str) -> bool:
    cleaned = clean_voice_text(text).lower()
    if "?" in cleaned:
        return True
    question_starters = (
        "what ",
        "why ",
        "how ",
        "where ",
        "when ",
        "who ",
        "which ",
        "should i ",
        "can you ",
        "tell me ",
        "do i ",
        "is there ",
        "are there ",
        "i want to know",
        "i'd like to know",
        "i would like to know",
        "i was wondering",
        "i wonder",
        "i am wondering",
        "i'm wondering",
        "i need to know",
        "help me understand",
    )
    question_phrases = (
        "what should i notice",
        "what do i need to do",
        "what should i do",
        "what should i visit",
        "what is important",
        "where should i go",
        "why does",
        "want to know",
        "was wondering if",
        "was wondering whether",
        "help me understand",
    )
    return cleaned.startswith(question_starters) or any(phrase in cleaned for phrase in question_phrases)


def voice_question_topic(text: str) -> str:
    q = clean_voice_text(text).lower()
    topic_keywords = {
        "sports_snapshot": ["sport", "team", "baseball", "football", "basketball", "hockey", "soccer", "stadium"],
        "food_snapshot": ["food", "eat", "dish", "restaurant", "cuisine", "pizza", "barbecue", "breakfast"],
        "politics_snapshot": ["politic", "election", "trump", "biden", "democrat", "republican", "vote"],
        "industry_snapshot": ["industry", "economy", "job", "employer", "company", "work"],
        "population_snapshot": ["population", "people", "how big", "metro"],
        "historical_background": ["history", "historic", "historical", "past"],
    }
    for topic, keywords in topic_keywords.items():
        if any(keyword in q for keyword in keywords):
            return topic
    return "general"


def answer_voice_question(text: str, brief: dict | None = None) -> str:
    topic = voice_question_topic(text)
    if brief and topic != "general":
        return str(brief.get(topic) or brief.get("brief_15_sec") or answer_home_question(text))
    if brief:
        destination = ", ".join(part for part in [brief.get("destination"), brief.get("state")] if part)
        return (
            f"I opened the full place brief for {destination}. "
            f"{brief.get('brief_15_sec', '')} "
            "Start with the Field Anchors section, then scan population, industries, food, sports, and politics."
        )
    return answer_home_question(text)


def infer_destination_from_text(text: str) -> tuple[str, str]:
    cleaned = clean_voice_text(text)
    lowered = cleaned.lower()
    for item in CURATED_US_DESTINATIONS:
        if item["destination"].lower() in lowered:
            return item["destination"], item["state"]
    match = re.search(r"\b(?:in|about|for|near|to)\s+([A-Z][A-Za-z .'-]+?)(?:\?|$|,|\.| please| today| tomorrow)", cleaned)
    if match:
        destination = normalize_destination(match.group(1).strip())
        geo = geocode_destination(destination)
        return destination, geo.get("state", "")
    return "", ""


def save_text_log_from_voice(text: str) -> int:
    raw = text
    cleaned = clean_voice_text(text)
    destination, state = infer_destination_from_text(cleaned)
    geo = geocode_destination(destination, state) if destination else {}
    category = classify_note_theme(cleaned, "voice", "curious")
    location = destination or geo.get("city") or ""
    ai_summary = generate_public_ready_summary(cleaned, location, category)
    ai_context = generate_ai_context(cleaned, category, location)
    title = generate_note_title_from_text(cleaned, "Voice field note")
    return insert_field_note(
        {
            "title": title,
            "date": datetime.now().isoformat(timespec="minutes"),
            "location_name": location,
            "address": "",
            "latitude": geo.get("latitude"),
            "longitude": geo.get("longitude"),
            "city": geo.get("city", destination),
            "state": geo.get("state", state),
            "category": category,
            "note_text": cleaned,
            "photo_path": "",
            "audio_path": "",
            "audio_transcript": raw,
            "mood": "curious",
            "ai_summary": ai_summary,
            "ai_context": ai_context,
            "tags": "voice",
            "privacy_level": "private",
        }
    )


def generate_note_title_from_text(text: str, fallback: str = "Moving thought") -> str:
    cleaned = clean_voice_text(text)
    if not cleaned:
        return fallback
    destination, _ = infer_destination_from_text(cleaned)
    category = classify_note_theme(cleaned, "voice", "curious")
    first_words = " ".join(cleaned.split()[:7]).strip("., ")
    if destination:
        return f"{category.title()} in {destination}"
    return first_words or fallback


def handle_voice_query_params() -> None:
    action = st.query_params.get("voice_action", "")
    text = st.query_params.get("voice_text", "")
    if isinstance(action, list):
        action = action[0] if action else ""
    if isinstance(text, list):
        text = text[0] if text else ""
    if not action or not text:
        return
    cleaned = clean_voice_text(text)
    voice_key = f"{action}:{cleaned}"
    if st.session_state.get("last_voice_query") == voice_key:
        return
    st.session_state.last_voice_query = voice_key
    if action == "auto":
        action = "ask" if is_voice_question(cleaned) else "log"
    if action == "log":
        note_id = save_text_log_from_voice(cleaned)
        st.session_state.voice_result = f"Saved private voice log #{note_id}."
        st.session_state.voice_spoken_answer = "Saved as a private personal log. I cleaned up the transcript and created a title for it."
        st.session_state.page = "Library"
        return
    if action == "ask":
        destination, state = infer_destination_from_text(cleaned)
        st.session_state.voice_result = f"Transcript: {cleaned}"
        brief = generate_destination_brief(destination, state, "Voice question", GUIDEBOOK_INTERESTS) if destination else None
        st.session_state.voice_answer = answer_voice_question(cleaned, brief)
        st.session_state.voice_spoken_answer = st.session_state.voice_answer
        st.session_state.ask_prefill = cleaned
        if destination:
            st.session_state.ask_place_prefill = ", ".join(part for part in [destination, state] if part)
        if destination:
            st.session_state.current_brief = brief
            st.session_state.page = "Understand"
        else:
            st.session_state.page = "Ask"


def render_browser_voice_helper(component_key: str) -> None:
    components.html(
        """
        <style>
          body { margin: 0; font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: transparent; }
          .browser-voice-box {
            border: 1px solid rgba(62, 48, 33, 0.16);
            background: rgba(255, 252, 246, 0.92);
            padding: 14px;
            color: #161411;
            box-sizing: border-box;
          }
          #recordVoice {
            border: 0;
            border-radius: 999px;
            padding: 14px 20px;
            background: linear-gradient(135deg, #17211c, #2f6f58);
            color: #fff;
            font-weight: 850;
            font-size: 15px;
            cursor: pointer;
            box-shadow: 0 12px 24px rgba(23,33,28,.18);
          }
          #recordVoice[disabled] { opacity: .55; cursor: not-allowed; }
          #voiceStatus { margin-left: 12px; color: #746d62; font-size: 15px; }
          #voiceTranscript {
            width: 100%;
            min-height: 74px;
            margin-top: 12px;
            border: 1px solid rgba(62,48,33,.18);
            border-radius: 12px;
            padding: 10px;
            box-sizing: border-box;
            font: inherit;
            color: #161411;
            background: rgba(255,255,255,.76);
          }
          .voice-actions { display:flex; gap:8px; flex-wrap:wrap; margin-top:10px; }
          .voice-actions button {
            border: 1px solid rgba(23,33,28,.18);
            border-radius: 999px;
            padding: 10px 13px;
            background: white;
            color: #17211c;
            font-weight: 800;
            cursor: pointer;
          }
          .mic-icon { font-size: 0.78rem; letter-spacing: 0.06rem; margin-right: 0.34rem; opacity: 0.86; }
        </style>
        <div class="browser-voice-box">
          <button id="recordVoice"><span class="mic-icon">MIC</span> Start</button>
          <span id="voiceStatus" style="margin-left:10px;color:#746d62;">Ready for a walk, car, station, kitchen, or street note.</span>
          <textarea id="voiceTranscript" placeholder="Your transcript appears here, without leaving the page."></textarea>
          <div class="voice-actions">
            <button id="askWaymark" type="button">Ask Waymark</button>
            <button id="saveLog" type="button">Save as Private Note</button>
          </div>
        </div>
        <script>
          const button = document.getElementById("recordVoice");
          const status = document.getElementById("voiceStatus");
          const transcript = document.getElementById("voiceTranscript");
          const askWaymark = document.getElementById("askWaymark");
          const saveLog = document.getElementById("saveLog");
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          let recognition = null;
          let listening = false;
          let autoSubmitted = false;
          let silenceTimer = null;
          function looksLikeQuestion(text) {
            const cleaned = text.trim().toLowerCase();
            return cleaned.includes("?")
              || /^(what|why|how|where|when|who|which)\\b/.test(cleaned)
              || /^(should i|can you|tell me|do i|is there|are there)\\b/.test(cleaned)
              || /^(i want to know|i'd like to know|i would like to know|i was wondering|i wonder|i need to know|help me understand)\\b/.test(cleaned)
              || cleaned.includes("what should i notice")
              || cleaned.includes("what do i need to do")
              || cleaned.includes("what should i visit")
              || cleaned.includes("where should i go")
              || cleaned.includes("was wondering if")
              || cleaned.includes("was wondering whether");
          }
          function cleanLocalText(text) {
            return text.trim()
              .replace(/\\bwhy do i need to do\\b/ig, "what do I need to do")
              .replace(/\\bwhy do i need to see\\b/ig, "what do I need to see")
              .replace(/\\bway mark\\b/ig, "Waymark")
              .replace(/\\bchicargo\\b/ig, "Chicago")
              .replace(/\\bnew orleans\\b/ig, "New Orleans");
          }
          function appBaseUrl() {
            try {
              const ref = document.referrer ? new URL(document.referrer) : new URL(window.top.location.href);
              return ref.origin + ref.pathname;
            } catch (error) {
              return "/";
            }
          }
          function submitVoice(action, automatic=false) {
            const text = transcript.value.trim();
            if (!text) {
              status.textContent = "Say something first.";
              return;
            }
            const corrected = cleanLocalText(text);
            transcript.value = corrected;
            const finalAction = action === "auto" ? (looksLikeQuestion(corrected) ? "ask" : "log") : action;
            const params = new URLSearchParams();
            params.set("voice_action", finalAction);
            params.set("voice_text", corrected);
            if (automatic) status.textContent = finalAction === "ask" ? "Question detected. Opening brief..." : "Saving private log...";
            const nextUrl = appBaseUrl() + "?" + params.toString();
            try {
              window.top.location.assign(nextUrl);
            } catch (error) {
              window.open(nextUrl, "_top");
            }
          }
          askWaymark.addEventListener("click", () => submitVoice("ask"));
          saveLog.addEventListener("click", () => submitVoice("log"));
          function resetSilenceTimer() {
            if (silenceTimer) window.clearTimeout(silenceTimer);
            if (!listening) return;
            silenceTimer = window.setTimeout(() => {
              if (listening && recognition) {
                status.textContent = "Silence detected. Processing...";
                recognition.stop();
              }
            }, 3000);
          }
          if (!SpeechRecognition) {
            status.textContent = "Speech recognition is not available here. Type into the box, then choose an action.";
            button.disabled = true;
            button.style.opacity = 0.55;
          } else {
            recognition = new SpeechRecognition();
            recognition.lang = "en-US";
            recognition.interimResults = true;
            recognition.continuous = true;
            recognition.onresult = event => {
              resetSilenceTimer();
              let finalText = "";
              let interimText = "";
              for (let i = 0; i < event.results.length; i++) {
                const chunk = event.results[i][0].transcript;
                if (event.results[i].isFinal) finalText += chunk + " ";
                else interimText += chunk;
              }
              transcript.value = (finalText + interimText).trim()
                .replace(/\\bwhy do i need to do\\b/ig, "what do I need to do")
                .replace(/\\bwhy do i need to see\\b/ig, "what do I need to see")
                .replace(/\\bway mark\\b/ig, "Waymark")
                .replace(/\\bchicargo\\b/ig, "Chicago")
                .replace(/\\bnew orleans\\b/ig, "New Orleans");
            };
            recognition.onerror = event => {
              if (silenceTimer) window.clearTimeout(silenceTimer);
              status.textContent = "Speech stopped: " + event.error + ". You can type into the box.";
              listening = false;
              button.innerHTML = '<span class="mic-icon">MIC</span> Start';
            };
            recognition.onend = () => {
              if (silenceTimer) window.clearTimeout(silenceTimer);
              listening = false;
              button.innerHTML = '<span class="mic-icon">MIC</span> Start';
              if (transcript.value.trim()) {
                status.textContent = "Transcript ready. Processing automatically...";
                if (!autoSubmitted) {
                  autoSubmitted = true;
                  window.setTimeout(() => submitVoice("auto", true), 1100);
                }
              }
            };
            button.addEventListener("click", () => {
              if (listening) {
                recognition.stop();
                return;
              }
              try {
                recognition.start();
                listening = true;
                button.textContent = "Stop";
                status.textContent = "Recording. Pause for 3 seconds to auto-stop, or tap Stop.";
                resetSilenceTimer();
              } catch (error) {
                status.textContent = "Speech recognition could not start. You can type into the box.";
              }
            });
          }
        </script>
        """,
        height=240,
    )


def render_voice_speaker(text: str, component_key: str = "voice_speaker") -> None:
    if not text:
        return
    speech_json = json.dumps(re.sub(r"\*\*", "", str(text)))
    components.html(
        f"""
        <script>
          const spoken = {speech_json};
          function speakWaymark() {{
            if (!spoken || !window.speechSynthesis) return;
            const utterance = new SpeechSynthesisUtterance(spoken);
            utterance.lang = "en-US";
            utterance.rate = 0.94;
            utterance.pitch = 1.0;
            const voices = window.speechSynthesis.getVoices();
            const nativeVoice = voices.find(v => v.lang === "en-US" && /Samantha|Alex|Google US English|Microsoft.*English/i.test(v.name))
              || voices.find(v => v.lang === "en-US")
              || voices.find(v => v.lang && v.lang.startsWith("en"));
            if (nativeVoice) utterance.voice = nativeVoice;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
          }}
          window.setTimeout(speakWaymark, 450);
        </script>
        """,
        height=0,
    )


def open_place_brief(destination: str, state: str = "", display_name: str = "") -> None:
    brief = generate_destination_brief(destination, state, "Map exploration", GUIDEBOOK_INTERESTS)
    if display_name:
        brief["display_name"] = display_name
    st.session_state.current_brief = brief
    st.session_state.page = "Ask About This Place"
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


def build_review_brief_candidates(mapped: pd.DataFrame) -> pd.DataFrame:
    if mapped.empty:
        return pd.DataFrame()
    rows = []
    seen = set()
    for row in mapped.itertuples():
        title = str(getattr(row, "location", "") or getattr(row, "title", "") or "").strip()
        if not title:
            continue
        key = (title.lower(), round(float(row.latitude), 3), round(float(row.longitude), 3))
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            {
                "source": "Review-backed place",
                "source_id": f"review-{getattr(row, 'source_id', len(rows))}",
                "title": title,
                "location": title,
                "state": "",
                "category": "review-backed brief",
                "latitude": float(row.latitude),
                "longitude": float(row.longitude),
                "summary": "This place has a saved review. Click to open a guidebook-style brief.",
                "color": [47, 111, 88],
            }
        )
    return pd.DataFrame(rows)


def build_state_zoom_points(states: list[str]) -> pd.DataFrame:
    rows = []
    for state in sorted(set(states)):
        if state in STATE_CENTERS:
            lat, lon = STATE_CENTERS[state]
            rows.append(
                {
                    "source": "State zoom",
                    "source_id": f"state-{state}",
                    "title": state,
                    "location": state,
                    "state": state,
                    "category": "state zoom",
                    "latitude": lat,
                    "longitude": lon,
                    "summary": "Click to zoom into this state.",
                    "color": [23, 33, 28, 55],
                }
            )
    return pd.DataFrame(rows)


def render_compact_map(points: pd.DataFrame, target_payload: dict | None = None, include_routes: bool = False) -> None:
    if points.empty and not include_routes:
        st.info("No mapped records yet.")
        return
    if target_payload and target_payload.get("latitude") and target_payload.get("longitude"):
        midpoint = [target_payload["longitude"], target_payload["latitude"]]
        zoom = 6.8
    elif not points.empty:
        midpoint = [points["longitude"].mean(), points["latitude"].mean()]
        zoom = 3.5
    else:
        midpoint = [PLACE_BRIEF_CANDIDATES["longitude"].mean(), PLACE_BRIEF_CANDIDATES["latitude"].mean()]
        zoom = 3.5
    layers = []
    if not points.empty:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=points,
                id="saved-brief-points" if include_routes else "memory-points",
                get_position="[longitude, latitude]",
                get_fill_color="color",
                get_radius=10000,
                pickable=True,
                auto_highlight=True,
                opacity=0.82,
            )
        )
    if include_routes:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=PLACE_BRIEF_CANDIDATES,
                id="brief-candidates",
                get_position="[longitude, latitude]",
                get_fill_color="color",
                get_radius=12500,
                pickable=True,
                auto_highlight=True,
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
                pickable=False,
            )
        )
    event = st.pydeck_chart(
        pdk.Deck(
            layers=layers,
            initial_view_state=pdk.ViewState(latitude=midpoint[1], longitude=midpoint[0], zoom=zoom),
            tooltip={
                "html": "<b>{title}</b><br/>{category}<br/>{summary}",
                "style": {"backgroundColor": "#17211c", "color": "white"},
            },
        ),
        use_container_width=True,
        on_select="rerun" if include_routes else "ignore",
        selection_mode="single-object",
        key="compact_brief_route_map" if include_routes else "compact_memory_map",
    )
    if include_routes:
        selected_objects = getattr(event.selection, "objects", {}) if event else {}
        clicked = None
        for layer_id in ("brief-candidates", "saved-brief-points"):
            objects = selected_objects.get(layer_id, [])
            if objects:
                clicked = objects[0]
                break
        if clicked:
            open_place_brief(
                str(clicked.get("title", "")),
                str(clicked.get("state", "")),
                str(clicked.get("location", "")),
            )
        st.caption("Zoom in and click a gold place marker to open its brief. Highway lines are route context; place markers are clickable.")


def answer_home_question(question: str) -> str:
    q = (question or "").lower()
    if not q.strip():
        return "Ask me what to notice in a place, where your memories cluster, or how to turn notes into a public-safe reflection."
    if any(phrase in q for phrase in ["what do i need to do", "what should i do", "what should i visit", "where should i go"]):
        return "I treated this as a place question and opened a field brief with food, teams, industries, politics, local context, and good places to start observing."
    if "public" in q or "publish" in q or "share" in q:
        return "Start private. When you are ready, use Export to create a public-safe draft that removes exact addresses, private names, raw transcripts, and real-time details before you manually share it elsewhere."
    if "map" in q or "where" in q:
        return "Use Memory Map. Field notes show what you noticed; Place Briefs show context you generated before or during a trip. The two stay separate so memory and research do not blur."
    if "notice" in q or "brief" in q or "place" in q:
        return "Use Ask About This Place. Enter a city, park, landmark, or small town, then generate a visual brief with prompts for what to notice."
    return "Capture the rough thought first. Waymark U.S. will attach place, theme, mood, and privacy status so scattered notes can become searchable memory later."


def brief_icon_svg(key: str) -> str:
    icons = {
        "historical_background": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4.5h10a3 3 0 0 1 3 3v12H8a3 3 0 0 0-3 0v-15z"></path><path d="M8 7h7M8 10h6"></path></svg>',
        "cultural_signals": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12s3.5-6 9-6 9 6 9 6-3.5 6-9 6-9-6-9-6z"></path><circle cx="12" cy="12" r="2.5"></circle></svg>',
        "local_food": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3v8M10 3v8M7 11h3v10"></path><path d="M16 3c2 2.4 2 6.5 0 9v9"></path></svg>',
        "questions_to_ask": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.5 9a3 3 0 1 1 4.7 2.5c-1.2.8-1.7 1.4-1.7 2.8"></path><path d="M12 18h.01"></path><circle cx="12" cy="12" r="9"></circle></svg>',
        "field_note_prompts": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h4l11-11a2.2 2.2 0 0 0-3-3L5 17l-1 3z"></path><path d="M14 7l3 3"></path></svg>',
        "safety_etiquette": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l7 3v5c0 5-3 8.5-7 10-4-1.5-7-5-7-10V6l7-3z"></path><path d="M9 12l2 2 4-5"></path></svg>',
        "population_snapshot": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 19V7l5-3 5 3v12"></path><path d="M14 19V9l6 3v7"></path><path d="M7 10h2M7 14h2M16 14h2"></path></svg>',
        "industry_snapshot": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 19h18"></path><path d="M5 19V9l4 3V9l4 3V7h5v12"></path><path d="M8 16h1M12 16h1M16 16h1"></path></svg>',
        "sports_snapshot": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8"></circle><path d="M7 8c3 2 7 2 10 0M7 16c3-2 7-2 10 0M12 4c-2 4-2 12 0 16M12 4c2 4 2 12 0 16"></path></svg>',
        "food_snapshot": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h16"></path><path d="M6 12c.5-4 3-7 6-7s5.5 3 6 7"></path><path d="M7 16h10l-1 4H8l-1-4z"></path></svg>',
        "politics_snapshot": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h16"></path><path d="M6 17V9l6-4 6 4v8"></path><path d="M9 17v-5h6v5"></path></svg>',
        "community_lens": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM16 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"></path><path d="M3.5 20c.7-3.5 2.4-5 4.5-5s3.8 1.5 4.5 5M11.5 20c.7-3.5 2.4-5 4.5-5s3.8 1.5 4.5 5"></path></svg>',
        "economy_lens": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 19h16"></path><path d="M6 19V9l4 3V9l4 3V7h4v12"></path></svg>',
        "nature_lens": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21V8"></path><path d="M12 8c-4 0-7 3-7 7 4 0 7-3 7-7z"></path><path d="M12 12c4 0 7-3 7-7-4 0-7 3-7 7z"></path></svg>',
        "music_lens": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18V5l10-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="16" cy="16" r="3"></circle></svg>',
        "agriculture_lens": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20c5-8 11-12 16-14"></path><path d="M7 16c-1-4 1-7 5-8 1 4-1 7-5 8z"></path><path d="M13 12c0-4 3-6 7-6 0 4-3 6-7 6z"></path></svg>',
    }
    return icons.get(key, '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8"></circle></svg>')


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
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    quick_left, quick_right = st.columns([0.9, 1.1])
    with quick_left:
        st.markdown(
            """
            <div class="quick-record-panel">
                <div>
                    <div class="atlas-choice-label">Voice-first capture</div>
                    <h3>Say the thought before it disappears.</h3>
                    <p>Use it while walking, driving, waiting at a station, eating, or noticing a street scene. Questions become spoken answers; ordinary thoughts become private logs.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with quick_right:
        render_browser_voice_helper("home_quick_record")
    if st.session_state.get("voice_result"):
        st.success(st.session_state.pop("voice_result"))
    if st.session_state.get("voice_answer"):
        st.info(st.session_state.pop("voice_answer"))
    if st.session_state.get("voice_spoken_answer"):
        render_voice_speaker(st.session_state.pop("voice_spoken_answer"), "home_voice_speaker")

    st.markdown('<div class="atlas-choice-label">Before or after?</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="journey-card before-card">
                <div class="journey-icon"><svg viewBox="0 0 24 24"><path d="M3 11l18-8-8 18-2-8-8-2z"></path></svg></div>
                <div class="atlas-choice-label">Before the trip</div>
                <h3>Read a place brief</h3>
                <p>Search a city, park, landmark, or corridor. Get a field brief with food, teams, politics, industries, and good places to start observing.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Learn About a Place", width="stretch"):
            go_to("Ask About This Place")
    with c2:
        st.markdown(
            """
            <div class="journey-card after-card">
                <div class="journey-icon"><svg viewBox="0 0 24 24"><path d="M12 3v18"></path><path d="M5 8h14"></path><path d="M7 21h10"></path><path d="M8 3h8"></path></svg></div>
                <div class="atlas-choice-label">After the moment</div>
                <h3>Save what happened</h3>
                <p>Record a voice note, paste a rough impression, or save a community encounter. Everything starts private.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Record a Thought", width="stretch"):
            go_to("Capture Note")

    st.markdown("### Ask or search")
    st.markdown(
        """
        <div class="voice-dock">
            <h3>Need an answer instead of a recording?</h3>
            <p>Ask what to notice, where to look on the map, or how to make a note public-safe.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
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
        st.markdown("**Voice note**")
        render_browser_voice_helper("capture_voice_helper")
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
        if not captured_text.strip():
            captured_text = "Quick private marker saved without a transcript yet."
        photo_path = save_upload(photo, "photos")
        audio_path = ""
        location = location_name or city or state
        category = classify_note_theme(captured_text, tags, mood)
        ai_summary = generate_public_ready_summary(captured_text, location, category)
        ai_context = generate_ai_context(captured_text, category, location)
        privacy_level = {
            "Private": "private",
            "Working note": "semi-private",
            "Public-ready draft": "public-ready",
        }[publishing_choice]
        generated_title = title.strip() or generate_note_title_from_text(captured_text)
        note_id = insert_field_note(
            {
                "title": generated_title,
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
            st.subheader(generated_title)
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

    visited_states = []
    visited_places = []
    route_mentions = set()
    if not notes.empty:
        if "state" in notes:
            visited_states.extend([str(x) for x in notes["state"].dropna().unique() if str(x).strip()])
        if "location_name" in notes:
            visited_places.extend([str(x) for x in notes["location_name"].dropna().unique() if str(x).strip()])
        note_blob = " ".join(
            str(value)
            for column in ["title", "location_name", "note_text", "tags", "ai_summary"]
            if column in notes
            for value in notes[column].dropna().tolist()
        )
        route_mentions.update(re.findall(r"\b(?:I[-\s]?\d{1,3}|Interstate\s+\d{1,3}|US[-\s]?\d{1,3}|Route\s+\d{1,3})\b", note_blob, flags=re.IGNORECASE))
    if not briefs.empty:
        visited_places.extend([str(x) for x in briefs["destination"].dropna().unique() if str(x).strip()])

    st.markdown("### Waymark Progress")
    prog_a, prog_b, prog_c = st.columns(3)
    prog_a.metric("Places marked", len(set(visited_places)))
    prog_b.metric("States touched", len(set(visited_states)))
    prog_c.metric("Road corridors noted", len(route_mentions))
    if visited_places:
        chips = "".join(f"<span>{html.escape(place)}</span>" for place in sorted(set(visited_places))[:14])
        st.markdown(f'<div class="map-legend">{chips}</div>', unsafe_allow_html=True)
    if route_mentions:
        route_chips = "".join(f"<span>{html.escape(route.upper().replace('INTERSTATE ', 'I-'))}</span>" for route in sorted(route_mentions)[:12])
        st.markdown(f'<div class="map-legend">{route_chips}</div>', unsafe_allow_html=True)

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
        review_candidates = build_review_brief_candidates(mapped)
        render_brief_map(visible_briefs, map_place_payload, map_place_label, review_candidates)


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
                    "Field note" if selected_row["source"] == "Field note" else "Farmstay note",
                    int(selected_row["source_id"]),
                )
                st.session_state.page = "Export"
                st.rerun()
            if c2.button("Export This Record", key=f"map_export_{selected_record}"):
                source_type = "Field note" if selected_row["source"] == "Field note" else "Farmstay note"
                st.session_state.export_selection = [f"{source_type}:{selected_row['source_id']}"]
                st.session_state.page = "Export"
                st.rerun()

    if not needs_location.empty:
        st.subheader("Needs Location Data")
        st.dataframe(needs_location[["source", "title", "location", "category"]], width="stretch")


def render_brief_map(
    visible: pd.DataFrame,
    map_place_payload: dict | None,
    map_place_label: str,
    review_candidates: pd.DataFrame | None = None,
) -> None:
    candidate_points = pd.concat(
        [PLACE_BRIEF_CANDIDATES.copy(), review_candidates if review_candidates is not None else pd.DataFrame()],
        ignore_index=True,
        sort=False,
    )
    state_points = build_state_zoom_points([str(x) for x in candidate_points.get("state", pd.Series(dtype=str)).dropna() if str(x)])
    if map_place_label:
        query = map_place_label.lower()
        filtered_candidates = candidate_points[
            candidate_points[["title", "location", "category"]]
            .fillna("")
            .astype(str)
            .agg(" ".join, axis=1)
            .str.lower()
            .str.contains(query, na=False)
        ]
        if not filtered_candidates.empty:
            candidate_points = filtered_candidates
    if map_place_payload and map_place_payload.get("latitude") and map_place_payload.get("longitude"):
        midpoint = [map_place_payload["longitude"], map_place_payload["latitude"]]
        zoom = 8.4
    elif st.session_state.get("map_focus_state") in STATE_CENTERS:
        lat, lon = STATE_CENTERS[st.session_state["map_focus_state"]]
        midpoint = [lon, lat]
        zoom = 5.7
    elif not visible.empty:
        midpoint = [visible["longitude"].mean(), visible["latitude"].mean()]
        zoom = 4.2
    else:
        midpoint = [candidate_points["longitude"].mean(), candidate_points["latitude"].mean()]
        zoom = 3.5
    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=state_points,
            id="state-zoom-points",
            get_position="[longitude, latitude]",
            get_fill_color="color",
            get_radius=70000,
            pickable=True,
            auto_highlight=True,
            opacity=0.24,
        ),
        pdk.Layer(
            "ScatterplotLayer",
            data=candidate_points,
            id="brief-candidates",
            get_position="[longitude, latitude]",
            get_fill_color="color",
            get_radius=12500,
            pickable=True,
            auto_highlight=True,
            opacity=0.58,
        )
    ]
    if not visible.empty:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=visible,
                id="saved-brief-points",
                get_position="[longitude, latitude]",
                get_fill_color="color",
                get_radius=15000,
                pickable=True,
                auto_highlight=True,
                opacity=0.92,
            )
        )
    layers.append(
        pdk.Layer(
            "PathLayer",
            data=INTERSTATE_ROUTES,
            get_path="path",
            get_color=[183, 150, 93, 110],
            width_min_pixels=2,
            pickable=False,
        )
    )
    event = st.pydeck_chart(
        pdk.Deck(
            layers=layers,
            initial_view_state=pdk.ViewState(latitude=midpoint[1], longitude=midpoint[0], zoom=zoom),
            tooltip={
                "html": "<b>{title}</b><br/>{location}<br/>{category}<br/><br/>{summary}",
                "style": {"backgroundColor": "#3a2c19", "color": "white"},
            },
        ),
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-object",
        key="memory_brief_click_map",
    )
    selected_objects = getattr(event.selection, "objects", {}) if event else {}
    clicked = None
    for layer_id in ("state-zoom-points", "brief-candidates", "saved-brief-points"):
        objects = selected_objects.get(layer_id, [])
        if objects:
            clicked = objects[0]
            break
    if clicked:
        if str(clicked.get("category", "")) == "state zoom":
            st.session_state.map_focus_state = str(clicked.get("state") or clicked.get("title") or "")
            st.rerun()
        else:
            open_place_brief(
                str(clicked.get("title", "")),
                str(clicked.get("state", "")),
                str(clicked.get("location", "")),
            )
    st.caption("Gold markers open place briefs. Green markers are places with reviews. Large soft state markers zoom into that state.")
    if visible.empty:
        st.info("No saved briefs match yet. Click a suggested city or park on the map to generate one.")
        return
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
        if st.button("Open This Brief", key=f"open_saved_brief_{selected_brief}"):
            open_place_brief(str(selected_row["title"]), "", str(selected_row["location"]))


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
    if st.session_state.get("voice_result"):
        st.success(st.session_state.pop("voice_result"))
    if st.session_state.get("voice_answer"):
        st.info(st.session_state.pop("voice_answer"))
    if st.session_state.get("voice_spoken_answer"):
        render_voice_speaker(st.session_state.pop("voice_spoken_answer"), "brief_voice_speaker")

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
    st.markdown(
        '<div class="atlas-card"><strong>Field brief mode</strong><br><span class="small-muted">Waymark now covers the full place brief by default: population, industries, sports, food, politics, history, community, nature, routes, and good places to start observing.</span></div>',
        unsafe_allow_html=True,
    )
    interests = GUIDEBOOK_INTERESTS
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
            for key in [
                "brief_15_sec",
                "population_snapshot",
                "industry_snapshot",
                "sports_snapshot",
                "food_snapshot",
                "politics_snapshot",
                "historical_background",
                "questions_to_ask",
            ]
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
            ("population_snapshot", "Population"),
            ("industry_snapshot", "Industries"),
            ("sports_snapshot", "Sports"),
            ("food_snapshot", "Food"),
            ("historical_background", "Historical Background"),
            ("cultural_signals", "Cultural Signals"),
        ]
        if brief.get("community_lens"):
            section_labels.append(("community_lens", "Community Lens"))
        if brief.get("economy_lens"):
            section_labels.append(("economy_lens", "Economy Lens"))
        if brief.get("agriculture_lens"):
            section_labels.append(("agriculture_lens", "Agriculture Lens"))
        if brief.get("nature_lens"):
            section_labels.append(("nature_lens", "Nature Lens"))
        if brief.get("music_lens"):
            section_labels.append(("music_lens", "Music Lens"))
        if brief.get("politics_snapshot"):
            section_labels.append(("politics_snapshot", "Politics"))
        section_labels.extend(
            [
                ("questions_to_ask", "Questions To Ask"),
                ("field_note_prompts", "Field Note Prompts"),
            ]
        )
        if brief.get("must_visit"):
            st.markdown("### Good Places To Start Observing")
            spot_cols = st.columns(min(2, len(brief["must_visit"])))
            for col, spot in zip(spot_cols, brief["must_visit"]):
                with col:
                    spot_name = html.escape(str(spot.get("name", "Place to visit")))
                    spot_why = guide_text_html(str(spot.get("why", "")))
                    spot_image = html.escape(str(spot.get("image_url", HERO_IMAGE_URL)))
                    st.markdown(
                        f"""
                        <div class="field-anchor-card">
                            <img src="{spot_image}" alt="{spot_name}">
                            <div>
                                <h4>{spot_name}</h4>
                                <p>{spot_why}</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        for row_start in range(0, len(section_labels), 2):
            cols = st.columns(2)
            for col, (key, label) in zip(cols, section_labels[row_start : row_start + 2]):
                with col:
                    icon = brief_icon_svg(key)
                    st.markdown(
                        f"""
                        <div class="brief-section">
                            <div class="brief-icon">{icon}</div>
                            <h4>{html.escape(label)}</h4>
                            <p>{guide_text_html(str(brief.get(key, "")))}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        with st.container(border=True):
            st.markdown("**Local institutions**")
            st.markdown(guide_text_html(brief["local_institutions"]), unsafe_allow_html=True)
        if brief.get("safety_etiquette"):
            st.caption(f"Privacy and courtesy note: {brief['safety_etiquette']}")
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
    location_text = st.text_input("Place or town", placeholder="Asheville market, rural Kentucky, neighborhood diner...")
    moment_type = st.selectbox(
        "What kind of community moment was it?",
        [
            "Local conversation",
            "Farmstay",
            "Shared meal or hospitality",
            "Market or small business visit",
            "Community event",
            "Religious or civic gathering",
            "Volunteer or work exchange",
            "Homestay",
            "Other",
        ],
    )

    with st.form("farmstay_form"):
        farm_name = st.text_input("Optional title", placeholder="Market conversation, dinner with hosts, town meeting...")
        reflection = st.text_area("What happened?", height=220, placeholder="Write it messily. Who was there, what was said, what surprised you, what should stay private?")
        people_met = st.text_input("Private people note", placeholder="Optional. Roles are safer than names.")
        community_feeling = st.slider("How strong did the community feeling seem?", 1, 5, 3)
        submitted = st.form_submit_button("Save Community Log")

    if submitted:
        selected_location_payload = geocode_destination(location_text) if location_text else {}
        work_done = reflection
        food_eaten = ""
        conversation_topics = reflection
        lifestyle_observations = reflection
        surprises = ""
        labor_intensity = 3
        payload = {
            "date": date.today().isoformat(),
            "farm_name": farm_name,
            "location_name": location_text,
            "latitude": selected_location_payload.get("latitude"),
            "longitude": selected_location_payload.get("longitude"),
            "farm_type": moment_type.lower(),
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
        st.success(f"Saved private farmstay note #{log_id}.")
        with st.container(border=True):
            st.subheader(farm_name or "Farmstay note")
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
    if not text and str(item.get("source_type")) == "Farmstay note":
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
    public_only = False
    st.title("Search Notes")
    st.caption(
        "Find private field notes, place questions, farmstay memories, and draft reflections by place, theme, tag, or keyword."
    )
    items = fetch_all_library_items()
    if items.empty:
        st.info("No notes yet.")
        return
    if public_only:
        items = items[items["privacy_level"].fillna("").astype(str) == "public-ready"]
        if items.empty:
            st.info("No public-ready reviews yet. Mark a personal log public-ready when you want it to appear here.")
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
                st.session_state.page = "Export"
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
        if source_type == "Farmstay note":
            farms = fetch_farmstay_logs()
            match = farms[farms["id"] == source_id]
            record = match.iloc[0].to_dict() if not match.empty else None
        if record:
            for label, value in record.items():
                if value not in (None, ""):
                    st.markdown(f"**{label.replace('_', ' ').title()}**")
                    st.write(value)


def personal_log_page() -> None:
    st.title("Personal Log")
    st.caption("Private voice notes and rough thoughts live here first. You can keep them private or prepare selected notes as public-safe draft candidates.")
    if st.session_state.get("voice_result"):
        st.success(st.session_state.pop("voice_result"))
    if st.session_state.get("voice_spoken_answer"):
        render_voice_speaker(st.session_state.pop("voice_spoken_answer"), "personal_log_voice_speaker")

    notes = fetch_field_notes()
    if notes.empty:
        st.info("No personal logs yet. Use the mic on Home or Capture Note.")
        return
    logs = notes[
        notes[["tags", "audio_transcript", "note_text"]]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .str.lower()
        .str.contains("voice|quick private marker", regex=True)
    ].copy()
    if logs.empty:
        logs = notes.copy()
    logs = logs.sort_values("created_at", ascending=False)

    privacy_filter = st.segmented_control(
        "Show",
        ["All", "Private", "Public-ready"],
        default="All",
        key="personal_log_privacy_filter",
    )
    if privacy_filter == "Private":
        logs = logs[logs["privacy_level"].fillna("private").astype(str) == "private"]
    elif privacy_filter == "Public-ready":
        logs = logs[logs["privacy_level"].fillna("").astype(str) == "public-ready"]

    for _, note in logs.head(30).iterrows():
        privacy = str(note.get("privacy_level") or "private")
        raw_text = str(note.get("audio_transcript") or "")
        clean_text = str(note.get("note_text") or "")
        body = clean_text if len(clean_text) < 340 else f"{clean_text[:340]}..."
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="memory-mode-card">
                    <div class="atlas-choice-label">{html.escape(privacy)}</div>
                    <h3>{html.escape(str(note.get("title") or "Untitled voice log"))}</h3>
                    <p>{html.escape(body)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            meta = " | ".join(
                part
                for part in [
                    str(note.get("date") or ""),
                    str(note.get("location_name") or note.get("city") or ""),
                    str(note.get("category") or ""),
                ]
                if part
            )
            if meta:
                st.caption(meta)
            if note.get("ai_summary"):
                st.markdown("**AI summary**")
                st.write(note.get("ai_summary"))
            if raw_text and raw_text != clean_text:
                with st.expander("Raw transcript"):
                    st.write(raw_text)
            c1, c2, c3 = st.columns(3)
            note_id = int(note["id"])
            if privacy != "public-ready":
                if c1.button("Mark public-ready", key=f"make_public_{note_id}"):
                    update_field_note_privacy_local(note_id, "public-ready")
                    st.success("Marked as a public-safe draft candidate.")
                    st.rerun()
            else:
                if c1.button("Make private", key=f"make_private_{note_id}"):
                    update_field_note_privacy_local(note_id, "private")
                    st.success("Moved back to private.")
                    st.rerun()
            if c2.button("Create public version", key=f"log_public_version_{note_id}"):
                st.session_state.selected_public = ("Field note", note_id)
                st.session_state.page = "Export"
                st.rerun()
            if c3.button("Export", key=f"log_export_{note_id}"):
                st.session_state.export_selection = [f"Field note:{note_id}"]
                st.session_state.page = "Export"
                st.rerun()


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
    st.title("Create Public-Safe Draft")
    st.warning("Public versions are drafts. Please manually review before publishing.")
    st.markdown(
        """
        Select a note, generate an anonymous public version, then review what was removed.
        Exact place, exact date, raw transcript, names, affiliations, and real-time movement stay private by default.
        """
    )

    if st.session_state.get("selected_public") and st.session_state.selected_public[0] == "Farmstay note":
        log = get_farmstay_log(int(st.session_state.selected_public[1]))
        if log:
            st.subheader("Farmstay public-safe draft")
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


FIELDWORK_TYPES = [
    "Question",
    "Observation",
    "Conversation",
    "Food",
    "Farmstay",
    "Local institution",
    "Economic signal",
    "Cultural signal",
    "Reflection",
    "Road scene",
    "Other",
]


FIELDWORK_FILTERS = [
    "All",
    "Questions",
    "Observations",
    "Food",
    "Farmstay",
    "Conversations",
    "Local institutions",
    "Economic signals",
    "Cultural signals",
    "Reflections",
    "Place Briefs",
    "Export-ready",
]


def fieldwork_slug(label: str) -> str:
    return (label or "Other").strip().lower().replace(" ", "_")


def privacy_copy() -> None:
    st.info("Nothing is published from Waymark. Public-safe drafts are only copyable drafts for manual review.")


def infer_location_from_place(place: str) -> dict:
    if not place:
        return {}
    parts = [part.strip() for part in place.split(",")]
    destination = parts[0] if parts else place
    state = parts[1] if len(parts) > 1 else ""
    return geocode_destination(destination, state)


def make_private_summary(text: str, note_type: str, place: str = "") -> str:
    cleaned = clean_voice_text(text)
    seed = cleaned[:260] if cleaned else "No raw note text was provided."
    label = note_type.lower()
    place_text = f" in {place}" if place else ""
    if label == "question":
        return f"You asked a place question{place_text}: {seed} Treat this as something for Ask/Understand, not as a public reflection by default."
    if label == "conversation":
        return f"Conversation note{place_text}: {seed} Remove names and identifying details before any export."
    if label == "food":
        return f"Food field note{place_text}: {seed} Useful for reading local institutions, migration, work rhythms, and everyday culture."
    if label == "farmstay":
        return f"Farmstay note{place_text}: {seed} Exact farm location, host names, and private routines should stay sensitive."
    if label in {"economic signal", "local institution", "cultural signal"}:
        return f"{note_type} note{place_text}: {seed} This may help compare how places organize daily life."
    return f"{note_type} note{place_text}: {seed}"


def ask_waymark_response(place: str, observation: str, lens: str) -> dict[str, object]:
    place_label = place or "this place"
    lens_label = lens or "general"
    obs = clean_voice_text(observation)
    tags = [fieldwork_slug(lens_label), "question", "field_prompt"]
    return {
        "possible_explanations": [
            f"One possible lens is **{lens_label}**: the scene may reflect older institutions, current economics, local identity, or who uses public space at different times of day.",
            f"In **{place_label}**, avoid treating one scene as proof. Use it as a clue and compare it with streets, signs, food places, churches, schools, employers, and local media.",
            f"The observation may reveal a gap between visitor-facing imagery and everyday routines. Check what feels designed for outsiders versus what locals actually use.",
        ],
        "what_to_notice_next": [
            "Which institutions repeat: churches, schools, hospitals, courthouses, universities, farm supply stores, warehouses, stadiums, diners?",
            "Who is present at different times of day, and who seems absent?",
            "Which signs, team logos, menus, storefronts, or road patterns keep showing up?",
        ],
        "questions_to_ask": [
            "What has changed here in the last ten years?",
            "Which place would locals send a visitor to if they wanted to understand the town?",
            "What do outsiders usually misunderstand about this place?",
        ],
        "tags": tags,
        "followups": [
            f"What would a {lens_label} reading of this scene miss?",
            f"How does {place_label} compare with the last place I visited?",
            "What should I notice next if I only have 30 minutes here?",
        ],
        "summary": f"Question about {place_label}: {obs[:180]}",
    }


def save_question_record(place: str, question: str, response: dict[str, object], lens: str) -> int:
    geo = infer_location_from_place(place)
    title = generate_note_title_from_text(question, "Question about a place")
    return insert_field_note(
        {
            "title": title,
            "date": datetime.now().isoformat(timespec="minutes"),
            "location_name": place,
            "address": "",
            "latitude": geo.get("latitude"),
            "longitude": geo.get("longitude"),
            "city": geo.get("city", ""),
            "state": geo.get("state", ""),
            "category": "question",
            "note_text": question,
            "audio_transcript": "",
            "mood": "curious",
            "ai_summary": str(response.get("summary", "")),
            "ai_context": json.dumps(response, ensure_ascii=False),
            "tags": ", ".join(response.get("tags", [fieldwork_slug(lens), "question"])),
            "privacy_level": "private",
        }
    )


def get_private_records() -> pd.DataFrame:
    notes = fetch_field_notes()
    if notes.empty:
        return pd.DataFrame()
    records = notes.copy()
    records["record_kind"] = records["category"].fillna("field_note").astype(str).str.lower()
    records["cleaned_title"] = records["title"].fillna("").replace("", "Untitled field note")
    records["private_summary"] = records["ai_summary"].fillna("")
    records["visibility"] = records["privacy_level"].fillna("private").replace({"public-ready": "Public-safe draft candidate", "semi-private": "Private", "private": "Private"})
    return records


def filter_records(records: pd.DataFrame, selected_filter: str) -> pd.DataFrame:
    if records.empty or selected_filter == "All":
        return records
    category_map = {
        "Questions": ["question"],
        "Observations": ["observation", "road scene", "road_scene", "travel"],
        "Food": ["food"],
        "Farmstay": ["farmstay", "farm"],
        "Conversations": ["conversation", "people"],
        "Local institutions": ["local institution", "local_institution"],
        "Economic signals": ["economic signal", "economic_signal", "economy"],
        "Cultural signals": ["cultural signal", "cultural_signal", "culture"],
        "Reflections": ["reflection", "personal reflection", "personal_reflection"],
        "Export-ready": ["public-ready"],
    }
    if selected_filter == "Export-ready":
        return records[records["privacy_level"].fillna("").astype(str).isin(category_map[selected_filter])]
    values = category_map.get(selected_filter, [])
    return records[records["record_kind"].isin(values)]


def get_place_brief_records() -> pd.DataFrame:
    briefs = fetch_saved_briefs()
    if briefs.empty:
        return pd.DataFrame()
    rows = []
    for brief in briefs.itertuples():
        geo = geocode_destination(str(brief.destination or ""), str(brief.state or ""))
        rows.append(
            {
                "id": f"brief-{brief.id}",
                "record_kind": "place_brief",
                "cleaned_title": f"{brief.destination}, {brief.state}".strip(", "),
                "location_name": ", ".join(part for part in [brief.destination, brief.state] if part),
                "date": getattr(brief, "generated_at", ""),
                "private_summary": getattr(brief, "brief_15_sec", ""),
                "tags": "place_brief, understand",
                "latitude": geo.get("latitude"),
                "longitude": geo.get("longitude"),
                "city": geo.get("city", ""),
                "state": geo.get("state", getattr(brief, "state", "")),
                "visibility": "Private",
                "source_id": getattr(brief, "id", ""),
            }
        )
    return pd.DataFrame(rows)


def render_sidebar(pages: list[str]) -> str:
    nav_labels = {
        "Home": "Home",
        "Understand": "Understand",
        "Ask": "Ask",
        "Capture": "Capture",
        "Memory Map": "Memory Map",
        "Synthesize": "Synthesize",
        "Library": "Library",
        "Export": "Export",
    }
    st.sidebar.title(APP_NAME)
    st.sidebar.markdown(
        '<div class="sidebar-tagline">Private AI field journal. Understand what you see. Remember what you notice.</div>',
        unsafe_allow_html=True,
    )
    for page in pages:
        label = nav_labels.get(page, page)
        if page == st.session_state.page:
            st.sidebar.markdown(f'<div class="nav-active">{label}</div>', unsafe_allow_html=True)
        elif st.sidebar.button(label, key=f"mvp_side_nav_{page}"):
            st.session_state.page = page
            st.rerun()
    return st.session_state.page


def render_top_nav(pages: list[str]) -> None:
    with st.expander("Navigate Waymark U.S.", expanded=False):
        cols = st.columns(4)
        for idx, page in enumerate(pages):
            with cols[idx % 4]:
                if page == st.session_state.page:
                    st.markdown(f'<div class="top-nav-active">{html.escape(page)}</div>', unsafe_allow_html=True)
                elif st.button(page, key=f"mvp_top_nav_{page}", width="stretch"):
                    st.session_state.page = page
                    st.rerun()


def home_page() -> None:
    st.markdown(
        f"""
        <div class="atlas-hero">
            <div>
                <div class="atlas-kicker">A private AI field journal</div>
                <h1>Waymark U.S.</h1>
                <h3>Understand what you see.<br>Remember what you notice.</h3>
                <p>Waymark is a private AI field journal for curious travelers. It helps you read a place before you arrive, ask better questions while you're there, and turn rough road notes into maps, comparisons, essays, and reflections after the trip.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    cards = [
        ("Understand a Place", "Get a short “How to read this place” brief before you arrive.", "Generate Place Brief", "Understand"),
        ("Ask About What I’m Seeing", "Turn a confusing or interesting scene into a better question.", "Ask Waymark", "Ask"),
        ("Capture a Field Note", "Say the thought before it disappears.", "Capture Note", "Capture"),
    ]
    for col, (title, body, button, page) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="journey-card">
                    <div class="atlas-choice-label">Fieldwork</div>
                    <h3>{html.escape(title)}</h3>
                    <p>{html.escape(body)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(button, key=f"home_card_{page}", width="stretch"):
                go_to(page)
    st.markdown(
        """
        <div class="atlas-panel">
            <h3>Synthesize My Journey</h3>
            <p class="small-muted">Compare places, find recurring themes, and turn observations into essays or scripts.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Synthesize Notes", width="stretch"):
        go_to("Synthesize")
    st.markdown(
        """
        <div class="atlas-panel">
            <h3>Not an audio tour. Not a trip planner. Not just a travel diary.</h3>
            <p class="small-muted">Audio tour apps tell you stories about places. Trip planners tell you where to go. Photo journals show where you went. Waymark helps you notice, ask, compare, and remember.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    privacy_copy()


def ai_companion_page() -> None:
    st.title("Understand a Place")
    st.caption('Get oriented before you arrive. Waymark gives you a compact “How to read this place” brief — not a tourist checklist.')
    destination = st.text_input("Destination", placeholder="Boston, MA or Nashville, TN", key="understand_destination")
    state = st.text_input("State / region (optional)", placeholder="MA, Tennessee, Appalachia", key="understand_state")
    lens = st.selectbox(
        "What lens do you want?",
        [
            "General orientation",
            "Local history",
            "Food and local institutions",
            "Farm / rural life",
            "Race and community",
            "Economy and industries",
            "Religion and civic life",
            "Sports and local identity",
            "Nature and landscape",
            "Small-town life",
        ],
    )
    question = st.text_input("Optional question", placeholder="What should I notice here? Why does this town feel this way?")
    if st.button('Generate “How to Read This Place” Brief', width="stretch"):
        if not destination.strip():
            st.error("We could not lock this destination. Please type the city and state manually.")
        else:
            brief = generate_destination_brief(destination, state, lens, GUIDEBOOK_INTERESTS)
            if question:
                brief["field_note_prompts"] = f"**Your question:** {question} " + str(brief.get("field_note_prompts", ""))
            st.session_state.current_brief = brief

    brief = st.session_state.get("current_brief")
    if not brief:
        return
    title = ", ".join(part for part in [brief.get("destination"), brief.get("state")] if part)
    st.markdown(f"## {title} in 15 seconds")
    st.markdown(guide_text_html(brief.get("brief_15_sec", "")), unsafe_allow_html=True)
    sections = [
        ("How to read this place", "cultural_signals"),
        ("What to notice", "field_note_prompts"),
        ("Local signals", "community_lens"),
        ("Food and institutions", "local_food"),
        ("Economy / industries", "industry_snapshot"),
        ("History underneath the surface", "historical_background"),
        ("Questions to ask locals", "questions_to_ask"),
    ]
    if brief.get("sports_snapshot"):
        sections.insert(5, ("Sports and local identity", "sports_snapshot"))
    for label, key in sections:
        with st.container(border=True):
            st.markdown(f"### {label}")
            st.markdown(guide_text_html(brief.get(key, "")), unsafe_allow_html=True)
    if brief.get("must_visit"):
        st.markdown("### Good places to start observing")
        cols = st.columns(min(2, len(brief["must_visit"])))
        for col, spot in zip(cols, brief["must_visit"]):
            with col:
                st.markdown(f"**{spot.get('name', 'Field anchor')}**")
                st.write(spot.get("why", "A useful starting point for observing the place."))
    c1, c2 = st.columns(2)
    if c1.button("Save Private Place Brief", width="stretch"):
        insert_ai_brief(brief)
        st.success("Saved as a private place brief. It will appear in Memory Map and Library.")
    if c2.button("Read Aloud", width="stretch"):
        render_voice_speaker(f"{title}. {brief.get('brief_15_sec', '')}", "brief_read_aloud")


def ask_page() -> None:
    st.title("Ask About What I’m Seeing")
    st.caption("Turn a confusing or interesting scene into better questions. Waymark answers with possible lenses, not definitive claims.")
    place = st.text_input("Current place / destination", value=st.session_state.pop("ask_place_prefill", ""), placeholder="Chicago, IL")
    seeing = st.text_area("What are you seeing?", value=st.session_state.pop("ask_prefill", ""), height=170, placeholder="I’m seeing a lot of churches and empty storefronts. What might explain that?")
    lens = st.selectbox("Optional lens", ["history", "economy", "religion", "race/community", "food", "agriculture", "sports", "urban design", "other"])
    if st.button("Ask Waymark", width="stretch"):
        if not seeing.strip():
            st.error("Type or dictate what you are seeing first.")
            return
        response = ask_waymark_response(place, seeing, lens)
        st.session_state.ask_response = {"place": place, "seeing": seeing, "lens": lens, "response": response}

    payload = st.session_state.get("ask_response")
    if payload:
        response = payload["response"]
        for label, key in [
            ("Possible explanations", "possible_explanations"),
            ("What to notice next", "what_to_notice_next"),
            ("Questions to ask locals", "questions_to_ask"),
            ("Suggested follow-up questions", "followups"),
        ]:
            with st.container(border=True):
                st.markdown(f"### {label}")
                for item in response[key]:
                    st.markdown(f"- {guide_text_html(item)}", unsafe_allow_html=True)
        st.caption("Related tags: " + ", ".join(response["tags"]))
        if st.button("Save as Question", width="stretch"):
            note_id = save_question_record(payload["place"], payload["seeing"], response, payload["lens"])
            st.success(f"Saved question #{note_id} to Library and Memory Map.")


def add_field_note_page() -> None:
    st.title("Capture a Field Note")
    st.caption("Say the thought before it disappears. Capture a question, observation, conversation, food memory, farmstay moment, or reflection. Everything is private by default.")
    render_browser_voice_helper("capture_voice_mvp")
    st.divider()
    place = st.text_input("Location / Place", placeholder="Chicago, IL or Blue Ridge foothills")
    title = st.text_input("Optional title")
    raw_note = st.text_area("Raw note", height=180, placeholder="Write or paste the field note here.")
    note_type = st.selectbox("Note type", FIELDWORK_TYPES, index=1)
    visibility = st.selectbox("Visibility", ["Private", "Public-safe draft candidate"], index=0)
    extra = {}
    if note_type == "Farmstay":
        c1, c2 = st.columns(2)
        extra["farm_type"] = c1.text_input("Farm type")
        extra["work_done"] = c2.text_input("Work done")
        extra["food_eaten"] = st.text_input("Food eaten")
        extra["people_met"] = st.text_input("People met")
        extra["surprises"] = st.text_input("What surprised me")
        extra["rural_life"] = st.text_area("What this reveals about rural life", height=100)
    if st.button("Save as Field Note", width="stretch"):
        text_parts = [raw_note, *[value for value in extra.values() if value]]
        full_text = "\n".join(part for part in text_parts if part).strip()
        if not full_text:
            st.error("Add a note or transcript first.")
            return
        geo = infer_location_from_place(place)
        cleaned_title = title.strip() or generate_note_title_from_text(full_text, "Untitled field note")
        summary = make_private_summary(full_text, note_type, place)
        note_id = insert_field_note(
            {
                "title": cleaned_title,
                "date": datetime.now().isoformat(timespec="minutes"),
                "location_name": place,
                "latitude": geo.get("latitude"),
                "longitude": geo.get("longitude"),
                "city": geo.get("city", ""),
                "state": geo.get("state", ""),
                "category": fieldwork_slug(note_type),
                "note_text": clean_voice_text(full_text),
                "audio_transcript": raw_note,
                "mood": "curious",
                "ai_summary": summary,
                "ai_context": "User original words are stored separately from this private summary.",
                "tags": fieldwork_slug(note_type),
                "privacy_level": "public-ready" if visibility == "Public-safe draft candidate" else "private",
            }
        )
        st.success(f"Saved private field note #{note_id}.")
    privacy_copy()


def map_view_page() -> None:
    st.title("Memory Map")
    st.caption("Map what you noticed, not just where you went. Your map collects questions, observations, conversations, food signals, farmstay notes, and reflections.")
    records = get_private_records()
    briefs = get_place_brief_records()
    selected = st.selectbox("Filter", FIELDWORK_FILTERS, index=0)
    visible_records = filter_records(records, selected)
    if selected == "Place Briefs":
        visible_records = pd.DataFrame()
    layers = []
    needs_location = []
    point_rows = []
    if not visible_records.empty:
        for row in visible_records.itertuples():
            lat = pd.to_numeric(getattr(row, "latitude", None), errors="coerce")
            lon = pd.to_numeric(getattr(row, "longitude", None), errors="coerce")
            if pd.isna(lat) or pd.isna(lon):
                needs_location.append({"title": row.cleaned_title, "location": getattr(row, "location_name", ""), "type": row.record_kind})
                continue
            point_rows.append({"title": row.cleaned_title, "location": getattr(row, "location_name", ""), "record_type": row.record_kind, "summary": str(getattr(row, "private_summary", ""))[:120], "latitude": lat, "longitude": lon, "color": [47, 111, 88]})
    if selected in {"All", "Place Briefs"} and not briefs.empty:
        for row in briefs.itertuples():
            if pd.notna(row.latitude) and pd.notna(row.longitude):
                point_rows.append({"title": row.cleaned_title, "location": row.location_name, "record_type": "place_brief", "summary": str(row.private_summary)[:120], "latitude": row.latitude, "longitude": row.longitude, "color": [183, 150, 93]})
            else:
                needs_location.append({"title": row.cleaned_title, "location": row.location_name, "type": "place_brief"})
    points = pd.DataFrame(point_rows)
    if points.empty:
        st.info("No mapped private records yet. Notes without coordinates appear below.")
    else:
        midpoint = [points["longitude"].mean(), points["latitude"].mean()]
        st.pydeck_chart(
            pdk.Deck(
                layers=[pdk.Layer("ScatterplotLayer", data=points, get_position="[longitude, latitude]", get_fill_color="color", get_radius=10000, pickable=True, opacity=0.84)],
                initial_view_state=pdk.ViewState(latitude=midpoint[1], longitude=midpoint[0], zoom=4.2),
                tooltip={"html": "<b>{title}</b><br/>{record_type}<br/>{location}<br/>{summary}<br/><em>Open in Library</em>", "style": {"backgroundColor": "#17211c", "color": "white"}},
            ),
            use_container_width=True,
        )
    if needs_location:
        st.subheader("Needs location")
        st.dataframe(pd.DataFrame(needs_location), width="stretch")


def journey_review_page() -> None:
    st.title("Synthesize My Journey")
    st.caption("Turn scattered road notes into patterns.")
    records = get_private_records()
    if records.empty:
        st.info("Capture notes first, then synthesize patterns here.")
        return
    synthesis_type = st.selectbox("Synthesis type", ["Recurring themes", "Compare places", "What surprised me", "Questions I kept asking", "What I learned about America", "Essay outline", "Podcast outline", "Field report"])
    places = sorted({str(value) for value in records["location_name"].dropna() if str(value)})
    selected_places = st.multiselect("Places to compare", places, default=places[:3])
    filtered = records[records["location_name"].isin(selected_places)] if selected_places else records
    if st.button("Generate Synthesis", width="stretch"):
        themes = filtered["record_kind"].value_counts().head(6)
        strongest = filtered["note_text"].fillna("").astype(str).head(5).tolist()
        st.session_state.synthesis = {"type": synthesis_type, "themes": themes, "strongest": strongest, "places": selected_places}
    synth = st.session_state.get("synthesis")
    if synth:
        st.markdown("### Recurring themes")
        st.write(", ".join(f"{k} ({v})" for k, v in synth["themes"].items()))
        st.markdown("### Places that felt similar")
        st.write(", ".join(synth["places"][:3]) or "Add places to compare.")
        st.markdown("### Questions that remain unanswered")
        st.write("What institutions shape daily life here? What changed recently? What did I assume too quickly?")
        st.markdown("### Strongest observations")
        for item in synth["strongest"]:
            st.markdown(f"- {item[:240]}")
        st.markdown("### Possible essay / podcast angles")
        st.write("A strong draft can compare what repeated across places and what resisted easy explanation.")
        st.markdown("### Next trip prompts")
        st.write("Ask one local institution question, one food question, one work/economy question, and one memory/history question.")


def note_library_page() -> None:
    st.title("Library")
    st.caption("Your private field notes, questions, place briefs, and reflections.")
    records = get_private_records()
    briefs = get_place_brief_records()
    selected = st.selectbox("Filter", FIELDWORK_FILTERS, index=0, key="library_filter")
    show_briefs = selected in {"All", "Place Briefs"}
    visible = filter_records(records, selected)
    if visible.empty and (not show_briefs or briefs.empty):
        st.info("No private records match this filter.")
        return
    if show_briefs and not briefs.empty:
        for _, brief in briefs.iterrows():
            with st.container(border=True):
                st.caption("PLACE BRIEF")
                st.subheader(brief["cleaned_title"])
                st.write(brief.get("private_summary", ""))
                st.caption(brief.get("location_name", ""))
    for _, row in visible.iterrows():
        label = "DRAFT CANDIDATE" if str(row.get("privacy_level")) == "public-ready" else str(row.get("record_kind", "field_note")).replace("_", " ").upper()
        with st.container(border=True):
            st.caption(label)
            st.subheader(row.get("cleaned_title") or "Untitled field note")
            st.write(f"{row.get('location_name', '')} | {row.get('date', '')} | {row.get('record_kind', '')}")
            st.write(row.get("private_summary") or make_private_summary(row.get("note_text", ""), str(row.get("record_kind", "field note")), row.get("location_name", "")))
            st.caption(f"Tags: {row.get('tags', '')}")
            c1, c2, c3 = st.columns(3)
            if c1.button("View", key=f"lib_view_{row['id']}"):
                st.session_state[f"show_detail_{row['id']}"] = not st.session_state.get(f"show_detail_{row['id']}", False)
            if c2.button("Ask follow-up", key=f"lib_ask_{row['id']}"):
                st.session_state.ask_prefill = row.get("note_text", "")
                st.session_state.ask_place_prefill = row.get("location_name", "")
                go_to("Ask")
            if c3.button("Export", key=f"lib_export_{row['id']}"):
                st.session_state.export_selection = [f"Field note:{row['id']}"]
                go_to("Export")
            if st.session_state.get(f"show_detail_{row['id']}", False):
                st.markdown("**User original words**")
                st.write(row.get("note_text", ""))
                st.markdown("**AI summary**")
                st.write(row.get("private_summary", ""))


def export_center_page() -> None:
    st.title("Export")
    st.caption("Turn selected field notes into something you can use. Rough observations → selected insight → draft output.")
    st.warning("Public drafts are drafts. Review manually before publishing.")
    st.markdown("Private Note → Public-safe Draft → Manual Review → Copy/Export")
    items = fetch_all_library_items()
    if items.empty:
        st.info("Capture notes before exporting.")
        return
    options = [f"{row.source_type}:{row.source_id}" for row in items.itertuples()]
    labels = {f"{row.source_type}:{row.source_id}": f"{row.display_title} | {row.display_location}" for row in items.itertuples()}
    default = [item for item in st.session_state.pop("export_selection", []) if item in options]
    selection = st.multiselect("Select private records", options, default=default, format_func=lambda value: labels.get(value, value))
    export_type = st.selectbox("Export type", ["Public-safe travel reflection", "Essay outline", "Substack-style essay", "Podcast script", "Japanese diary", "English field note", "Field report", "Markdown archive"])
    button_label = "Create Public Draft" if export_type == "Public-safe travel reflection" else "Create Draft"
    if st.button(button_label, width="stretch"):
        selected_items = get_selected_items(selection, items)
        if not selected_items:
            st.error("Select at least one private record.")
            return
        mapped_type = "English field note" if export_type in {"Public-safe travel reflection", "Field report", "Essay outline"} else export_type
        title, content = generate_export(mapped_type, selected_items)
        if export_type == "Public-safe travel reflection":
            content = "PUBLIC-SAFE DRAFT — MANUAL REVIEW REQUIRED\n\n" + content + "\n\nRemoved/generalized by policy: exact address, real-time location, future itinerary, private names, raw transcript, affiliations, and sensitive comments should be checked manually."
        st.session_state.generated_export = {"title": title, "content": content, "items": selected_items, "type": export_type}
    generated = st.session_state.get("generated_export")
    if generated:
        st.subheader(generated["title"])
        st.text_area("Draft output", generated["content"], height=420)
        if st.button("Save Export Record"):
            export_id = save_export(generated["type"], generated["items"], generated["content"], generated["title"])
            st.success(f"Saved private export #{export_id}.")


def main() -> None:
    apply_style()
    handle_voice_query_params()
    pages = [
        "Home",
        "Understand",
        "Ask",
        "Capture",
        "Memory Map",
        "Synthesize",
        "Library",
        "Export",
    ]
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if st.session_state.page not in pages:
        st.session_state.page = "Home"
    page = render_sidebar(pages)
    st.session_state.page = page
    render_top_nav(pages)

    if page == "Home":
        home_page()
    elif page == "Understand":
        ai_companion_page()
    elif page == "Ask":
        ask_page()
    elif page == "Capture":
        add_field_note_page()
    elif page == "Memory Map":
        map_view_page()
    elif page == "Synthesize":
        journey_review_page()
    elif page == "Library":
        note_library_page()
    elif page == "Export":
        export_center_page()


if __name__ == "__main__":
    main()
