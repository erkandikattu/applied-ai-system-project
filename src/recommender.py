from typing import List, Dict, Tuple, Iterable
from dataclasses import dataclass
import csv
import logging


logger = logging.getLogger(__name__)


REQUIRED_SONG_FIELDS = {
    "id",
    "title",
    "artist",
    "genre",
    "mood",
    "energy",
    "tempo_bpm",
    "valence",
    "danceability",
    "acousticness",
}

REQUIRED_SCORING_SONG_FIELDS = {"title", "genre", "mood", "energy"}

REQUIRED_USER_FIELDS = {"favorite_genre", "favorite_mood", "target_energy"}

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
        validated_user = validate_user_profile(user)
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(validated_user, song_to_dict(song))[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        validated_user = validate_user_profile(user)
        score, reasons = score_song(validated_user, song_to_dict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)


def song_to_dict(song: Song) -> Dict:
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
    }


def validate_user_profile(user_prefs: Dict | UserProfile) -> Dict:
    if isinstance(user_prefs, UserProfile):
        user_prefs = {
            "favorite_genre": user_prefs.favorite_genre,
            "favorite_mood": user_prefs.favorite_mood,
            "target_energy": user_prefs.target_energy,
            "likes_acoustic": user_prefs.likes_acoustic,
        }

    if not isinstance(user_prefs, dict):
        raise TypeError("user preferences must be a dictionary or UserProfile")

    validated = dict(user_prefs)
    for field in REQUIRED_USER_FIELDS:
        primary_value = validated.get(field)
        fallback_field = field.replace("favorite_", "") if field.startswith("favorite_") else field
        fallback_value = validated.get(fallback_field)
        value = primary_value if primary_value not in (None, "") else fallback_value

        if field == "target_energy":
            if value in (None, ""):
                value = 0.0
            try:
                value = float(value)
            except (TypeError, ValueError) as exc:
                raise ValueError("target_energy must be numeric") from exc
            if value < 0.0 or value > 1.0:
                logger.warning("target_energy is outside the expected [0, 1] range: %s", value)
        elif value in (None, ""):
            value = ""

        validated[field] = value

    return validated


def validate_song_record(song: Dict, strict: bool = False) -> Dict:
    if not isinstance(song, dict):
        raise TypeError("song records must be dictionaries")

    required_fields = REQUIRED_SONG_FIELDS if strict else REQUIRED_SCORING_SONG_FIELDS
    missing_fields = required_fields - song.keys()
    if missing_fields:
        raise ValueError(f"song record is missing required fields: {sorted(missing_fields)}")

    return song

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

    logger.info("Loaded %s songs from %s", len(songs), csv_path)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return reasons."""
    validated_user = validate_user_profile(user_prefs)
    validated_song = validate_song_record(song)

    favorite_genre = validated_user.get("favorite_genre", "")
    favorite_mood = validated_user.get("favorite_mood", "")
    target_energy = float(validated_user.get("target_energy", 0.0))

    score = 0.0
    reasons: List[str] = []

    if validated_song.get("genre") == favorite_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if validated_song.get("mood") == favorite_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    song_energy = float(validated_song.get("energy", 0.0))
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
    validated_user = validate_user_profile(user_prefs)
    logger.info("Generating recommendations for profile=%s", validated_user)

    strict_songs: List[Dict] = []
    relaxed_songs: List[Dict] = []
    for song in songs:
        try:
            strict_songs.append(validate_song_record(song, strict=True))
        except (TypeError, ValueError):
            try:
                relaxed_songs.append(validate_song_record(song))
            except (TypeError, ValueError) as exc:
                logger.warning("Skipping invalid song record: %s", exc)

    songs_to_rank = strict_songs if strict_songs else relaxed_songs

    scored: List[Tuple[Dict, float, str, float]] = []
    for validated_song in songs_to_rank:
        score, reasons = score_song(validated_user, validated_song)
        energy_distance = abs(float(validated_song.get("energy", 0.0)) - float(validated_user.get("target_energy", 0.0)))
        explanation = "; ".join(reasons)
        scored.append((validated_song, score, explanation, energy_distance))

    ranked = sorted(
        scored,
        key=lambda item: (-item[1], item[3], item[0].get("title", "")),
    )

    top_k = ranked[:k]
    return [(song, score, explanation) for song, score, explanation, _ in top_k]


def run_reliability_checks(
    user_profiles: Iterable[Dict],
    songs: List[Dict],
    k: int = 5,
) -> List[Dict]:
    """Run simple pass/fail checks against a set of user profiles."""
    results: List[Dict] = []
    for index, profile in enumerate(user_profiles, start=1):
        name = profile.get("name", f"profile_{index}")
        prefs = profile.get("prefs", {})
        try:
            recommendations_first = recommend_songs(prefs, songs, k=k)
            recommendations_second = recommend_songs(prefs, songs, k=k)

            same_order = [item[0].get("title", "") for item in recommendations_first] == [
                item[0].get("title", "") for item in recommendations_second
            ]
            score_bounds_ok = all(0.0 <= score <= 5.0 for _, score, _ in recommendations_first)
            passed = len(recommendations_first) <= k and same_order and score_bounds_ok

            result = {
                "name": name,
                "passed": passed,
                "count": len(recommendations_first),
                "deterministic": same_order,
                "score_bounds_ok": score_bounds_ok,
            }
            results.append(result)
            if not passed:
                logger.error("Reliability check failed for %s", name)
        except (TypeError, ValueError) as exc:
            logger.exception("Reliability check crashed for %s", name)
            results.append({"name": name, "passed": False, "error": str(exc)})

    return results
