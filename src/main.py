"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
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

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "="*50)
    print("🎵 TOP MUSIC RECOMMENDATIONS 🎵")
    print("="*50 + "\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
