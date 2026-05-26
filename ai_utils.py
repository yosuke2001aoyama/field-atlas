from __future__ import annotations

import difflib
import re
from datetime import datetime
from urllib.parse import quote

import requests


HTTP_HEADERS = {
    "User-Agent": "WaymarkUS/1.0 (public Streamlit app; educational field-note tool)"
}

KNOWN_US_DESTINATIONS = [
    "Boston",
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

CURATED_US_DESTINATIONS = [
    {"destination": "Boston", "state": "Massachusetts", "latitude": 42.3601, "longitude": -71.0589, "kind": "city"},
    {"destination": "New York", "state": "New York", "latitude": 40.7128, "longitude": -74.0060, "kind": "city"},
    {"destination": "Washington", "state": "District of Columbia", "latitude": 38.9072, "longitude": -77.0369, "kind": "city"},
    {"destination": "Philadelphia", "state": "Pennsylvania", "latitude": 39.9526, "longitude": -75.1652, "kind": "city"},
    {"destination": "Chicago", "state": "Illinois", "latitude": 41.8781, "longitude": -87.6298, "kind": "city"},
    {"destination": "Los Angeles", "state": "California", "latitude": 34.0522, "longitude": -118.2437, "kind": "city"},
    {"destination": "San Francisco", "state": "California", "latitude": 37.7749, "longitude": -122.4194, "kind": "city"},
    {"destination": "Seattle", "state": "Washington", "latitude": 47.6062, "longitude": -122.3321, "kind": "city"},
    {"destination": "New Orleans", "state": "Louisiana", "latitude": 29.9511, "longitude": -90.0715, "kind": "city"},
    {"destination": "Denver", "state": "Colorado", "latitude": 39.7392, "longitude": -104.9903, "kind": "city"},
    {"destination": "Austin", "state": "Texas", "latitude": 30.2672, "longitude": -97.7431, "kind": "city"},
    {"destination": "Grand Canyon National Park", "state": "Arizona", "latitude": 36.2679, "longitude": -112.3535, "kind": "national park"},
    {"destination": "Yellowstone National Park", "state": "Wyoming", "latitude": 44.4280, "longitude": -110.5885, "kind": "national park"},
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
    "politics": "county and state election baselines, civic institutions, campaign signs, local media, and policy debates",
}

CURATED_PLACE_GUIDES = {
    "Boston": {
        "population": "City population is about **675,000**, with a metro area near **five million**. Read **Boston** as a university, hospital, finance, biotech, and port city rather than only a colonial-history destination.",
        "industries": "**Higher education**, **Mass General Brigham**, **biotech**, **finance**, **software**, tourism, maritime trade, and public-sector work shape daily rhythms.",
        "sports": "**Red Sox** at **Fenway Park**, **Celtics**, **Bruins**, **Patriots** regional fandom, the **Boston Marathon**, college rowing, and neighborhood sports bars are core civic signals.",
        "food": "**Clam chowder**, **lobster rolls**, **roast beef sandwiches**, **North End cannoli**, Irish pubs, seafood markets, and newer immigrant food corridors are the first food map.",
        "politics": "**Boston/Suffolk County** is strongly Democratic in recent presidential voting, while **Massachusetts** is also Democratic-leaning statewide. Use this as a baseline, then check precinct-level sources for current detail.",
        "must_visit": [
            {
                "name": "Freedom Trail",
                "why": "A compact way to read public memory, tourism, revolution-era sites, churches, burial grounds, and the way Boston packages origin stories.",
                "image_url": "https://images.unsplash.com/photo-1501979376754-2ff867a4f659?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Fenway Park area",
                "why": "Useful for seeing sports identity, neighborhood commerce, transit crowds, and how an old ballpark anchors modern development.",
                "image_url": "https://images.unsplash.com/photo-1577223625816-7546f13df25d?auto=format&fit=crop&w=900&q=80",
            },
        ],
    },
    "New Orleans": {
        "population": "City population is under **400,000**, while the metro area is around **one million**. **New Orleans** is best read through port geography, Black culture, tourism, music, food, water, and recovery politics.",
        "industries": "**Tourism**, hospitality, **Port of New Orleans** logistics, energy services, healthcare, universities, music/cultural production, and water infrastructure define the economy.",
        "sports": "**New Orleans Saints** football and **Pelicans** basketball matter, but **second lines**, school bands, **Mardi Gras Indians**, and festival calendars are just as important.",
        "food": "**Gumbo**, **po'boys**, **red beans and rice**, **beignets**, **crawfish**, **oysters**, **sno-balls**, Creole/Cajun traditions, and corner stores are core signals.",
        "politics": "**Orleans Parish** is strongly Democratic in recent presidential voting, while **Louisiana** statewide has leaned Republican. That city-state contrast is central context.",
        "must_visit": [
            {
                "name": "Treme and Congo Square",
                "why": "A starting point for Black music history, public memory, neighborhoods, churches, performance, and contested preservation.",
                "image_url": "https://images.unsplash.com/photo-1543101130-4beb2728c43d?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Bywater and the river edge",
                "why": "Shows port geography, flood memory, tourism pressure, murals, local restaurants, and changing housing patterns.",
                "image_url": "https://images.unsplash.com/photo-1508357941501-0924cf312bbd?auto=format&fit=crop&w=900&q=80",
            },
        ],
    },
    "Chicago": {
        "population": "City population is about **2.7 million**, with a metro area near **9.5 million**. **Chicago** is a rail, lake, finance, logistics, food, sports, architecture, and neighborhood city.",
        "industries": "**Finance**, **rail/freight logistics**, healthcare, universities, food processing, manufacturing legacy, media, conventions, and professional services drive the region.",
        "sports": "**Cubs**, **White Sox**, **Bulls**, **Bears**, **Blackhawks**, college sports, lakefront running, and neighborhood bar loyalties make sports a geography lesson.",
        "food": "**Deep-dish pizza**, **tavern-style pizza**, **Italian beef**, **Chicago dogs**, Polish and Mexican foodways, barbecue, and neighborhood bakeries reveal migration layers.",
        "politics": "**Chicago/Cook County** is strongly Democratic in recent presidential voting, while **Illinois** statewide also leans Democratic. Ward-level power remains useful context.",
        "must_visit": [
            {
                "name": "Chicago River architecture corridor",
                "why": "A readable cross-section of finance, infrastructure, architecture, tourism, and the downtown work economy.",
                "image_url": "https://images.unsplash.com/photo-1494522855154-9297ac14b55f?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Pilsen",
                "why": "Useful for murals, Mexican American culture, food, galleries, displacement pressure, and neighborhood identity.",
                "image_url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=900&q=80",
            },
        ],
    },
    "Louisville": {
        "population": "**Louisville/Jefferson County** is a consolidated metro government of roughly **780,000** people, linking river logistics, bourbon tourism, healthcare, manufacturing, and neighborhoods.",
        "industries": "**UPS Worldport**, **bourbon**, hospitality, healthcare, auto manufacturing, food and beverage, universities, and Ohio River commerce are key anchors.",
        "sports": "**University of Louisville Cardinals**, **Kentucky Derby**, **Louisville Bats**, high-school sports, and horse racing shape local attention.",
        "food": "**Hot Brown**, bourbon bars, barbecue, Southern breakfasts, immigrant restaurants, and Derby-season hospitality are worth reading.",
        "politics": "**Jefferson County** is Democratic-leaning in recent presidential voting, while **Kentucky** statewide is strongly Republican. That county-state split is important context.",
        "must_visit": [
            {
                "name": "Muhammad Ali Center and riverfront",
                "why": "Connects civil rights memory, sports, tourism, downtown redevelopment, and the Ohio River.",
                "image_url": "https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Old Louisville",
                "why": "Shows architecture, universities, preservation, rental housing, and the city beyond Derby imagery.",
                "image_url": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?auto=format&fit=crop&w=900&q=80",
            },
        ],
    },
    "Knoxville": {
        "population": "**Knoxville** has roughly **190,000** city residents and sits in a larger East Tennessee metro. Read it through **University of Tennessee**, the **Tennessee River**, Appalachia, logistics, and outdoor access.",
        "industries": "**University of Tennessee**, medical employment, logistics, manufacturing, tourism, **Oak Ridge** science links, retail, and outdoor recreation shape the region.",
        "sports": "**Tennessee Volunteers** football is the major civic rhythm; high-school sports and outdoor recreation also mark weekends.",
        "food": "**Barbecue**, **meat-and-three plates**, biscuits, breweries, Appalachian ingredients, farmers markets, and game-day food are useful signals.",
        "politics": "**Knox County** and East Tennessee lean Republican in recent presidential voting, while Knoxville itself contains more mixed urban and university politics.",
        "must_visit": [
            {
                "name": "Market Square",
                "why": "A compact place to read downtown revival, food, local retail, students, visitors, and public events.",
                "image_url": "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Tennessee River waterfront",
                "why": "Shows how river infrastructure, sports crowds, redevelopment, and outdoor life overlap.",
                "image_url": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=900&q=80",
            },
        ],
    },
    "Asheville": {
        "population": "**Asheville** has under **100,000** city residents but functions as western North Carolina's tourism, arts, healthcare, and mountain gateway.",
        "industries": "**Tourism**, hospitality, healthcare, **craft beer**, arts, outdoor recreation, retirement migration, and regional services shape the economy.",
        "sports": "**Asheville Tourists** baseball, outdoor endurance culture, high-school sports, and regional college sports matter more than major pro teams.",
        "food": "**Craft beer**, farm-to-table restaurants, biscuits, barbecue, Appalachian ingredients, bakeries, and farmers markets are central.",
        "politics": "**Buncombe County/Asheville** lean Democratic in recent presidential voting, while surrounding mountain counties are often more Republican. The urban-rural contrast is visible.",
        "must_visit": [
            {
                "name": "River Arts District",
                "why": "Good for seeing arts, tourism, flood vulnerability, redevelopment, warehouses, and changing land use.",
                "image_url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Blue Ridge Parkway overlook",
                "why": "Connects landscape, federal infrastructure, tourism, ecology, and the way mountain identity is staged.",
                "image_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=900&q=80",
            },
        ],
    },
    "Raleigh": {
        "population": "**Raleigh** has nearly **half a million** city residents and anchors the fast-growing **Research Triangle** with universities, state government, tech, healthcare, and suburban growth.",
        "industries": "**State government**, universities, **Research Triangle** tech, life sciences, healthcare, education, real estate, and services define the region.",
        "sports": "**Carolina Hurricanes**, **NC State Wolfpack**, college basketball rivalries, youth sports, and greenway recreation are strong signals.",
        "food": "**Eastern vs. Lexington-style barbecue** debates, biscuits, breweries, food halls, immigrant restaurants, and farmers markets are good entry points.",
        "politics": "**Wake County** leans Democratic in recent presidential voting, while **North Carolina** statewide is competitive. Growth politics matter.",
        "must_visit": [
            {
                "name": "North Carolina State Capitol area",
                "why": "A direct read on state government, downtown redevelopment, museums, public memory, and civic space.",
                "image_url": "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=900&q=80",
            },
            {
                "name": "Research Triangle corridor",
                "why": "Useful for understanding universities, tech campuses, commuting, suburban growth, and the knowledge economy.",
                "image_url": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=900&q=80",
            },
        ],
    },
}

DEFAULT_PLACE_GUIDE = {
    "population": "Use Census QuickFacts or ACS tables for city, county, and metro population before you arrive. Compare city population with the surrounding county to understand whether the place is urban core, suburb, resort town, college town, or rural service center.",
    "industries": "Start with hospitals, universities, logistics, tourism, agriculture, energy, manufacturing, military, state government, and retail. The largest employers often explain traffic, restaurants, housing pressure, and who is visible during the day.",
    "sports": "Sports guide: identify the local college team, high-school rivalry, minor-league club, sports bar strip, running trail, and weekend event calendar. These names often reveal regional identity faster than monuments do.",
    "food": "Food guide: name the regional dish, immigrant corridor, best-known diner or market, bakery, barbecue or seafood style, produce stand, and the lunch place workers actually use.",
    "politics": "Use county-level presidential results, state election returns, local newspapers, and civic institutions as a starting baseline. Avoid treating one yard sign or one conversation as the whole place.",
    "must_visit": [
        {
            "name": "Downtown or courthouse square",
            "why": "Usually the fastest way to read local government, older commerce, empty storefronts, new investment, and public memory.",
            "image_url": "https://images.unsplash.com/photo-1524661135-423995f22d0b?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Main market, riverfront, campus, or transit hub",
            "why": "These places reveal the everyday economy: who moves through, what is sold, what is advertised, and what has recently changed.",
            "image_url": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=900&q=80",
        },
    ],
}

PLACE_GUIDE_DETAILS = {
    "Boston": {
        "history": "**Freedom Trail**, **Old North Church**, **Faneuil Hall**, **Beacon Hill**, and the **Black Heritage Trail** make the city readable as revolution, abolition, immigration, universities, and medicine layered into one compact core.",
        "culture": "Names to know before arrival: **Harvard**, **MIT**, **Mass General Brigham**, **Fenway Park**, **MBTA/T**, **North End**, **South Boston**, **Cambridge**, and **Dorchester**.",
        "community": "For neighborhood texture, compare **North End** Italian food tourism, **Chinatown**, **Roxbury** Black Boston history, **Cambridge/Somerville** student and tech life, and **Seaport** redevelopment.",
        "nature": "**Boston Harbor**, the **Charles River Esplanade**, **Boston Common**, and the **Emerald Necklace** explain why the city feels maritime, walkable, and park-threaded.",
        "music": "**Boston Symphony Orchestra**, **Berklee College of Music**, Irish pub sessions, college radio, and Fenway concert nights are the useful music anchors.",
        "institutions": "**Boston Public Library**, **Museum of Fine Arts**, **Isabella Stewart Gardner Museum**, **Harvard**, **MIT**, **Massachusetts State House**, and **Fenway Park** are the first institution map.",
    },
    "New Orleans": {
        "history": "**French Quarter**, **Treme**, **Congo Square**, **St. Louis Cathedral**, **Garden District**, and **Lower Ninth Ward** frame the city through colonial rule, Black culture, water, music, and disaster recovery.",
        "culture": "Names to know: **Mardi Gras**, **second line**, **brass band**, **Mardi Gras Indians**, **Creole**, **Cajun**, **shotgun house**, **levee**, and **neutral ground**.",
        "community": "**Treme**, **Bywater**, **Marigny**, **Central City**, **Uptown**, and **Algiers** give a better read than staying only on **Bourbon Street**.",
        "nature": "**Mississippi River**, **Lake Pontchartrain**, levees, pumps, bayous, humidity, and hurricane memory are not background; they are the operating system.",
        "music": "**Preservation Hall**, **Tipitina's**, **Frenchmen Street**, brass bands, bounce, gospel, and jazz funerals are core to the guidebook.",
        "institutions": "**Preservation Hall**, **Backstreet Cultural Museum**, **New Orleans Jazz Museum**, **Cafe du Monde**, **Commander's Palace**, **Superdome**, and the **Port of New Orleans** are anchor points.",
    },
    "Chicago": {
        "history": "**Chicago River**, **Pullman**, **Haymarket**, **Great Migration**, **Union Stock Yards**, and **Chicago Architecture Center** explain labor, race, rail, food, and skyscrapers.",
        "culture": "Names to know: **L train**, **Loop**, **South Side**, **North Side**, **Lake Michigan**, **Wrigley Field**, **Guaranteed Rate Field**, **Second City**, and **blues**.",
        "community": "Compare **Pilsen**, **Bronzeville**, **Hyde Park**, **Wicker Park**, **Chinatown**, and **West Loop** to see migration, universities, art, food, and redevelopment pressure.",
        "nature": "**Lake Michigan**, the **Chicago Riverwalk**, **Lincoln Park**, and the lakefront trail make water and public space central to the city.",
        "music": "**Chicago blues**, **house music**, **gospel**, **Second City**, **Green Mill**, and summer festivals are the core sound map.",
        "institutions": "**Art Institute of Chicago**, **Field Museum**, **University of Chicago**, **Navy Pier**, **Wrigley Field**, **Chicago Board of Trade**, and **Union Station** are anchor points.",
    },
}

DEFAULT_GUIDE_DETAILS = {
    "history": "Start with the main museum, courthouse square, oldest neighborhood, rail or river corridor, and one local history site. These usually reveal settlement, labor, migration, and public memory.",
    "culture": "Build a name map before arrival: local college, hospital system, newspaper, sports team, signature festival, best-known dish, and main street or waterfront.",
    "community": "Compare downtown, one older residential neighborhood, one newer growth corridor, and one everyday shopping street. That gives a clearer guidebook read than a single attraction.",
    "nature": "Use the river, ridge, coast, prairie, desert edge, lake, or weather pattern as a guidebook chapter; it usually explains settlement and recreation.",
    "music": "Look up the best-known venue, festival, college radio station, church music tradition, and bar or dance scene before arrival.",
    "institutions": "Anchor the visit with the public library, courthouse or city hall, main museum, college or hospital, sports field, market, and transit hub.",
}

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
    "food": ["food", "meal", "diner", "coffee", "market", "restaurant", "bread", "farmers", "breakfast"],
    "people": ["people", "conversation", "met", "neighbor", "vendor", "friend", "host", "family", "local"],
    "culture": ["music", "church", "festival", "museum", "ritual", "accent", "school", "sign", "tradition"],
    "economy": ["industry", "work", "job", "housing", "price", "warehouse", "factory", "tourism", "labor"],
    "politics/news": ["election", "policy", "mayor", "county", "news", "politic", "protest", "government"],
    "personal reflection": ["felt", "wondered", "realized", "miss", "remember", "lonely", "surprised", "thought"],
    "nature": ["river", "mountain", "forest", "trail", "weather", "soil", "rain", "field", "landscape"],
    "logistics": ["train", "bus", "station", "road", "motel", "drive", "parking", "airport", "route"],
    "travel": ["arrived", "road", "trip", "walk", "visited", "drive", "downtown", "stop", "journey"],
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


def classify_note_theme(text: str, tags: str = "", mood: str = "") -> str:
    """Deterministic placeholder classifier for the movement-based second brain."""
    haystack = f"{text or ''} {tags or ''} {mood or ''}".lower()
    scores = {theme: 0 for theme in NOTE_THEMES}
    for theme, keywords in THEME_KEYWORDS.items():
        scores[theme] += sum(1 for keyword in keywords if keyword in haystack)
    best_theme, best_score = max(scores.items(), key=lambda item: item[1])
    return best_theme if best_score else "personal reflection"


def generate_public_ready_summary(text: str, location: str, theme: str) -> str:
    seed = _first_sentence(text, "This note records a small observation from movement through place.")
    place = location or "a U.S. place"
    return (
        f"An anonymous {theme} field note from {place}: {seed} "
        "Exact timing, private names, and sensitive details should be reviewed before publication."
    )


def geocode_destination(destination: str, state: str = "") -> dict:
    cleaned_lookup = re.sub(r"\s+", " ", (destination or "").strip()).lower()
    for item in CURATED_US_DESTINATIONS:
        if cleaned_lookup in {item["destination"].lower(), f'{item["destination"].lower()}, {item["state"].lower()}'}:
            return {
                "display_name": f'{item["destination"]}, {item["state"]}, United States',
                "latitude": item["latitude"],
                "longitude": item["longitude"],
                "city": item["destination"],
                "state": item["state"],
                "source_url": "curated:waymark-us",
            }
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
    suggestions: list[dict] = []
    seen = set()
    seen_names = set()
    for item in CURATED_US_DESTINATIONS:
        haystack = f'{item["destination"]} {item["state"]}'.lower()
        if cleaned.lower() in haystack or item["destination"].lower().startswith(cleaned.lower()):
            label = f'{item["destination"]} - {item["state"]} | {item["kind"]}'
            suggestions.append(
                {
                    "label": label,
                    "destination": item["destination"],
                    "state": item["state"],
                    "display_name": f'{item["destination"]}, {item["state"]}, United States',
                    "latitude": item["latitude"],
                    "longitude": item["longitude"],
                    "source_url": "curated:waymark-us",
                }
            )
            seen.add((item["destination"], item["state"], round(item["latitude"], 3), round(item["longitude"], 3)))
            seen_names.add((item["destination"].lower(), item["state"].lower()))
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
        return suggestions

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
        raw_class = result.get("class") or ""
        raw_type = result.get("type") or ""
        place_type = raw_type or raw_class or "place"
        name_state_key = (str(name).lower(), str(state).lower())
        if raw_class == "boundary" and raw_type == "administrative" and name_state_key in seen_names:
            continue
        if address.get("city") or address.get("town") or address.get("village") or raw_type in {"city", "town", "village", "hamlet"}:
            place_type = "city"
        elif raw_class in {"leisure", "tourism"} or "park" in place_type:
            place_type = "park / landmark"
        elif raw_class == "boundary" and raw_type == "administrative":
            place_type = "region"
        key = (name, state, round(float(result.get("lat", 0)), 3), round(float(result.get("lon", 0)), 3))
        if key in seen or (place_type == "region" and name_state_key in seen_names):
            continue
        seen.add(key)
        seen_names.add(name_state_key)
        label = " - ".join(part for part in [name, state] if part)
        if place_type:
            label = f"{label} | {place_type}"
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
    guide = CURATED_PLACE_GUIDES.get(corrected_destination, DEFAULT_PLACE_GUIDE)
    guide_details = {**DEFAULT_GUIDE_DETAILS, **PLACE_GUIDE_DETAILS.get(corrected_destination, {})}
    interest_text = ", ".join(interests) if interests else "history, food, economy, and everyday life"
    interest_lenses = [
        f"{interest}: {INTEREST_PROMPTS[interest]}"
        for interest in interests
        if interest in INTEREST_PROMPTS
    ]
    source_notes = " ".join(item.get("extract", "") for item in summaries[:3])
    if not source_notes:
        source_notes = f"{place} should be approached through public institutions, roads, foodways, work routines, and local memory."
    image_url = next((item.get("image_url") for item in summaries if item.get("image_url")), "")
    sources = build_source_list(
        summaries,
        [
            {"name": "OpenStreetMap Nominatim", "source_url": "https://nominatim.openstreetmap.org/"},
            {"name": "U.S. Census Bureau QuickFacts", "source_url": "https://www.census.gov/quickfacts/"},
            {"name": "MIT Election Data and Science Lab", "source_url": "https://electionlab.mit.edu/data"},
            {"name": "Federal Highway Administration", "source_url": "https://www.fhwa.dot.gov/programadmin/interstate.cfm"},
        ],
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
            f"**{place or 'This destination'}** guidebook: start with population scale, dominant industries, named sports teams, signature food, political baseline, and the must-visit places below."
        ),
        "population_snapshot": guide["population"],
        "industry_snapshot": guide["industries"],
        "sports_snapshot": guide["sports"],
        "food_snapshot": guide["food"],
        "politics_snapshot": guide["politics"],
        "must_visit": guide["must_visit"],
        "historical_background": (
            f"{guide_details['history']} Reference snapshot: {source_notes[:650]}"
        ),
        "cultural_signals": (
            guide_details["culture"]
        ),
        "community_lens": (
            guide_details["community"]
        ),
        "economy_lens": (
            f"Economy guide: {guide['industries']} For a quick read, connect the largest employers with commute patterns, lunch spots, housing prices, and who fills downtown during weekdays."
        ),
        "agriculture_lens": (
            f"Food-system guide: use farmers markets, regional produce, seafood or meat supply chains, farm stands, wholesale markets, and restaurant menus to connect **{place or 'the area'}** to nearby land and labor."
        ),
        "nature_lens": (
            guide_details["nature"]
        ),
        "music_lens": (
            guide_details["music"]
        ),
        "local_food": (
            guide["food"]
        ),
        "local_institutions": (
            guide_details["institutions"]
        ),
        "questions_to_ask": (
            f"Guidebook questions for **{place or 'this place'}**: What changed after the last decade of growth or decline? Which neighborhood should a first-time visitor not skip? Which food is locally loved, not just marketed? Which employer or school quietly shapes daily life?"
        ),
        "field_note_prompts": (
            "Suggested field-note set: one named dish, one team or school logo, one major employer, one local institution, one neighborhood contrast, one transit or highway detail, and one phrase locals use. "
            + ("Selected lenses: " + "; ".join(interest_lenses) if interest_lenses else "")
        ),
        "safety_etiquette": (
            "Do not record private conversations without permission. Avoid real-time posting. Ask before photographing people, homes, farms, or workplaces."
        ),
    }


# Future hook: replace deterministic templates with OpenAI API calls once credentials and model policy are configured.
# Future hook: add Whisper or another transcription pipeline for uploaded audio.
