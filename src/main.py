"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse
import logging

from recommender import load_songs, recommend_songs, run_reliability_checks


logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


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


def run_evaluation(songs, k: int) -> None:
    results = run_reliability_checks(ADVERSARIAL_PROFILES, songs, k=k)
    passed = sum(1 for result in results if result.get("passed"))
    failed = len(results) - passed

    print("\nEVALUATION SUMMARY")
    print("=" * 50)
    for result in results:
        status = "PASS" if result.get("passed") else "FAIL"
        extra = f" ({result['error']})" if "error" in result else f" [{result.get('count', 0)} recs]"
        print(f"{status}: {result['name']}{extra}")
    print(f"Passed: {passed} | Failed: {failed}")

    if failed:
        logger.warning("Evaluation completed with %s failing profile(s)", failed)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the music recommender simulation.")
    parser.add_argument(
        "--adversarial",
        action="store_true",
        help="Run a suite of adversarial/edge-case user profiles.",
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Run reliability checks against the adversarial profiles.",
    )
    parser.add_argument("--k", type=int, default=5, help="Number of recommendations to return.")
    args = parser.parse_args()

    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs1 = {"genre": "pop", "mood": "happy", "energy": 0.8}
    user_prefs2 = {"genre": "rock", "mood": "angry", "energy": 0.9}
    user_prefs3 = {"genre": "lofi", "mood": "chill", "energy": 0.3}

    if args.adversarial:
        run_adversarial_profiles(songs, k=args.k)
        return

    if args.evaluate:
        run_evaluation(songs, k=args.k)
        return

    recommendations1 = recommend_songs(user_prefs1, songs, k=args.k)
    recommendations2 = recommend_songs(user_prefs2, songs, k=args.k)
    recommendations3 = recommend_songs(user_prefs3, songs, k=args.k)

    print_recommendations("User 1 MUSIC RECOMMENDATIONS", recommendations1)
    print_recommendations("User 2 MUSIC RECOMMENDATIONS", recommendations2)
    print_recommendations("User 3 MUSIC RECOMMENDATIONS", recommendations3)


if __name__ == "__main__":
    main()
