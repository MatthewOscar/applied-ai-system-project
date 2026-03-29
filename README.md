# Music Recommender Simulation

## Project Summary

A content-based music recommender that scores songs against a user taste profile using weighted genre, mood, and energy matching, then returns the top-ranked results with explanations.

---

## How The System Works

- **Song features:** genre, mood, energy (0-1), acousticness (0-1)
- **User profile:** favorite genre, favorite mood, target energy, acoustic preference
- **Scoring:** genre match +2.0, mood match +1.0, energy similarity up to +1.0, acoustic bonus +0.5
- **Ranking:** sort all songs by score descending, return top k

---

## Getting Started

### Setup

1. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest tests/test_recommender.py -v
```

---

## Experiments You Tried

Genre weight shift (2.0 -> 0.5) for Pop Happy user: "Rooftop Lights" (mood match) jumped from #3 to #2, passing "Gym Hero" (genre match only). Confirms genre weight is the dominant ranking factor.

---

## Limitations and Risks

- 10-song catalog, lofi/chill heavy
- Exact genre matching only
- No tempo, valence, or artist diversity in scoring

See [model_card.md](model_card.md) for more detail.

---

## Reflection

See [model_card.md](model_card.md).

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
