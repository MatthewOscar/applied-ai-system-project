# Model Card: VibeFinder 2.0

## 1. Model Name

**VibeFinder 2.0** (extended from VibeFinder 1.0, Module 3)

---

## 2. Intended Use

A content-based music recommender with RAG-powered explanations. Suggests 3-5 songs from a 30-song catalog based on genre, mood, energy, and acoustic preferences. Designed as a classroom project demonstrating end-to-end AI system integration, not for production use.

---

## 3. How It Works

The system scores each song against a user profile using weighted matching:
- Genre match: +2.0 points (exact match)
- Mood match: +1.0 points (exact match)
- Energy similarity: up to +1.0 points (continuous, based on how close the song's energy is to the user's target)
- Acoustic bonus: +0.5 points (if user likes acoustic and song acousticness > 0.7)

Songs are ranked by total score. Each recommendation also receives a confidence score (0-1) measuring how many dimensions matched well. In AI-Enhanced mode, the system retrieves additional context about each song from a knowledge base (descriptions, similar artists, vibes) and sends it to Google Gemini to generate a natural-language explanation.

---

## 4. Data

- **30 songs** in `data/songs.csv` (expanded from 10 in VibeFinder 1.0)
- **13 genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, edm, country, classical, metal, folk, electronic, hip-hop
- **12 moods represented:** happy, chill, intense, focused, moody, relaxed, romantic, euphoric, nostalgic, melancholy, aggressive
- **Knowledge base:** 30 entries in `data/song_knowledge.json` with descriptions, similar artists, best-for contexts, and vibe tags

---

## 5. Strengths

- Transparent and explainable: every recommendation comes with a score breakdown and confidence level
- RAG explanations are grounded in the knowledge base, reducing hallucination risk
- Works with or without an API key (graceful fallback to static explanations)
- Broader genre coverage than VibeFinder 1.0 (13 genres vs 7)
- Evaluation harness provides automated quality assurance

---

## 6. Limitations and Bias

- 30-song catalog is still small compared to real music services
- Exact genre matching only ("indie pop" does not match "pop")
- Genre weight (2.0) dominates scoring -- a genre match outweighs all other factors combined
- Knowledge base descriptions are hand-written and may not capture all listening contexts
- No user history, collaborative filtering, or personalization beyond the stated profile
- Gemini explanations add latency and API cost (mitigated by using Flash model)

---

## 7. Evaluation

**Unit tests:** 9 tests passing
- Recommender sorting and explanation generation (2 original tests)
- Confidence scoring: perfect match, no match, bounded values (3 tests)
- RAG: knowledge base loading, context retrieval, prompt construction (4 tests)

**Evaluation harness:** 60/60 checks passing
- Consistency: identical inputs always produce identical rankings (5/5)
- Score distribution: scores are meaningfully spread, not degenerate (5/5)
- Confidence calibration: top recommendations have higher confidence than lower ones (5/5)
- Explanation quality: all explanations are non-empty and include scoring info (15/15)
- Knowledge base coverage: every song has a knowledge base entry (30/30)

**Key finding:** Confidence scores correlate well with recommendation quality. Songs matching on genre + mood + energy receive High confidence (0.75+), while partial matches receive Medium (0.45-0.75). The "Edge Case: No Match" profile (metal/angry) correctly shows Low confidence across all results, signaling the system knows it lacks good options.

---

## 8. Future Work

- Genre similarity scoring (partial credit for related genres like "indie pop" and "pop")
- Collaborative filtering using user listening history
- Artist diversity constraint to avoid recommending the same artist multiple times
- Larger catalog with real song metadata (e.g., from Spotify API)
- A/B testing RAG explanations against static explanations for user preference

---

## 9. Reflection on AI Collaboration

During development, AI (Claude Code) was used extensively for:
- Designing the system architecture and planning the RAG integration
- Generating the expanded song catalog and knowledge base entries
- Writing boilerplate code for the evaluation harness and tests

**Helpful AI suggestion:** Claude suggested implementing graceful fallback in the RAG explainer so the system works without an API key. This was valuable because it ensures the project is reproducible for anyone reviewing it, regardless of whether they have a Gemini API key.

**Flawed AI suggestion:** Initially, Claude recommended using the `anthropic` SDK (Claude API) for the RAG feature. However, this wasn't compatible with the course's existing Gemini setup and would have required a paid API key. Switching to the `google-genai` SDK aligned better with the Module 4 DocuBot pattern the course already uses.

**What surprised me:** The confidence scoring revealed that the recommender can rank a song highly (#1) while still having only Medium confidence -- this happens when a song wins on genre match alone but doesn't align on mood or energy. This gap between ranking and confidence is a useful signal for users.

**System limitations:** The biggest limitation is exact genre matching. A user who likes "pop" gets no credit for "indie pop" songs, even though they're closely related. Real recommender systems use embedding-based similarity rather than exact string matching. The 30-song catalog, while improved, is still too small to serve diverse tastes well.
