"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse
from recommender import load_songs, recommend_songs


ADVERSARIAL_PROFILES = [
    {
        "name": "out_of_range_high_energy",
        "prefs": {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 100.0},
    },
    {
        "name": "out_of_range_negative_energy",
        "prefs": {"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": -5.0},
    },
    {
        "name": "missing_core_preferences",
        "prefs": {"likes_acoustic": True},
    },
    {
        "name": "conflicting_primary_vs_fallback_keys",
        "prefs": {
            "favorite_genre": "pop",
            "genre": "rock",
            "favorite_mood": "happy",
            "mood": "intense",
            "target_energy": 0.5,
            "energy": 0.9,
        },
    },
    {
        "name": "fallback_only_keys",
        "prefs": {"genre": "rock", "mood": "intense", "energy": 0.9},
    },
    {
        "name": "contradictory_mood_vs_energy",
        "prefs": {"favorite_genre": "ambient", "favorite_mood": "sad", "target_energy": 0.9},
    },
    {
        "name": "likes_acoustic_but_ignored",
        "prefs": {
            "favorite_genre": "house",
            "favorite_mood": "euphoric",
            "target_energy": 0.89,
            "likes_acoustic": True,
        },
    },
    {
        "name": "nonexistent_taxonomy",
        "prefs": {"favorite_genre": "vaportrap", "favorite_mood": "transcendental", "target_energy": 0.75},
    },
    {
        "name": "lofi_chill_tie_probe",
        "prefs": {"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.385},
    },
    {
        "name": "empty_string_preferences",
        "prefs": {"favorite_genre": "", "favorite_mood": "", "target_energy": 0.5},
    },
]


def print_recommendations(header: str, recommendations) -> None:
    print("\n" + "=" * 50)
    print(header)
    print("=" * 50 + "\n")
    for song, score, explanation in recommendations:
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


def run_adversarial_profiles(songs, k: int) -> None:
    for profile in ADVERSARIAL_PROFILES:
        prefs = profile["prefs"]
        recommendations = recommend_songs(prefs, songs, k=k)
        print_recommendations(
            f"ADVERSARIAL PROFILE: {profile['name']}",
            recommendations,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the music recommender simulation.")
    parser.add_argument(
        "--adversarial",
        action="store_true",
        help="Run a suite of adversarial/edge-case user profiles.",
    )
    parser.add_argument("--k", type=int, default=5, help="Number of recommendations to return.")
    args = parser.parse_args()

    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    taste_profile = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.45,
        "likes_acoustic": True,
        "target_tempo_bpm": 84,
        "target_danceability": 0.58,
        "genre_weight": 0.35,
        "mood_weight": 0.25,
        "energy_weight": 0.25,
        "acousticness_weight": 0.15,
    }

    if args.adversarial:
        run_adversarial_profiles(songs, k=args.k)
        return

    recommendations = recommend_songs(user_prefs, songs, k=args.k)
    print_recommendations("TOP MUSIC RECOMMENDATIONS", recommendations)


if __name__ == "__main__":
    main()
