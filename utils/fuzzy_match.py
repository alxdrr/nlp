import pandas as pd
from rapidfuzz import process, fuzz

# Membaca data dari CSV hanya sekali saat modul diimpor
try:
    data = pd.read_csv("tracksdata.csv")
    all_tracks = [track.strip().lower() for track in data['track_name'] if isinstance(track, str)]
except Exception as e:
    print("Error loading track data:", e)
    all_tracks = []

def fuzzy_search(query):
    """Mencari lagu yang mirip dengan query menggunakan RapidFuzz."""
    if not query or not all_tracks:
        return []

    matches = process.extract(query, all_tracks, limit=10, scorer=fuzz.partial_token_sort_ratio)
    return [match[0] for match in matches if match[1] >= 80]  # Hanya hasil dengan skor ≥80
