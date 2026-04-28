# 🎵 Music Recommender Simulation

## Title & Summary

**SongMatch** is a content-based music recommendation system that helps users discover songs from a catalog by matching their preferences. Given a user's favorite genre, mood, and target energy level, the system scores and ranks songs to provide personalized recommendations. This project demonstrates core concepts in recommendation algorithms, preference modeling, and handling edge cases in AI systems.

## Original Project

This project evolved from the **Module 3 Show: Music Recommender Simulation** project that introduced the foundational recommendation algorithm. The original system implemented basic genre and mood matching with energy-based scoring. Previously, the algorithm prioritized genre and mood matches with partial score for energy similarity while ignoring other user preferences. In this version, I've enhanced the system with reliability checks, adversarial profile testing, guardrails for invalid data, and a deterministic tie-breaking mechanism to ensure consistent, explainable recommendations.

## Architecture Overview

The system operates through three main stages:

1. **Data Loading**: Songs are loaded from a CSV file containing metadata (title, artist, genre, mood, energy level, etc.)
2. **Scoring Engine**: Each song is scored based on three criteria:
   - **Genre Match**: +2 points if the song's genre matches the user's preferred genre
   - **Mood Match**: +1 point if the song's mood matches the user's preferred mood
   - **Energy Similarity**: Up to +2 points based on how close the song's energy is to the user's target energy
   - **Total Score Range**: 0.0 (no match) to 5.0 (perfect match)
3. **Ranking & Recommendation**: Songs are sorted by score (highest first), with deterministic tie-breaking by energy distance and alphabetical title order. The top N recommendations are returned with explanations.

The system includes built-in validation to detect and log issues with invalid preferences or missing song data, ensuring robust handling of edge cases.

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps to Run

1. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the recommender**:
   ```bash
   python src/main.py
   ```
   
   Or test with adversarial profiles:
   ```bash
   python src/main.py --adversarial
   ```
   
   Or run reliability checks:
   ```bash
   python src/main.py --evaluate
   ```
4. **Running Tests**
  Run the starter tests with:

  ```bash
  python -m pytest
  ```

  More tests can be added in `tests/test_recommender.py`. The current test suite covers ranking, fallback preference handling, invalid song skipping, and the reliability evaluation helper.

### Logging

The CLI and recommender use Python logging to report when songs are loaded, profiles are validated, and guardrails skip bad records. This helps reproduce runs and debug failures without changing the main recommendation output.

---
## Sample Interactions

**Example 1: baseline happy pop profile**

Input: {"genre": "pop", "mood": "happy", "energy": 0.8}
Output: Sunrise City - Score: 3.36
Because: genre match (+2.0); mood match (+1.0); energy similarity (+0.36)

Gym Hero - Score: 2.14
Because: genre match (+2.0); energy similarity (+0.14)

Velvet Nocturne - Score: 1.56
Because: energy similarity (+1.56)

**Example 2: out-of-range high energy profile**

Input: {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 100.0}
Output: Sunrise City - Score: 3.00
Because: genre match (+2.0); mood match (+1.0); energy similarity (+0.00)

Gym Hero - Score: 2.00
Because: genre match (+2.0); energy similarity (+0.00)

Rooftop Lights - Score: 1.00
Because: mood match (+1.0); energy similarity (+0.00)

**Example 3: lofi chill tie probe**

Input: {"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.385}
Output: Midnight Coding - Score: 4.93
Because: genre match (+2.0); mood match (+1.0); energy similarity (+1.93)

Library Rain - Score: 4.93
Because: genre match (+2.0); mood match (+1.0); energy similarity (+1.93)

Focus Flow - Score: 3.97
Because: genre match (+2.0); energy similarity (+1.97)

## Design Decisions

**Algorithm Simplicity**: I chose a straightforward weighted-scoring approach rather than complex collaborative filtering. This prioritizes transparency and explainability since each recommendation comes with a clear explanation of why it was chosen. By using fewer preferences in the scoring algorithm, the explanations are easy to explain and debug.

**Exact Matching for Categories**: Genre and mood use exact text matching. While this can miss related terms (e.g., "sad" vs. "melancholic"), it provides deterministic, predictable behavior. The system will need to be improved to account for related terms using natural language processing or a larger genre/mood word bank.

**Genre-Weighted Over Mood**: The algorithm assigns +2 points for genre matches but only +1 for mood matches. This reflects my assumption that genre is the primary driver of music preference. However, this creates a bias where energetic pop songs may rank highly even when mood preferences don't align.

**Energy as Numeric Similarity**: Unlike categorical features, energy is treated as a continuous numerical value with similarity scoring. This allows flexibility for users with non-standard energy targets and handles out-of-range inputs correctly.

**Trade-offs**:
- **Clarity vs. Accuracy**: The simple algorithm is easy to understand and debug, but it may not capture complex user preferences or discover unexpected recommendations.
- **Exact Matching vs. Fuzzy Matching**: Exact matching is deterministic but brittle; fuzzy matching would be more forgiving but harder to explain and debug.
- **Small Dataset**: The 18-song catalog is sufficient for testing but creates filter bubbles where the same songs appear across many profiles. The catalog should be extended for better results across a variety of users.

## Testing Summary

I validated the recommender with automated tests and runtime checks. All pytest tests passed: 8 out of 8. The test suite covers ranking order, explanation output, fallback preference handling, invalid song skipping, tie-breaking, and the reliability check helper.

In addition to pytest, the code uses logging and error handling to make failures observable. It logs when songs are loaded, warns when target_energy is outside the expected range, records skipped invalid song records, and reports reliability check failures instead of silently ignoring them. This gave me a simple but real way to measure whether the AI was behaving consistently and to trace why a bad input or record failed.

Additionally, I validated the system using 10 adversarial user profiles that test edge cases:

**What Worked:**
- The Happy/Pop baseline profile produced intuitive recommendations (energetic pop songs).
- Chill/Lofi profiles correctly returned lower-energy songs.
- The scoring algorithm properly handled extreme energy values (e.g., 100.0, -5.0) by clamping similarity scores.
- Tie-breaking rules ensured deterministic output across multiple runs.

**What Didn't:**
- The acoustic preference feature was implemented but doesn't affect the scoring algorithm, so recommendations don't change when users indicate acoustic preference.
- Profiles with missing core preferences (e.g., only specifying acoustic preference) fell back to energy-only ranking, producing generic results.
- The small song catalog created filter bubbles—the same high-energy pop songs dominated recommendations across different profiles.

**What I Learned:**
The system exhibits a clear trade-off between simplicity and expressiveness. The exact-match approach works well for users with common preferences that align with existing song labels, but fails to provide meaningful recommendations for users with niche or unrepresented preferences. This shows how recommendation systems can create filter bubbles and reinforce existing biases in their training data. To improve the system, the song catalog should be extended with a more diverse selection of songs to support a diverse array of users. Additionally, related moods and genres should be accounted for (e.g., sad vs. melancholy).



## Reflection

This project taught me about how to implement recommender systems efficiently. At its core, they're about matching user preferences to items using a scoring algorithm. However, the system can run into potential drawbacks such as:

- **Bias**: Simple algorithms have assumptions (e.g., my algorithm has genre > mood). Being aware of these biases is very important.
- **Dataset Size & Quality**: The quality and diversity of the song catalog directly limits the quality of recommendations. A small or biased dataset leads to poor performance for users with uncommon preferences. A larger, more diverse dataset will support a diverse range of user preferences and have accurate songs to recommend for almost all users.
- **Explanations**: Providing clear explanations of why a song was recommended makes the system more trustworthy and helps users understand the algorithm's reasoning. It also helps the developer with debugging as a bonus.
- **Edge Cases**: Testing with adversarial user profiles exposed weaknesses I hadn't anticipated, highlighting the importance of robust input validation and testing. Without these edge cases, I would not identify areas of improvement and issues with the current system.

This project has given me a foundation for understanding how recommendation systems balance simplicity, accuracy, and fairness. Going forward, I'd prioritize expanding the dataset, adding fuzzy/similarity matching for genres/moods, and implementing user feedback mechanisms to improve recommendations over time.

## Demo Video

[Watch the project demo](https://drive.google.com/file/d/1jhUG4pgAI1tIrRYnAd0J0yIO96Zdau8n/preview)