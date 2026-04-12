# 🎵 Music Recommender Simulation

## Project Summary

This project implements a small content-based music recommender that ranks songs from a catalog using user preferences for genre, mood, and target energy. Songs earn points for genre and mood matches, plus similarity points based on how close song energy is to the user's target energy. Then, the system returns top recommendations with short explanations. I also tested multiple edge-case profiles to observe filter-bubble behavior and scoring limitations.

---

## How The System Works

Real-world recommender systems combine collaborative and content-based filtering techniques to rank songs by a score, which measures relevance and interest to the user. My version will prioritize clarity and simplicity. The system should match the user's preferred genre and mood first and then filter based on numeric similarities (like energy and acousticness).

In my system, each Song should use features like id, title, artist, genre, mood, energy, acousticness. Optionally, the system can further filter/refine the recommendations by using valence, tempo_bpm, and danceability.

My UserProfile stores favorite genre, favorite mood, target energy (numeric energy value), and acoustic preferences (like or dislike).

The system adds points for songs that match the user's genre/mood preferences.
The system adds similarity points for numeric features that are close to the user's target (e.g. energy distance). The combined weighted sum is the score for a song.

After scoring every song, sort the songs from highest to lowest score. Return the top 3 songs (or more than 3 if needed). An accompanying explanation of why the song was recommended could be included.

**Algorithm Recipe (Final)**:
  1. Genre match
    - If song genre equals user favorite genre: add 2.0
    - Else: add 0
  2. Mood match
    - If song mood equals user favorite mood: add 1.0
    - Else: add 0
  3. Energy similarity
    - Compute distance: absolute value of (song_energy - user_target_energy)
    - Convert to similarity: 1.0 - distance
    - Clamp to [0, 1] just in case
    - Add energy points: 2.0 × similarity
  Total score:
  Score = GenrePoints + MoodPoints + EnergyPoints

  Range:

  Minimum = 0.0
  Maximum = 5.0
  Normalized version: NormalizedScore = Score / 5.0

  Tie-break rule (recommended)

  If two songs have the same total score, rank the one with smaller energy distance first.
  If still tied, sort alphabetically by title for deterministic output.

**Potential Biases (expected)**
This system might over-prioritize genre since it assigns +2 points for matching genre compared to only +1 for matching mood. Therefore, songs with strong mood and energy scores may still rank lower if the genre does not match.



---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

First, I ran an experiment where I removed mood from the scoring algorithm. The result was that genre dominated the rankings with energy as a secondary factor if genre was not matching. Next, I ran an experiment where I switched the point values for mood and genre (originally genre: +2 and mood +1). The result was that the rankings prioritized mood more instead of genre. I also ran experiment for users that did not have any matching genre or mood to the songs in the dataset. The result was the system prioritized songs with similar energy levels.

---

## Limitations and Risks

The recommender currently only works on a small dataset songs.csv with only 18 songs. Therefore, it cannot support users with various preferences, especially niche preferences. Also, the recommender tends to favor matching genre over matching mood due to the scoring algorithm. Finally, the system does not factor other user preferences like acousticness or tempo_bpm into the scoring algorithm.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

I learned about how recommender systems work. First, the system uses user profiles and preferences as input to the system. Then, the system compares the user preferences against a scoring algorithm and assigs a score to each song/data entry. The scoring algorithm can weight different preferences/factors differently, significantly affecting the rankings/recommendation. Finally, the system outputs a recommendation sorted from higher scores to lower scores. 

These systems could have biases in dataset, scoring, and more. If the dataset is not large and diverse enough, the predictions could be heavily biased toward existing data. This means that users with niche or uncommon preferences will not get good predictions from the system. Additionally, if the scoring system weights certain preferences above others, users might get repetitive predictions. 


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"