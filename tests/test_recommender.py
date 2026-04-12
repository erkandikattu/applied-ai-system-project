from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_score_song_prefers_favorite_keys_over_fallback_keys():
    song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
        "title": "Preference Clash",
    }

    user_prefs = {
        "favorite_genre": "pop",
        "genre": "rock",
        "favorite_mood": "happy",
        "mood": "intense",
        "target_energy": 0.80,
        "energy": 0.10,
    }

    score, reasons = score_song(user_prefs, song)

    assert score == 5.0
    assert "genre match (+2.0)" in reasons
    assert "mood match (+1.0)" in reasons


def test_score_song_out_of_range_target_energy_collapses_energy_points():
    song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.82,
        "title": "Sunrise City",
    }

    score, reasons = score_song(
        {"favorite_genre": "vaportrap", "favorite_mood": "transcendental", "target_energy": 100.0},
        song,
    )

    assert score == 0.0
    assert "energy similarity (+0.00)" in reasons


def test_recommend_songs_uses_title_for_last_tiebreak():
    songs = [
        {"title": "Zulu", "genre": "x", "mood": "y", "energy": 0.5},
        {"title": "Alpha", "genre": "x", "mood": "y", "energy": 0.5},
    ]
    user_prefs = {"favorite_genre": "none", "favorite_mood": "none", "target_energy": 0.5}

    results = recommend_songs(user_prefs, songs, k=2)

    assert results[0][0]["title"] == "Alpha"
    assert results[1][0]["title"] == "Zulu"
