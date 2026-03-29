# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

Classroom simulation that suggests 3-5 songs from a small catalog based on genre, mood, and energy preferences. Not for real users.

---

## 3. How the Model Works

Scores each song against a user profile: +2.0 for genre match, +1.0 for mood match, up to +1.0 for energy closeness, +0.5 acoustic bonus. Songs are sorted by total score and the top results are returned with explanations.

---

## 4. Data

10 songs in `data/songs.csv`. Skewed toward lofi (3) and chill (3). No hip-hop, R&B, country, classical, or EDM represented.

---

## 5. Strengths

Transparent and explainable. Works well for lofi/chill users where the catalog has the most variety. Energy similarity provides nuance between otherwise-equal matches.

---

## 6. Limitations and Bias

- 10-song catalog limits variety, especially for rock/jazz/ambient (1 song each)
- Exact genre matching ("indie pop" != "pop")
- Genre weight dominance confirmed by weight-shift experiment
- No tempo, valence, or artist diversity in scoring

---

## 7. Evaluation

Tested 3 profiles (Pop Happy, Chill Lofi, Intense Rock). Results matched intuition. Genre weight-shift experiment (2.0 -> 0.5) showed mood match overtaking genre-only match in rankings. 2 unit tests passing.

---

## 8. Future Work

- Genre similarity scoring (partial credit for related genres)
- Tempo as a preference
- Artist diversity constraint

---

## 9. Personal Reflection

*TF: skipped per requirements.*
