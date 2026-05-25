from __future__ import annotations

import html
import shutil
from datetime import date
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


APP_NAME = "Waymark Atlas"


st.set_page_config(page_title=APP_NAME, page_icon="🗺️", layout="wide")
initialize_app()


CATEGORIES = [
    "food",
    "farm",
    "small town",
    "road",
    "motel",
    "church",
    "conversation",
    "landscape",
    "museum",
    "music",
    "neighborhood",
    "other",
]

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
                min-height: 27rem;
                display: grid;
                align-items: end;
                padding: 1.55rem;
                margin: 1rem 0 1.25rem;
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
                min-height: 10rem;
                padding: 1.25rem;
                border-top: 2px solid var(--atlas-gold);
                background: rgba(255, 252, 246, 0.88);
                box-shadow: 0 18px 46px rgba(35, 24, 13, 0.06);
            }

            .brief-section h4 {
                margin: 0 0 0.7rem;
                color: var(--atlas-ink);
                font-size: 0.86rem;
                letter-spacing: 0.1rem;
                text-transform: uppercase;
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


def render_sidebar(pages: list[str]) -> str:
    nav_labels = {
        "Home": "Home",
        "Explore Map": "Explore Map",
        "Read Reviews": "Read Reviews",
        "Search & Map": "Search & Map",
        "Capture Note": "Capture Note",
        "AI Brief": "AI Brief",
        "Community Log": "Community Log",
        "Library": "Library",
        "Export": "Export",
        "Publish Safely": "Publish Safely",
    }
    st.sidebar.title(APP_NAME)
    st.sidebar.markdown(
        '<div class="sidebar-tagline">Private road notes, maps, community logs, and public-ready storytelling.</div>',
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
    nav_button("AI Brief", "Plan Brief")
    nav_button("Explore Map")
    nav_button("Read Reviews")
    st.sidebar.markdown('<div class="nav-section">After</div>', unsafe_allow_html=True)
    nav_button("Capture Note")
    nav_button("Community Log")
    nav_button("Search & Map", "Search My Atlas")
    nav_button("Library")
    nav_button("Export")
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


def home_page() -> None:
    notes = fetch_field_notes()
    farms = fetch_farmstay_logs()
    mapped, _ = build_map_points(notes, farms)

    st.markdown(
        """
        <div class="atlas-hero">
            <div>
            <div class="atlas-kicker">Private field intelligence for the American road</div>
            <h1>Waymark Atlas</h1>
            <h3>An AI field companion for understanding America by road.</h3>
            <p>Collect roadtrip and community observations, map them, generate cultural context, and turn private notes into public-ready stories.</p>
            <div class="atlas-pill-row">
                <span class="atlas-pill">Road notes</span>
                <span class="atlas-pill">Community logs</span>
                <span class="atlas-pill">Map memory</span>
                <span class="atlas-pill">Private by default</span>
            </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="atlas-choice-label">Choose your journey mode</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="journey-card">
                <div class="atlas-choice-label">Before the journey</div>
                <h3>Plan where you are going</h3>
                <p>Enter a destination, get local context, see it on the map, and decide what to notice before you arrive.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Plan a Journey", width="stretch"):
            go_to("AI Brief")
    with c2:
        st.markdown(
            """
            <div class="journey-card">
                <div class="atlas-choice-label">After the journey</div>
                <h3>Reflect on what happened</h3>
                <p>Search your mapped notes, write field records, and transform selected memories into publishable work.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Reflect on a Journey", width="stretch"):
            go_to("Search & Map")

    if not mapped.empty:
        st.markdown("### Your Atlas Map")
        midpoint = [mapped["longitude"].mean(), mapped["latitude"].mean()]
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=mapped,
            get_position="[longitude, latitude]",
            get_fill_color="color",
            get_radius=10500,
            pickable=True,
            opacity=0.8,
        )
        st.pydeck_chart(
            pdk.Deck(
                layers=[layer],
                initial_view_state=pdk.ViewState(latitude=midpoint[1], longitude=midpoint[0], zoom=3.6),
                tooltip={
                    "html": "<b>{title}</b><br/>{location}<br/>{category}<br/><br/>{summary}",
                    "style": {"backgroundColor": "#17211c", "color": "white"},
                },
            ),
            use_container_width=True,
        )

    left, right = st.columns([1.2, 0.8])
    with left:
        st.markdown(
            """
            <div class="atlas-panel">
                <h3>Designed for the private-to-public workflow</h3>
                <p class="small-muted">Waymark Atlas keeps raw observations separate from organized knowledge and public storytelling. Exact places, raw transcripts, personal names, and real-time movement stay private unless you deliberately transform them.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown('<div class="atlas-photo-strip"></div>', unsafe_allow_html=True)


def before_journey_page() -> None:
    st.title("Before the Journey")
    st.caption("Start here when you are deciding where to go or what to notice before arrival.")
    c1, c2 = st.columns([1.1, 0.9])
    with c1:
        st.markdown(
            """
            <div class="atlas-route-card">
                <div>
                    <div class="atlas-choice-label">Destination intelligence</div>
                    <h3>Before You Arrive Brief</h3>
                    <p>Type a place, choose the best suggestion, then receive a sourced visual brief with map context and field prompts.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open AI Brief", width="stretch"):
            go_to("AI Brief")
    with c2:
        st.markdown(
            """
            <div class="atlas-panel">
                <h3>What this helps you do</h3>
                <p class="small-muted">Arrive with a quiet checklist: history, food, institutions, work rhythms, local etiquette, and questions worth asking.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('<div class="atlas-choice-label">Included in this mode</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="atlas-panel">
            <h3>AI Brief</h3>
            <p class="small-muted">Search any U.S. city, town, national park, historical park, landmark, or destination covered by OpenStreetMap, then generate a sourced local brief.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def after_journey_page() -> None:
    st.title("After the Journey")
    st.caption("Start here when you want to search, reflect, organize, or publish what you experienced.")
    c1, c2, c3 = st.columns(3)
    actions = [
        ("Search the map", "Find notes by place, category, and memory.", "Search & Map", "Open Map"),
        ("Capture a note", "Save a raw observation with photos, transcript, and publishing choice.", "Capture Note", "Add Note"),
        ("Community log", "Record a farmstay, local conversation, community event, or meaningful exchange.", "Community Log", "Add Community Log"),
    ]
    for col, (title, body, page_name, button_label) in zip((c1, c2, c3), actions):
        with col:
            st.markdown(
                f'<div class="atlas-action-card"><div><h4>{title}</h4><p>{body}</p></div></div>',
                unsafe_allow_html=True,
            )
            if st.button(button_label, key=f"after_{page_name}", width="stretch"):
                go_to(page_name)
    c4, c5, c6 = st.columns(3)
    more_actions = [
        ("Library", "Read your real field reviews and detailed source notes.", "Library", "Open Library"),
        ("Export", "Turn selected observations into essays, scripts, captions, or archive notes.", "Export", "Create Export"),
        ("Publish safely", "Create an anonymized public draft and review removed details.", "Publish Safely", "Prepare Public Version"),
    ]
    for col, (title, body, page_name, button_label) in zip((c4, c5, c6), more_actions):
        with col:
            st.markdown(
                f'<div class="atlas-action-card"><div><h4>{title}</h4><p>{body}</p></div></div>',
                unsafe_allow_html=True,
            )
            if st.button(button_label, key=f"after_more_{page_name}", width="stretch"):
                go_to(page_name)


def add_field_note_page() -> None:
    st.title("Capture Note")
    st.caption("Save the raw observation, then choose whether it stays private or becomes a public-ready draft.")

    with st.form("field_note_form", clear_on_submit=False):
        left, right = st.columns(2)
        title = left.text_input("Title")
        note_date = right.date_input("Date", value=date.today())
        location_name = left.text_input("Location name")
        address = right.text_input("Address")
        city = left.text_input("City")
        state = right.text_input("State")
        lat_col, lon_col = st.columns(2)
        latitude = lat_col.number_input("Latitude", value=None, format="%.6f")
        longitude = lon_col.number_input("Longitude", value=None, format="%.6f")
        category = st.selectbox("Category", CATEGORIES)
        note_text = st.text_area("Note text", height=180)
        photo = st.file_uploader("Photo upload", type=["png", "jpg", "jpeg", "webp"])
        audio = st.file_uploader("Audio upload", type=["mp3", "m4a", "wav", "aac"])
        audio_transcript = st.text_area("Audio transcript", height=120)
        tags = st.text_input("Tags", placeholder="comma-separated tags")
        publishing_choice = st.selectbox(
            "Publishing choice",
            [
                "Keep private in my atlas",
                "Save as semi-private working note",
                "Prepare as public-ready draft",
            ],
            help="Private notes keep exact details for your own use. Public-ready drafts should still be reviewed before publishing.",
        )
        submitted = st.form_submit_button("Save Note")

    if submitted:
        if not title.strip() and not note_text.strip():
            st.error("Please add at least a title or note text.")
            return
        photo_path = save_upload(photo, "photos")
        audio_path = save_upload(audio, "audio")
        location = location_name or city or state
        ai_summary = generate_ai_summary(note_text, category, location)
        ai_context = generate_ai_context(note_text, category, location)
        privacy_level = {
            "Keep private in my atlas": "private",
            "Save as semi-private working note": "semi-private",
            "Prepare as public-ready draft": "public-ready",
        }[publishing_choice]
        note_id = insert_field_note(
            {
                "title": title or "Untitled field note",
                "date": note_date.isoformat(),
                "location_name": location_name,
                "address": address,
                "latitude": latitude,
                "longitude": longitude,
                "city": city,
                "state": state,
                "category": category,
                "note_text": note_text,
                "photo_path": photo_path,
                "audio_path": audio_path,
                "audio_transcript": audio_transcript,
                "ai_summary": ai_summary,
                "ai_context": ai_context,
                "tags": tags,
                "privacy_level": privacy_level,
            }
        )
        st.success(f"Saved field note #{note_id}.")
        with st.container(border=True):
            st.subheader(title or "Untitled field note")
            st.write(ai_summary)
            render_context_block(ai_context)


def map_view_page() -> None:
    st.title("Search & Map")
    st.caption("Search any destination to orient the map, or search your saved reviews and notes.")
    notes = fetch_field_notes()
    farms = fetch_farmstay_logs()
    mapped, needs_location = build_map_points(notes, farms)

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

    search = st.text_input("Search saved notes and reviews", placeholder="Try: market, Knoxville, farm, church")
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

    if mapped.empty:
        st.info("No notes with coordinates yet.")
    elif visible.empty:
        st.info("No mapped records match the current search.")
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
            f"{row.source}:{row.source_id}": f"{row.source} · {row.title} · {row.location}"
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
            st.write(f"{selected_row['location']} · {selected_row['category']}")
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


def ai_companion_page() -> None:
    st.title("AI Brief")
    st.caption("Start typing a destination. Suggestions come from OpenStreetMap, so small cities, national parks, historical parks, landmarks, and rural places are searchable.")

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
        "Trip purpose",
        ["General field observation", "Road trip stop", "Community visit", "Food research", "Essay/podcast research", "Public field note"],
    )
    interests = st.multiselect(
        "Optional interests",
        ["history", "food", "race/community", "agriculture", "music", "religion", "economy", "small-town life", "nature", "sports"],
        default=["history", "food", "economy"],
    )
    generate = st.button("Generate Before You Arrive Brief", width="stretch")

    if generate:
        if not (corrected or destination).strip():
            st.error("Please enter a destination first.")
        else:
            brief = generate_destination_brief(corrected or destination, suggested_state, trip_purpose, interests)
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
        escaped_speech = speech_text.replace("\\", "\\\\").replace("`", "\\`")
        components.html(
            f"""
            <button
              style="border:0;border-radius:999px;padding:12px 18px;background:#17211c;color:white;font-weight:800;cursor:pointer;"
              onclick="window.speechSynthesis.cancel(); window.speechSynthesis.speak(new SpeechSynthesisUtterance(`{escaped_speech}`));">
              Listen to brief
            </button>
            <button
              style="border:1px solid rgba(23,33,28,.2);border-radius:999px;padding:11px 16px;background:white;color:#17211c;font-weight:800;cursor:pointer;margin-left:8px;"
              onclick="window.speechSynthesis.cancel();">
              Stop
            </button>
            """,
            height=56,
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
                    st.markdown(
                        f"""
                        <div class="brief-section">
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
                    st.markdown(f"- [{item.get('title')}]({item.get('url')}) — {item.get('description') or 'public reference'}")
        if brief.get("sources"):
            st.markdown("**Sources**")
            for source in brief["sources"]:
                st.markdown(f"- [{source['name']}]({source['url']})")
        if st.button("Save this brief"):
            brief_id = insert_ai_brief(brief)
            st.success(f"Saved brief #{brief_id}.")


def farmstay_log_page() -> None:
    st.title("Community Log")
    st.caption("Use this for farmstays, local conversations, community events, shared meals, volunteer days, or any meaningful exchange with people in a place. Keep private names and exact addresses out of public versions.")
    with st.form("farmstay_form"):
        left, right = st.columns(2)
        log_date = left.date_input("Date", value=date.today())
        farm_name = right.text_input("Community / host / place name")
        location_name = left.text_input("Location name")
        farm_type = right.selectbox(
            "Encounter type",
            ["local conversation", "community event", "farmstay", "market visit", "homestay", "volunteer day", "religious or civic gathering", "workshop", "other"],
        )
        lat_col, lon_col = st.columns(2)
        latitude = lat_col.number_input("Latitude", value=None, format="%.6f", key="farm_lat")
        longitude = lon_col.number_input("Longitude", value=None, format="%.6f", key="farm_lon")
        work_done = st.text_area("Activity / what happened")
        people_met = st.text_area("People met (private; use first names or roles only if safe)")
        food_eaten = st.text_area("Food or hospitality shared")
        conversation_topics = st.text_area("Conversation topics")
        lifestyle_observations = st.text_area("Community observations")
        labor_intensity = st.slider("Intensity of interaction", 1, 5, 3)
        community_feeling = st.slider("Community feeling", 1, 5, 3)
        surprises = st.text_area("What surprised me")
        reflection = st.text_area("Reflection", height=140)
        submitted = st.form_submit_button("Save Community Log")

    if submitted:
        payload = {
            "date": log_date.isoformat(),
            "farm_name": farm_name,
            "location_name": location_name,
            "latitude": latitude,
            "longitude": longitude,
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
    st.title("Library")
    st.caption("Actual field reviews from your notes and community logs. AI summaries are secondary; the review text is the primary record.")
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
            st.write(f"{item.get('date', '')} · {item.get('display_location', '')} · {item.get('display_category', '')}")
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
    labels = {f"{row.source_type}:{row.source_id}": f"{row.source_type} · {row.display_title} · {row.display_location}" for row in items.itertuples()}
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
    labels = {str(row.id): f"{row.title} · {row.location_name} · {row.date}" for row in notes.itertuples()}
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
        "Explore Map",
        "Read Reviews",
        "Search & Map",
        "Capture Note",
        "AI Brief",
        "Community Log",
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
    elif page == "Explore Map":
        map_view_page()
    elif page == "Read Reviews":
        note_library_page()
    elif page == "Capture Note":
        add_field_note_page()
    elif page == "Search & Map":
        map_view_page()
    elif page == "AI Brief":
        ai_companion_page()
    elif page == "Community Log":
        farmstay_log_page()
    elif page == "Library":
        note_library_page()
    elif page == "Export":
        export_center_page()
    elif page == "Publish Safely":
        privacy_page()


if __name__ == "__main__":
    main()
