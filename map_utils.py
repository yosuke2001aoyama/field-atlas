from __future__ import annotations

import pandas as pd


CATEGORY_COLORS = {
    "food": [214, 96, 77],
    "farm": [35, 139, 69],
    "small town": [128, 125, 186],
    "road": [67, 147, 195],
    "motel": [241, 163, 64],
    "church": [166, 97, 26],
    "conversation": [118, 42, 131],
    "landscape": [27, 120, 55],
    "museum": [1, 102, 94],
    "music": [208, 28, 139],
    "neighborhood": [53, 151, 143],
    "farmstay": [26, 150, 65],
    "other": [100, 100, 100],
}


def build_map_points(field_notes: pd.DataFrame, farmstay_logs: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    frames = []

    if not field_notes.empty:
        frames.append(
            pd.DataFrame(
                {
                    "source": "Field note",
                    "source_id": field_notes["id"].astype(str),
                    "title": field_notes["title"],
                    "location": field_notes["location_name"],
                    "category": field_notes["category"],
                    "latitude": field_notes["latitude"],
                    "longitude": field_notes["longitude"],
                    "summary": field_notes["ai_summary"],
                }
            )
        )

    if not farmstay_logs.empty:
        frames.append(
            pd.DataFrame(
                {
                    "source": "Farmstay log",
                    "source_id": farmstay_logs["id"].astype(str),
                    "title": farmstay_logs["farm_name"].fillna("Farmstay"),
                    "location": farmstay_logs["location_name"],
                    "category": farmstay_logs["farm_type"].fillna("farmstay"),
                    "latitude": farmstay_logs["latitude"],
                    "longitude": farmstay_logs["longitude"],
                    "summary": farmstay_logs["ai_summary"],
                }
            )
        )

    if not frames:
        return pd.DataFrame(), pd.DataFrame()

    points = pd.concat(frames, ignore_index=True)
    points["latitude"] = pd.to_numeric(points["latitude"], errors="coerce")
    points["longitude"] = pd.to_numeric(points["longitude"], errors="coerce")
    mapped = points.dropna(subset=["latitude", "longitude"]).copy()
    needs_location = points[points["latitude"].isna() | points["longitude"].isna()].copy()
    mapped["color"] = mapped["category"].map(lambda value: CATEGORY_COLORS.get(str(value).lower(), CATEGORY_COLORS["other"]))
    return mapped, needs_location
