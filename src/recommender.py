from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dictionaries."""
    songs: List[Dict] = []
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    with open(csv_path, mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            parsed_row: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    parsed_row[key] = int(value)
                elif key in float_fields:
                    parsed_row[key] = float(value)
                else:
                    parsed_row[key] = value.strip() if isinstance(value, str) else value
            songs.append(parsed_row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return reasons."""
    favorite_genre = user_prefs.get("favorite_genre", user_prefs.get("genre", ""))
    favorite_mood = user_prefs.get("favorite_mood", user_prefs.get("mood", ""))
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy", 0.0))

    score = 0.0
    reasons: List[str] = []

    if song.get("genre") == favorite_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song.get("mood") == favorite_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    song_energy = float(song.get("energy", 0.0))
    target_energy = float(target_energy)
    energy_distance = abs(song_energy - target_energy)
    energy_similarity = max(0.0, min(1.0, 1.0 - energy_distance))
    energy_points = 2.0 * energy_similarity
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    if not reasons:
        reasons.append("no preference match")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return top-k song recommendations sorted by computed score."""
    target_energy = float(user_prefs.get("target_energy", user_prefs.get("energy", 0.0)))

    scored: List[Tuple[Dict, float, str, float]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        energy_distance = abs(float(song.get("energy", 0.0)) - target_energy)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation, energy_distance))

    ranked = sorted(
        scored,
        key=lambda item: (-item[1], item[3], item[0].get("title", "")),
    )

    top_k = ranked[:k]
    return [(song, score, explanation) for song, score, explanation, _ in top_k]
