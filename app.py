from __future__ import annotations

import re
import sqlite3
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import pydeck as pdk
import streamlit as st


APP_NAME = "Waymark U.S."
TAGLINE = "Understand what you see. Remember what you notice."
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "waymark.db"
UPLOAD_DIR = BASE_DIR / "uploads"

RECORD_TYPES = [
        "place_brief",
        "question",
        "observation",
        "conversation",
        "food",
        "farmstay",
        "local_institution",
        "economic_signal",
        "cultural_signal",
        "reflection",
    ]

FILTERS = [
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

DESTINATIONS = {
        "Boston": ("Massachusetts", 42.3601, -71.0589),
        "Chicago": ("Illinois", 41.8781, -87.6298),
        "Louisville": ("Kentucky", 38.2527, -85.7585),
        "Knoxville": ("Tennessee", 35.9606, -83.9207),
        "Asheville": ("North Carolina", 35.5951, -82.5515),
        "Raleigh": ("North Carolina", 35.7796, -78.6382),
        "Nashville": ("Tennessee", 36.1627, -86.7816),
        "New Orleans": ("Louisiana", 29.9511, -90.0715),
        "Shelbyville": ("Indiana", 39.5214, -85.7769),
        "Grand Canyon": ("Arizona", 36.1069, -112.1129),
        "Yellowstone": ("Wyoming", 44.4280, -110.5885),
    }


def now_iso() -> str:
        return datetime.now().isoformat(timespec="seconds")


def ensure_storage() -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        (UPLOAD_DIR / "audio").mkdir(parents=True, exist_ok=True)
        (UPLOAD_DIR / "photos").mkdir(parents=True, exist_ok=True)


def conn() -> sqlite3.Connection:
        ensure_storage()
        db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        return db


def init_db() -> None:
        with conn() as db:
                    db.execute(
                                    """
                                                CREATE TABLE IF NOT EXISTS records (
                                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                                record_type TEXT,
                                                                                                title TEXT,
                                                                                                                cleaned_title TEXT,
                                                                                                                                place_name TEXT,
                                                                                                                                                city TEXT,
                                                                                                                                                                state TEXT,
                                                                                                                                                                                latitude REAL,
                                                                                                                                                                                                longitude REAL,
                                                                                                                                                                                                                created_at TEXT,
                                                                                                                                                                                                                                note_date TEXT,
                                                                                                                                                                                                                                                raw_text TEXT,
                                                                                                                                                                                                                                                                transcript TEXT,
                                                                                                                                                                                                                                                                                question_text TEXT,
                                                                                                                                                                                                                                                                                                ai_response TEXT,
                                                                                                                                                                                                                                                                                                                private_summary TEXT,
                                                                                                                                                                                                                                                                                                                                ai_context TEXT,
                                                                                                                                                                                                                                                                                                                                                tags TEXT,
                                                                                                                                                                                                                                                                                                                                                                visibility TEXT,
                                                                                                                                                                                                                                                                                                                                                                                source_record_ids TEXT,
                                                                                                                                                                                                                                                                                                                                                                                                export_type TEXT
                                                                                                                                                                                                                                                                                                                                                                                                            )
                                                                                                                                                                                                                                                                                                                                                                                                                        """
                                )
                    if db.execute("SELECT COUNT(*) FROM records").fetchone()[0] == 0:
                                    seed_records(db)


def seed_records(db: sqlite3.Connection) -> None:
        samples = [
                    ("observation", "Chicago station arrival", "Chicago", "Illinois", 41.8781, -87.6298, "The station felt like a machine for movement: commuters, luggage, food halls, and office workers crossing in every direction.", "transit,city,observation"),
                    ("food", "Knoxville diner counter", "Knoxville", "Tennessee", 35.9606, -83.9207, "A breakfast counter felt like a civic room, with coffee refills, weather talk, road work, and orange sports references.", "food,sports,conversation"),
                    ("farmstay", "Asheville market morning", "Asheville", "North Carolina", 35.5951, -82.5515, "Local agriculture was visible as food, labor, visitor economy, land pressure, and weather knowledge all at once.", "farmstay,food,agriculture"),
                    ("reflection", "Raleigh growth walk", "Raleigh", "North Carolina", 35.7796, -78.6382, "New apartments, older shaded streets, churches, and research-economy confidence made growth feel layered rather than simple.", "growth,city,reflection"),
                ]
        for rec_type, title, city, state, lat, lon, text, tags in samples:
                    insert_record(
                                    {
                                                        "record_type": rec_type,
                                                        "title": title,
                                                        "cleaned_title": title,
                                                        "place_name": city,
                                                        "city": city,
                                                        "state": state,
                                                        "latitude": lat,
                                                        "longitude": lon,
                                                        "created_at": now_iso(),
                                                        "note_date": str(date.today()),
                                                        "raw_text": text,
                                                        "transcript": "",
                                                        "question_text": "",
                                                        "ai_response": "",
                                                        "private_summary": summarize_note(rec_type, text),
                                                        "ai_context": "",
                                                        "tags": tags,
                                                        "visibility": "Private",
                                                        "source_record_ids": "",
                                                        "export_type": "",
                                                    },
                                    db,
                                )


def insert_record(payload: dict, db: sqlite3.Connection | None = None) -> int:
        owns_connection = db is None
        db = db or conn()
        cols = [
            "record_type",
            "title",
            "cleaned_title",
            "place_name",
            "city",
            "state",
            "latitude",
            "longitude",
            "created_at",
            "note_date",
            "raw_text",
            "transcript",
            "question_text",
            "ai_response",
            "private_summary",
            "ai_context",
            "tags",
            "visibility",
            "source_record_ids",
            "export_type",
        ]
        values = [payload.get(col, "") for col in cols]
        cur = db.execute(f"INSERT INTO records ({','.join(cols)}) VALUES ({','.join(['?'] * len(cols))})", values)
        if owns_connection:
                    db.commit()
                    db.close()
                return int(cur.lastrowid)


def records_df() -> pd.DataFrame:
        with conn() as db:
                    return pd.read_sql_query("SELECT * FROM records ORDER BY created_at DESC, id DESC", db)


def destination_lookup(place: str, state: str = "") -> tuple[str, str, float | None, float | None]:
        place = (place or "").strip()
    for known, info in DESTINATIONS.items():
                if known.lower() in place.lower() or place.lower() in known.lower():
                                return known, state or info[0], info[1], info[2]
                        parts = [part.strip() for part in re.split(r",|-", place) if part.strip()]
    city = parts[0] if parts else place
    return city or place, state or (parts[1] if len(parts) > 1 else ""), None, None


def clean_title(text: str, fallback: str = "Untitled field note") -> str:
        text = " ".join((text or "").split())
    if not text:
                return fallback
    text = re.sub(r"^(i want to know|i was wondering if|why do i need to|what do i need to)\s+", "", text, flags=re.I)
    title = text[:70].strip(" .!?")
    return title[:1].upper() + title[1:] if title else fallback


def classify_note(text: str, selected: str) -> str:
        if selected and selected != "Other":
                    return selected.lower().replace(" ", "_")
                t = (text or "").lower()
    if "?" in t or any(x in t for x in ["i want to know", "i was wondering", "why does", "what should"]):
                return "question"
    if any(x in t for x in ["pizza", "diner", "coffee", "food", "restaurant"]):
                return "food"
    if any(x in t for x in ["farm", "soil", "harvest", "barn"]):
                return "farmstay"
    if any(x in t for x in ["church", "school", "library", "station", "courthouse"]):
                return "local_institution"
    return "observation"


def summarize_note(record_type: str, text: str) -> str:
        body = " ".join((text or "").split())
    if record_type == "question":
                return "This is a place question. Use Ask or Understand before treating it as a publishable reflection."
    if record_type == "conversation":
                return "Conversation note. Remove names and identifying details before any export."
    if record_type == "food":
                return f"Food/local institution note: {body[:180]}"
    if record_type == "farmstay":
                return f"Farmstay/rural-life note. Treat names and exact farm location as sensitive. {body[:150]}"
    return f"Private field note: {body[:190]}"


def place_brief(destination: str, lens: str, question: str = "") -> dict[str, str]:
        city, state, _, _ = destination_lookup(destination)
    place = f"{city}, {state}".strip(", ")
    return {
                "15 seconds": f"**{place}** is best read through its institutions, work patterns, food rooms, civic rituals, and visible edges between old infrastructure and new money.",
                "How to read this place": f"Use **{lens.lower()}** as one lens, then check it against what you actually see: storefronts, churches, schools, roads, public buildings, sports colors, prices, accents, and who gathers where.",
                "What to notice": "Look for **daily routines**, not just landmarks: breakfast counters, gas stations, courthouse squares, campus edges, factory corridors, farmers markets, and transit points.",
                "Food and institutions": "Start with diners, markets, bakeries, local chains, church suppers, campus bars, libraries, county fairs, and sports bars. These often reveal who the place is built to serve.",
                "Economy / industries": "Ask what pays the bills here: universities, hospitals, logistics, tourism, farming, manufacturing, energy, government, military, or remote-work migration.",
                "History underneath the surface": "Look for what has been preserved, renamed, displaced, or converted: rail lines, riverfronts, mills, memorials, main streets, and neighborhoods split by highways.",
                "Questions to ask locals": "What has changed fastest? What place still feels local? What food would they defend? Which industry matters more than visitors realize?",
                "Field Anchors": "Good places to start observing: **main street**, **public library**, **farmers market**, **transit station**, **local diner**, **high school stadium**, and **county courthouse**.",
            }


def ask_response(place: str, observation: str, lens: str) -> str:
        return (
                    f"Possible lenses for **{place or 'this place'}**:\n\n"
                    f"- One explanation may involve **{lens.lower()}**, but treat this as a hypothesis.\n"
                    "- Check whether the scene is tied to work patterns, housing costs, religion, race/community history, local institutions, or tourism pressure.\n"
                    "- Notice what repeats: signs, prices, uniforms, school colors, empty storefronts, pickup trucks, murals, churches, factories, or meeting places.\n"
                    "- Ask a local: what changed here in the last ten years, and what has not changed at all?\n\n"
                    f"Your observation: {observation[:400]}"
                )


def export_text(rows: pd.DataFrame, export_type: str) -> str:
        joined = "\n".join(f"- {r.cleaned_title}: {r.private_summary}" for r in rows.itertuples())
    if "Public-safe" in export_type:
                return (
                    "Private Note -> Public-safe Draft -> Manual Review -> Copy/Export\n\n"
                    "This draft generalizes exact dates, locations, raw transcripts, private names, affiliations, and sensitive details.\n\n"
                    f"{joined}\n\nPublic-safe reflection: I moved through these places by paying attention to ordinary rooms, local institutions, food, work, and the questions each scene raised."
                )
    if "Podcast" in export_type:
                return f"Opening hook\nA road note begins with a small scene.\n\nWhat I noticed\n{joined}\n\nWhy it matters\nThese notes point toward the everyday machinery of place.\n\nClosing line\nMap what you noticed, not just where you went."
    if "Japanese" in export_type:
                return f"今日は、移動しながら見えた土地の手触りについて考えた。観光名所よりも、日常の場所や人の動きに、その町らしさが表れていた。\n\n{joined}"
    return f"{export_type}\n\nSelected field notes:\n{joined}\n\nDraft this outward only after manual privacy review."


def apply_theme() -> None:
        st.set_page_config(page_title=APP_NAME, page_icon="🧭", layout="wide")
    st.markdown(
                """
                        <style>
                                @import url('https://fonts.googleapis.com/css2?family=Newsreader:wght@600;700&family=Inter:wght@400;600;800&display=swap');
                                        :root { --green:#18382c; --gold:#b8945c; --ink:#191815; --muted:#706b61; --paper:#f7f1e6; }
                                                .stApp { background: linear-gradient(rgba(247,241,230,.94),rgba(247,241,230,.94)), repeating-linear-gradient(90deg, transparent 0 88px, rgba(184,148,92,.10) 89px 90px); color: var(--ink); }
                                                        h1, h2 { font-family: Newsreader, Georgia, serif !important; letter-spacing: 0 !important; }
                                                                h1 { font-size: clamp(3rem, 8vw, 6.8rem) !important; }
                                                                        [data-testid="stSidebar"] { background: #fbf7ef; border-right: 1px solid rgba(25,24,21,.12); }
                                                                                .hero { padding: clamp(2rem,5vw,5rem); min-height: 520px; display:flex; flex-direction:column; justify-content:end; color:#fff; background: linear-gradient(90deg, rgba(9,19,15,.86), rgba(9,19,15,.35)), url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1800&q=80') center/cover; }
                                                                                        .hero p { max-width: 780px; font-size: 1.35rem; line-height: 1.7; }
                                                                                                .eyebrow { color: var(--gold); text-transform: uppercase; font-weight: 800; letter-spacing: .18em; }
                                                                                                        .card { padding: 2rem; min-height: 250px; background: rgba(255,252,246,.90); border: 1px solid rgba(25,24,21,.14); box-shadow: 0 24px 70px rgba(35,24,13,.09); }
                                                                                                                .note-card { padding: 1.2rem; background: rgba(255,252,246,.95); border-left: 4px solid var(--gold); margin-bottom: 1rem; }
                                                                                                                        .privacy { padding: 1rem 1.2rem; background:#efe5d4; border-left:4px solid var(--green); }
                                                                                                                                div.stButton > button { border-radius: 999px; background: var(--green); color: white; border: 0; padding: .8rem 1.3rem; font-weight: 800; }
                                                                                                                                        div.stButton > button:hover { color: white; background:#285f49; }
                                                                                                                                                @media (max-width: 760px) { .hero { min-height: 430px; padding: 1.5rem; } .hero p { font-size: 1rem; } }
                                                                                                                                                        </style>
                                                                                                                                                                """,
                unsafe_allow_html=True,
            )


def nav() -> str:
        pages = ["Home", "Understand", "Ask", "Capture", "Memory Map", "Synthesize", "Library", "Export"]
    if "page" not in st.session_state or st.session_state.page not in pages:
                st.session_state.page = "Home"
    st.sidebar.title(APP_NAME)
    st.sidebar.caption("Private AI field journal.")
    for page in pages:
                if st.sidebar.button(page, key=f"nav_{page}", use_container_width=True):
                                st.session_state.page = page
                                st.rerun()
        st.sidebar.markdown('<div class="privacy">Nothing is published from Waymark. Public-safe drafts are only copyable drafts for manual review.</div>', unsafe_allow_html=True)
    return st.session_state.page


def home() -> None:
        st.markdown(
                    f"""
                            <section class="hero">
                                      <div class="eyebrow">A private AI field journal</div>
                                                <h1>{APP_NAME}</h1>
                                                          <h2>{TAGLINE}</h2>
                                                                    <p>Waymark helps curious travelers read a place before arriving, ask better questions while there, and turn rough road notes into maps, comparisons, essays, and reflections after the trip.</p>
                                                                            </section>
                                                                                    """,
                    unsafe_allow_html=True,
                )
    st.write("")
    cards = st.columns(3)
    actions = [
                ("Understand a Place", "Get a short How to read this place brief before you arrive.", "Generate Place Brief", "Understand"),
                ("Ask About What I’m Seeing", "Turn a confusing or interesting scene into a better question.", "Ask Waymark", "Ask"),
                ("Capture a Field Note", "Say the thought before it disappears.", "Capture Note", "Capture"),
            ]
    for col, (title, body, button, page) in zip(cards, actions):
                with col:
                                st.markdown(f'<div class="card"><div class="eyebrow">Core flow</div><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)
                                if st.button(button, key=f"home_{page}", use_container_width=True):
                                                    st.session_state.page = page
                                                    st.rerun()
                                        st.markdown("### Synthesize My Journey")
    st.write("Compare places, find recurring themes, and turn observations into essays or scripts.")
    st.info("Not an audio tour. Not a trip planner. Not just a travel diary. Waymark helps you notice, ask, compare, and remember.")


def understand() -> None:
        st.title("Understand a Place")
    st.write("Get oriented before you arrive. Waymark gives you a compact **How to read this place** brief, not a tourist checklist.")
    destination = st.text_input("Destination", placeholder="Boston, MA or Nashville, TN")
    state = st.text_input("State / region, optional")
    lens = st.selectbox("What lens do you want?", ["General orientation", "Local history", "Food and local institutions", "Farm / rural life", "Race and community", "Economy and industries", "Religion and civic life", "Sports and local identity", "Nature and landscape", "Small-town life"])
    question = st.text_input("Optional question", placeholder="What should I notice here? Why does this town feel this way?")
    if st.button('Generate "How to Read This Place" Brief', use_container_width=True):
                if not destination.strip():
                                st.error("We could not lock this destination. Please type the city and state manually.")
            return
        city, inferred_state, lat, lon = destination_lookup(destination, state)
        brief = place_brief(f"{city}, {inferred_state}", lens, question)
        st.session_state.generated_brief = (city, inferred_state, lat, lon, lens, brief)
    if "generated_brief" in st.session_state:
                city, state, lat, lon, lens, brief = st.session_state.generated_brief
        for key, value in brief.items():
                        st.markdown(f"### {key}")
            st.markdown(value)
        if st.button("Save Private Place Brief", use_container_width=True):
                        text = "\n\n".join(f"{k}: {v}" for k, v in brief.items())
            insert_record({"record_type": "place_brief", "title": f"How to read {city}", "cleaned_title": f"How to read {city}", "place_name": city, "city": city, "state": state, "latitude": lat, "longitude": lon, "created_at": now_iso(), "note_date": str(date.today()), "raw_text": "", "transcript": "", "question_text": question, "ai_response": text, "private_summary": brief["15 seconds"], "ai_context": text, "tags": lens.lower(), "visibility": "Private", "source_record_ids": "", "export_type": ""})
            st.success("Saved as a private place brief. It will appear in Memory Map and Library.")


def ask() -> None:
        st.title("Ask About What I’m Seeing")
    place = st.text_input("Current place / destination", value=st.session_state.pop("ask_place", ""))
    observation = st.text_area("What are you seeing?", value=st.session_state.pop("ask_text", ""), height=180, placeholder="I’m seeing a lot of churches and empty storefronts. What might explain that?")
    lens = st.selectbox("Optional lens", ["history", "economy", "religion", "race/community", "food", "agriculture", "sports", "urban design", "other"])
    if st.button("Ask Waymark", use_container_width=True):
                if not observation.strip():
                                st.error("Add the scene or question first.")
            return
        response = ask_response(place, observation, lens)
        st.session_state.ask_response = response
    if st.session_state.get("ask_response"):
                st.markdown(st.session_state.ask_response)
        if st.button("Save as Question", use_container_width=True):
                        city, state, lat, lon = destination_lookup(place)
            insert_record({"record_type": "question", "title": clean_title(observation, "Place question"), "cleaned_title": clean_title(observation, "Place question"), "place_name": place, "city": city, "state": state, "latitude": lat, "longitude": lon, "created_at": now_iso(), "note_date": str(date.today()), "raw_text": observation, "transcript": "", "question_text": observation, "ai_response": st.session_state.ask_response, "private_summary": summarize_note("question", observation), "ai_context": st.session_state.ask_response, "tags": f"question,{lens}", "visibility": "Private", "source_record_ids": "", "export_type": ""})
            st.success("Saved as a private question.")


def capture() -> None:
        st.title("Capture a Field Note")
    st.write("Say the thought before it disappears. Use this while moving, waiting, eating, working, or noticing a place. Everything is private by default.")
    st.caption("Voice-first hook: use phone/browser dictation in the transcript box for now. A native recorder can be connected later.")
    place = st.text_input("Location / Place", placeholder="Chicago, IL")
    title = st.text_input("Optional title")
    transcript = st.text_area("Transcript or rough note", height=180)
    note_type = st.selectbox("Note type", ["Other", "Question", "Observation", "Conversation", "Food", "Farmstay", "Local institution", "Economic signal", "Cultural signal", "Reflection", "Road scene"])
    visibility = st.selectbox("Visibility", ["Private", "Public-safe draft candidate"])
    if note_type == "Farmstay":
                extra = st.text_area("Optional farmstay details", placeholder="farm type, work done, food eaten, people met, what surprised me, what this reveals about rural life")
        transcript = "\n".join(part for part in [transcript, extra] if part.strip())
    c1, c2 = st.columns(2)
    if c1.button("Ask Waymark", use_container_width=True):
                st.session_state.ask_place = place
        st.session_state.ask_text = transcript
        st.session_state.page = "Ask"
        st.rerun()
    if c2.button("Save as Field Note", use_container_width=True):
                if not any([title.strip(), transcript.strip(), place.strip()]):
                                st.error("Add a place, title, or note first.")
            return
        rec_type = classify_note(transcript, note_type)
        city, state, lat, lon = destination_lookup(place)
        cleaned = title.strip() or clean_title(transcript)
        insert_record({"record_type": rec_type, "title": title or cleaned, "cleaned_title": cleaned, "place_name": place, "city": city, "state": state, "latitude": lat, "longitude": lon, "created_at": now_iso(), "note_date": str(date.today()), "raw_text": transcript, "transcript": transcript, "question_text": transcript if rec_type == "question" else "", "ai_response": "", "private_summary": summarize_note(rec_type, transcript), "ai_context": "", "tags": rec_type.replace("_", " "), "visibility": visibility, "source_record_ids": "", "export_type": ""})
        st.success("Saved as a private field note.")


def filter_df(df: pd.DataFrame, chosen: str) -> pd.DataFrame:
        if chosen == "All":
                    return df
    mapping = {
                "Questions": "question",
                "Observations": "observation",
                "Food": "food",
                "Farmstay": "farmstay",
                "Conversations": "conversation",
                "Local institutions": "local_institution",
                "Economic signals": "economic_signal",
                "Cultural signals": "cultural_signal",
                "Reflections": "reflection",
                "Place Briefs": "place_brief",
            }
    if chosen == "Export-ready":
                return df[df["visibility"].fillna("").str.contains("candidate", case=False)]
    return df[df["record_type"].eq(mapping.get(chosen, ""))]


def memory_map() -> None:
        st.title("Memory Map")
    st.write("Map what you noticed, not just where you went.")
    df = filter_df(records_df(), st.selectbox("Filter", FILTERS))
    mapped = df.dropna(subset=["latitude", "longitude"])
    mapped = mapped[mapped["latitude"].astype(str).ne("")]
    if not mapped.empty:
                st.pydeck_chart(
                                pdk.Deck(
                                                    initial_view_state=pdk.ViewState(latitude=float(mapped["latitude"].mean()), longitude=float(mapped["longitude"].mean()), zoom=4),
                                                    layers=[
                                                                            pdk.Layer(
                                                                                                        "ScatterplotLayer",
                                                                                                        data=mapped,
                                                                                                        get_position="[longitude, latitude]",
                                                                                                        get_radius=18000,
                                                                                                        get_fill_color=[24, 56, 44, 190],
                                                                                                        pickable=True,
                                                                                                    )
                                                                        ],
                                                    tooltip={"html": "<b>{cleaned_title}</b><br>{place_name}<br>{record_type}<br>{private_summary}<br><i>Open details in Library.</i>"},
                                                )
                            )
    else:
        st.info("No records with coordinates yet.")
    missing = df[df["latitude"].isna() | df["longitude"].isna()]
    if not missing.empty:
                st.subheader("Needs location")
        st.dataframe(missing[["cleaned_title", "place_name", "record_type", "private_summary"]], use_container_width=True)


def synthesize() -> None:
        st.title("Synthesize My Journey")
    st.write("Turn scattered road notes into patterns.")
    df = records_df()
    if df.empty:
                st.info("Capture notes first.")
        return
    synthesis_type = st.selectbox("Synthesis type", ["Recurring themes", "Compare places", "What surprised me", "Questions I kept asking", "What I learned about America", "Essay outline", "Podcast outline", "Field report"])
    selected = st.multiselect("Places to include", sorted(df["place_name"].dropna().unique()))
    subset = df[df["place_name"].isin(selected)] if selected else df
    st.markdown("### Recurring themes")
    st.write(", ".join(subset["record_type"].value_counts().head(6).index))
    st.markdown("### Places that felt different")
    st.write(", ".join(subset["place_name"].dropna().head(6)))
    st.markdown("### Questions that remain unanswered")
    st.write("What changed fastest here? Who benefits from the current economy? Which local institutions still gather people?")
    st.markdown("### Possible essay / podcast angles")
    st.write(f"{synthesis_type}: ordinary places as clues to work, memory, food, institutions, and belonging.")


def library() -> None:
        st.title("Library")
    st.write("Your private field notes, questions, place briefs, and reflections.")
    df = records_df()
    query = st.text_input("Search")
    chosen = st.selectbox("Filter", FILTERS, key="library_filter")
    df = filter_df(df, chosen)
    if query:
                haystack = df.fillna("").astype(str).agg(" ".join, axis=1)
        df = df[haystack.str.contains(query, case=False, na=False)]
    for row in df.itertuples():
                st.markdown(f'<div class="note-card"><div class="eyebrow">{row.record_type} · {row.visibility}</div><h3>{row.cleaned_title}</h3><p>{row.place_name} · {row.note_date}</p><p>{row.private_summary}</p><small>{row.tags}</small></div>', unsafe_allow_html=True)
        with st.expander("View details"):
                        st.write(row.raw_text or row.ai_response)


def export() -> None:
        st.title("Export")
    st.write("Turn selected field notes into something you can use.")
    st.warning("Public drafts are drafts. Review manually before publishing elsewhere.")
    df = records_df()
    if df.empty:
                st.info("Capture or save a place brief first.")
        return
    labels = {int(r.id): f"{r.cleaned_title} | {r.place_name} | {r.record_type}" for r in df.itertuples()}
    selected_ids = st.multiselect("Select records", list(labels), format_func=lambda x: labels[x])
    export_type = st.selectbox("Export type", ["Public-safe travel reflection", "Essay outline", "Substack-style essay", "Podcast script", "Japanese diary", "English field note", "Field report", "Markdown archive"])
    if st.button("Create Draft", use_container_width=True):
                if not selected_ids:
                                st.error("Select at least one record.")
            return
        rows = df[df["id"].isin(selected_ids)]
        st.text_area("Draft output", export_text(rows, export_type), height=380)


def main() -> None:
        apply_theme()
    init_db()
    page = nav()
    {
                "Home": home,
                "Understand": understand,
                "Ask": ask,
                "Capture": capture,
                "Memory Map": memory_map,
                "Synthesize": synthesize,
                "Library": library,
                "Export": export,
            }[page]()


if __name__ == "__main__":
        main()
