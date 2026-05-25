from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

import pandas as pd
import pydeck as pdk
import streamlit as st
import streamlit.components.v1 as components

from ai_utils import (
    generate_ai_context,
    generate_ai_summary,
    generate_destination_brief,
    generate_farmstay_summary,
    geocode_destination,
    normalize_destination,
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


st.set_page_config(page_title="Field Atlas", page_icon="🗺️", layout="wide")
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
                --atlas-ink: #17211c;
                --atlas-muted: #657064;
                --atlas-paper: #f4f1ea;
                --atlas-card: rgba(255, 255, 255, 0.86);
                --atlas-line: rgba(32, 42, 35, 0.12);
                --atlas-green: #2f6f58;
                --atlas-rust: #a65d3a;
                --atlas-gold: #d1a451;
            }

            .stApp {
                background:
                    radial-gradient(circle at 7% 8%, rgba(47, 111, 88, 0.10), transparent 27rem),
                    linear-gradient(180deg, #f7f4ed 0%, #ede8dd 100%);
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
                    linear-gradient(180deg, rgba(255, 255, 255, 0.84), rgba(244, 241, 234, 0.96)),
                    url("https://images.unsplash.com/photo-1524661135-423995f22d0b?auto=format&fit=crop&w=900&q=70");
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
                background: rgba(248, 246, 241, 0.88);
                backdrop-filter: blur(18px);
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

            [data-testid="stSidebar"] [role="radiogroup"] {
                display: grid;
                gap: 0.42rem;
                margin-top: 1rem;
            }

            [data-testid="stSidebar"] label {
                border: 1px solid rgba(23, 33, 28, 0.10);
                border-radius: 999px;
                padding: 0.62rem 0.82rem;
                background: rgba(255, 255, 255, 0.58);
                transition: all 160ms ease;
            }

            [data-testid="stSidebar"] label:hover {
                border-color: rgba(47, 111, 88, 0.35);
                background: rgba(255, 255, 255, 0.82);
                transform: translateX(2px);
            }

            [data-testid="stSidebar"] label:has(input:checked) {
                color: #ffffff;
                border-color: rgba(23, 33, 28, 0.08);
                background: linear-gradient(135deg, #17211c, #2f6f58);
                box-shadow: 0 10px 26px rgba(23, 33, 28, 0.18);
            }

            [data-testid="stSidebar"] label:has(input:checked) p {
                color: #ffffff;
                font-weight: 700;
            }

            [data-testid="stSidebar"] input[type="radio"] {
                appearance: none;
                width: 0.58rem;
                height: 0.58rem;
                border-radius: 999px;
                border: 1px solid rgba(23, 33, 28, 0.24);
                background: rgba(255, 255, 255, 0.56);
                margin: 0 0.52rem 0 0;
                display: inline-block;
                vertical-align: middle;
            }

            [data-testid="stSidebar"] input[type="radio"]:checked {
                border-color: #ffffff;
                background: var(--atlas-gold);
                box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.22);
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

            .nav-active {
                border-radius: 999px;
                padding: 0.76rem 0.92rem;
                margin: 0.35rem 0;
                color: #ffffff;
                background: linear-gradient(135deg, #17211c, #2f6f58);
                box-shadow: 0 10px 26px rgba(23, 33, 28, 0.18);
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

            [data-testid="stSidebar"] .stButton > button {
                width: 100%;
                justify-content: flex-start;
                border-radius: 999px;
                padding: 0.72rem 0.92rem;
                margin: 0.08rem 0;
                color: var(--atlas-ink);
                background: rgba(255, 255, 255, 0.58);
                border: 1px solid rgba(23, 33, 28, 0.10);
                box-shadow: none;
                font-weight: 750;
                min-height: 2.7rem;
            }

            [data-testid="stSidebar"] .stButton > button:hover {
                background: rgba(255, 255, 255, 0.84);
                border-color: rgba(47, 111, 88, 0.32);
                transform: translateX(2px);
            }

            .atlas-hero {
                min-height: 70vh;
                display: grid;
                align-items: end;
                overflow: hidden;
                border: 1px solid rgba(255, 255, 255, 0.46);
                border-radius: 24px;
                padding: clamp(1.25rem, 4vw, 3rem);
                margin-bottom: 1.35rem;
                color: #ffffff;
                background:
                    linear-gradient(180deg, rgba(9, 17, 12, 0.04) 0%, rgba(9, 17, 12, 0.74) 100%),
                    linear-gradient(90deg, rgba(9, 17, 12, 0.82), rgba(9, 17, 12, 0.14) 62%),
                    url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=80");
                background-size: cover;
                background-position: center;
                box-shadow: 0 28px 70px rgba(23, 33, 28, 0.22);
            }

            .atlas-hero h1 {
                color: #ffffff;
                font-size: clamp(4.1rem, 10vw, 8.2rem);
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
                color: rgba(255, 255, 255, 0.76);
                font-size: 0.78rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.14rem;
                margin-bottom: 0.35rem;
            }

            .atlas-card {
                background: var(--atlas-card);
                border: 1px solid var(--atlas-line);
                border-radius: 16px;
                padding: 1rem;
                margin-bottom: 0.8rem;
                box-shadow: 0 18px 44px rgba(23, 33, 28, 0.08);
                backdrop-filter: blur(14px);
            }

            .atlas-panel {
                background: rgba(255, 255, 255, 0.76);
                border: 1px solid var(--atlas-line);
                border-radius: 18px;
                padding: 1.15rem;
                box-shadow: 0 18px 46px rgba(23, 33, 28, 0.07);
            }

            .atlas-action-card {
                min-height: 9.5rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                background: rgba(255, 255, 255, 0.80);
                border: 1px solid var(--atlas-line);
                border-radius: 18px;
                padding: 1.05rem;
                box-shadow: 0 14px 32px rgba(23, 33, 28, 0.07);
            }

            .atlas-action-card h4 {
                margin: 0 0 0.35rem;
                font-size: 1rem;
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
    st.sidebar.title("Field Atlas")
    st.sidebar.markdown(
        '<div class="sidebar-tagline">Private road notes, maps, farmstay logs, and public-ready storytelling.</div>',
        unsafe_allow_html=True,
    )
    return st.sidebar.radio(
        "Navigate",
        pages,
        index=pages.index(st.session_state.page),
        label_visibility="collapsed",
    )


def render_top_nav(pages: list[str]) -> None:
    st.markdown('<div class="top-nav-wrap">', unsafe_allow_html=True)
    for row_start in range(0, len(pages), 4):
        cols = st.columns(4)
        for col, page_name in zip(cols, pages[row_start : row_start + 4]):
            with col:
                if page_name == st.session_state.page:
                    st.markdown(f'<div class="top-nav-active">{page_name}</div>', unsafe_allow_html=True)
                elif st.button(page_name, key=f"top_nav_{page_name}", width="stretch"):
                    st.session_state.page = page_name
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def home_page() -> None:
    notes = fetch_field_notes()
    farms = fetch_farmstay_logs()
    states = notes["state"].dropna()
    states_count = len({state for state in states if str(state).strip()})

    st.markdown(
        """
        <div class="atlas-hero">
            <div>
            <div class="atlas-kicker">Private field intelligence for the American road</div>
            <h1>Field Atlas</h1>
            <h3>An AI field companion for understanding America by road.</h3>
            <p>Collect roadtrip and farmstay observations, map them, generate cultural context, and turn private notes into public-ready stories.</p>
            <div class="atlas-pill-row">
                <span class="atlas-pill">Road notes</span>
                <span class="atlas-pill">Farmstay logs</span>
                <span class="atlas-pill">Map memory</span>
                <span class="atlas-pill">Private by default</span>
            </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total field notes", len(notes))
    col2.metric("States visited", states_count)
    col3.metric("Farmstay logs", len(farms))

    st.markdown("### Start From The Field")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="atlas-action-card"><div><h4>Capture a place</h4><p>Save a raw note with location, media, tags, and privacy level.</p></div></div>', unsafe_allow_html=True)
        if st.button("Add Field Note", width="stretch"):
            st.session_state.page = "Add Field Note"
            st.rerun()
    with c2:
        st.markdown('<div class="atlas-action-card"><div><h4>Arrive prepared</h4><p>Generate a cultural and historical before-you-arrive brief.</p></div></div>', unsafe_allow_html=True)
        if st.button("Generate AI Brief", width="stretch"):
            st.session_state.page = "AI Companion"
            st.rerun()
    with c3:
        st.markdown('<div class="atlas-action-card"><div><h4>Log farm life</h4><p>Structure work, food, people, surprises, and reflection.</p></div></div>', unsafe_allow_html=True)
        if st.button("Add Farmstay Log", width="stretch"):
            st.session_state.page = "Farmstay Log"
            st.rerun()
    with c4:
        st.markdown('<div class="atlas-action-card"><div><h4>Make it public</h4><p>Turn selected notes into scripts, essays, captions, or public versions.</p></div></div>', unsafe_allow_html=True)
        if st.button("Export Notes", width="stretch"):
            st.session_state.page = "Export Center"
            st.rerun()

    left, right = st.columns([1.2, 0.8])
    with left:
        st.markdown(
            """
            <div class="atlas-panel">
                <h3>Designed for the private-to-public workflow</h3>
                <p class="small-muted">Field Atlas keeps raw observations separate from organized knowledge and public storytelling. Exact places, raw transcripts, personal names, and real-time movement stay private unless you deliberately transform them.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown('<div class="atlas-photo-strip"></div>', unsafe_allow_html=True)


def add_field_note_page() -> None:
    st.title("Add Field Note")
    st.caption("Capture the raw material first. You can refine, anonymize, and export it later.")

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
        privacy_level = st.radio("Privacy level", PRIVACY_LEVELS, horizontal=True)
        submitted = st.form_submit_button("Save Field Note")

    if submitted:
        if not title.strip() and not note_text.strip():
            st.error("Please add at least a title or note text.")
            return
        photo_path = save_upload(photo, "photos")
        audio_path = save_upload(audio, "audio")
        location = location_name or city or state
        ai_summary = generate_ai_summary(note_text, category, location)
        ai_context = generate_ai_context(note_text, category, location)
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
    st.title("Map View")
    st.caption("Search your notes, see the matching places on the map, then open the record without leaving this page.")
    notes = fetch_field_notes()
    farms = fetch_farmstay_logs()
    mapped, needs_location = build_map_points(notes, farms)

    search = st.text_input("Search mapped notes", placeholder="Try: market, Knoxville, farm, church")
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
        midpoint = [visible["longitude"].mean(), visible["latitude"].mean()]
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=visible,
            get_position="[longitude, latitude]",
            get_fill_color="color",
            get_radius=9000,
            pickable=True,
            opacity=0.82,
        )
        tooltip = {
            "html": "<b>{title}</b><br/>{location}<br/>{category}<br/><br/>{summary}<br/><em>Open details in Note Library.</em>",
            "style": {"backgroundColor": "#1f2a24", "color": "white"},
        }
        st.pydeck_chart(
            pdk.Deck(
                layers=[layer],
                initial_view_state=pdk.ViewState(latitude=midpoint[1], longitude=midpoint[0], zoom=4.2),
                tooltip=tooltip,
            ),
            width="stretch",
        )

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
                    "Field note" if selected_row["source"] == "Field note" else "Farmstay log",
                    int(selected_row["source_id"]),
                )
                st.session_state.page = "Privacy / Public Version"
                st.rerun()
            if c2.button("Export This Record", key=f"map_export_{selected_record}"):
                source_type = "Field note" if selected_row["source"] == "Field note" else "Farmstay log"
                st.session_state.export_selection = [f"{source_type}:{selected_row['source_id']}"]
                st.session_state.page = "Export Center"
                st.rerun()

    if not needs_location.empty:
        st.subheader("Needs Location Data")
        st.dataframe(needs_location[["source", "title", "location", "category"]], width="stretch")


def ai_companion_page() -> None:
    st.title("AI Companion")
    st.caption("Enter a destination. Field Atlas corrects light typos, suggests the state, then builds a sourced before-you-arrive brief.")

    destination = st.text_input("Destination", placeholder="Try: Louiville, Asheville, Chicago")
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
        ["General field observation", "Road trip stop", "Farmstay preparation", "Food research", "Essay/podcast research", "Public field note"],
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
            st.session_state.current_brief = brief

    brief = st.session_state.get("current_brief")
    if brief:
        title_line = ", ".join(part for part in [brief.get("destination"), brief.get("state")] if part)
        st.markdown(f"### Before You Arrive: {title_line}")
        if brief.get("image_url"):
            st.image(brief["image_url"], width="stretch")

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
                width="stretch",
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
            ("brief_15_sec", "1. 15-second brief"),
            ("historical_background", "2. Historical background"),
            ("cultural_signals", "3. Cultural signals to notice"),
            ("local_food", "4. Food and local institutions"),
            ("local_institutions", "Local institutions"),
            ("questions_to_ask", "5. Questions to ask locals"),
            ("field_note_prompts", "6. Field note prompts"),
            ("safety_etiquette", "7. Safety / etiquette notes"),
        ]
        for key, label in section_labels:
            with st.container(border=True):
                st.markdown(f"**{label}**")
                st.write(brief[key])
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
    st.title("Farmstay Log")
    with st.form("farmstay_form"):
        left, right = st.columns(2)
        log_date = left.date_input("Date", value=date.today())
        farm_name = right.text_input("Farm name")
        location_name = left.text_input("Location name")
        farm_type = right.selectbox("Farm type", FARM_TYPES)
        lat_col, lon_col = st.columns(2)
        latitude = lat_col.number_input("Latitude", value=None, format="%.6f", key="farm_lat")
        longitude = lon_col.number_input("Longitude", value=None, format="%.6f", key="farm_lon")
        work_done = st.text_area("Work done")
        people_met = st.text_area("People met")
        food_eaten = st.text_area("Food eaten")
        conversation_topics = st.text_area("Conversation topics")
        lifestyle_observations = st.text_area("Lifestyle observations")
        labor_intensity = st.slider("Labor intensity", 1, 5, 3)
        community_feeling = st.slider("Community feeling", 1, 5, 3)
        surprises = st.text_area("What surprised me")
        reflection = st.text_area("Reflection", height=140)
        submitted = st.form_submit_button("Save Farmstay Log")

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
        st.success(f"Saved farmstay log #{log_id}.")
        with st.container(border=True):
            st.subheader(farm_name or "Farmstay log")
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


def note_library_page() -> None:
    st.title("Note Library")
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
            st.write(item.get("ai_summary", ""))
            b1, b2, b3 = st.columns(3)
            detail_key = f"detail_{item.get('source_type')}_{item.get('source_id')}"
            public_key = f"public_{item.get('source_type')}_{item.get('source_id')}"
            if b1.button("View Details", key=detail_key):
                st.session_state.selected_detail = (item.get("source_type"), int(item.get("source_id")))
            if b2.button("Create Public Version", key=public_key):
                st.session_state.selected_public = (item.get("source_type"), int(item.get("source_id")))
                st.session_state.page = "Privacy / Public Version"
                st.rerun()
            if b3.button("Export", key=f"export_{item.get('source_type')}_{item.get('source_id')}"):
                st.session_state.export_selection = [f"{item.get('source_type')}:{item.get('source_id')}"]
                st.session_state.page = "Export Center"
                st.rerun()

    if st.session_state.get("selected_detail"):
        source_type, source_id = st.session_state.selected_detail
        st.divider()
        st.subheader("Details")
        record = get_field_note(source_id) if source_type == "Field note" else None
        if source_type == "Farmstay log":
            farms = fetch_farmstay_logs()
            match = farms[farms["id"] == source_id]
            record = match.iloc[0].to_dict() if not match.empty else None
        if record:
            st.json(record)


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
    st.title("Export Center")
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
    st.title("Privacy / Public Version")
    st.warning("Please manually review before publishing.")
    st.markdown(
        """
        Privacy principles: exact location and exact date are private by default; raw voice transcripts are private by default;
        names of private individuals are private by default; public output should be delayed and generalized; no affiliation disclosure;
        no real-time posting recommendation.
        """
    )

    if st.session_state.get("selected_public") and st.session_state.selected_public[0] == "Farmstay log":
        log = get_farmstay_log(int(st.session_state.selected_public[1]))
        if log:
            st.subheader("Farmstay public version")
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
        "Add Field Note",
        "Map View",
        "AI Companion",
        "Farmstay Log",
        "Note Library",
        "Export Center",
        "Privacy / Public Version",
    ]
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    page = render_sidebar(pages)
    st.session_state.page = page
    render_top_nav(pages)

    if page == "Home":
        home_page()
    elif page == "Add Field Note":
        add_field_note_page()
    elif page == "Map View":
        map_view_page()
    elif page == "AI Companion":
        ai_companion_page()
    elif page == "Farmstay Log":
        farmstay_log_page()
    elif page == "Note Library":
        note_library_page()
    elif page == "Export Center":
        export_center_page()
    elif page == "Privacy / Public Version":
        privacy_page()


if __name__ == "__main__":
    main()
