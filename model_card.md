# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**SongMatch** 

---

## 2. Intended Use  

The recommender is designed for users looking for new songs to listen to. This recommender generates a ranking of songs from a small song catalog based on the user's preferred genre, mood, and target energy. It assumes that the user can accurately describe their preferences with specific fields and that matching labels are significant indicators of a good song recommendation. This project is more for classroom exploration since it still lacks features and data to be useful for real users.

---

## 3. How the Model Works  

The model takes a song's genre, mood, and energy, then compares it against the user's preferred genre, preferred mood, and target energy. Matching genre and mood increases the song's score. If the song's energy is closer to the user's target energy, then similarity points are added to the song's score. Finally, songs are ranked from highest to lowest. From the starter logic, I implemented the scoring logic, explanation for a song's ranking, and a deterministic tie-break logic.

---

## 4. Data  

The dataset is a songs.csv file with 18 songs. The songs represent genres like pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, hip hop, metal, reggae, country, blues, house, and k-pop. The songs represent moods like happy, chill, intense, relaxed, focused, moody, melancholic, confident, aggressive, sunny, nostalgic, soulful, euphoric, and romantic. I did not remove any songs, but I did add 8 diverse songs to the original 10. The dataset is still missing songs of different language, culture, genre, mood, and more.

---

## 5. Strengths  

My recommendation system works well for users with simple and clear genre/mood preferences with a common energy target. The scoring captures simple patterns well such as matching genre and mood, and songs closer to the target energy. The cases where the recommendations matched my intuition were the Happy/Pop users getting energetic pop songs and Chill Lofi users getting lower-energy lofi songs. My intuition also matched recommendations for users with mood and genre preferences not included in the dataset; they were recommended songs with similar energy level instead.

---

## 6. Limitations and Bias  

The music recommender system relies on exact matches for genre and mood labels. For example, if a user enters a mood like sad but the catalog has melancholic, the system treats them as unrelated and gives no mood match points. Next, genre is weighted more heavily than mood, so the model can overfit to genre even when mood or other features might be better recommendations for the user. Also, the system currently ignores some user preference features, such as acoustic preference. Finally, the song catalog is small and uneven across genres/moods, so users with preferences in underrepresented categories receive fewer accurate options.

---

## 7. Evaluation  

I tested the recommender system by running the baseline Happy/Pop profile and also comparing multiple edge-case profile pairs. For each run, I looked at the top songs, score explanations, and repeated patterns.

I specifically tested these profile pairs as edge cases: out_of_range_high_energy vs out_of_range_negative_energy, missing_core_preferences vs empty_string_preferences, conflicting_primary_vs_fallback_keys vs fallback_only_keys, contradictory_mood_vs_energy vs likes_acoustic_but_ignored, and lofi_chill_tie_probe vs nonexistent_taxonomy.

I looked for whether recommendations made sense for different users. For example, users with high-energy preferences would often get Gym Hero and Storm Runner because those songs have very high energy numbers in the songs.csv catalog. If recommendations did not make sense, the reason was usually not enough diverse songs in the songs.csv catalog or a logic issue.

I was surprised by how the same songs were ranked very high across different user profiles. It helped me realize that the current scoring algorithm forms filter bubbles, especially since genre and energy have signfiicant impact on rankings, especially when profile preferences are incomplete or niche.

---

## 8. Future Work  

I would add more songs to the songs.csv dataset to support more niche user preferences. I would also add more user features to the preferences and the scoring algorithm such as acousticness, language preference, etc. I would improve explanations by showing which preference contributed most to the score. I would also add a diversity rule to prevent the rankings from being dominated by one genre or artist. To support more complex user tastes, I would allow weighted preferences and mixed-mood listening logic.

---

## 9. Personal Reflection  

I learned that recommender systems are more simple than I previously thought. The user provides preferences which the system scores each song based on. Then the ranked songs are returned for the user. I found the scoring algorithm creation very interesting since the rankings changed a lot depending on which factors were weighted differently. I now know that music recommendation apps are more simple than I thought, but still have much more versatility and complexity than my simple recommendation system.
