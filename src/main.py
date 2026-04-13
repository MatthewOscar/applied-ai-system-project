"""
Command line runner for VibeFinder 2.0 - Music Recommender System.

Supports two modes:
  1) Classic   - Original scoring with static explanations
  2) AI-Enhanced - Confidence scores + RAG-powered Gemini explanations
"""

import os
from dotenv import load_dotenv

from .recommender import load_songs, recommend_songs, score_song
from .confidence import confidence_score, confidence_label
from .rag_explainer import load_knowledge_base, generate_explanation


PROFILES = [
    ("Pop Happy Listener", {"genre": "pop", "mood": "happy", "energy": 0.8}),
    ("Chill Lofi Student", {"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True}),
    ("Intense Rock Fan", {"genre": "rock", "mood": "intense", "energy": 0.9}),
]


def run_classic_mode(songs: list, profiles: list) -> None:
    """Run the original VibeFinder 1.0 recommendations."""
    for name, user_prefs in profiles:
        print(f"\n{'='*50}")
        print(f"Profile: {name}")
        print(f"Preferences: {user_prefs}")
        print(f"{'='*50}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for rank, rec in enumerate(recommendations, 1):
            song, rec_score, explanation = rec
            print(f"  {rank}. {song['title']} by {song['artist']} - Score: {rec_score:.2f}")
            print(f"     Because: {explanation}")
            print()

    # --- Data Experiment: Genre Weight Shift ---
    print("\n" + "=" * 50)
    print("EXPERIMENT: Genre Weight Shift")
    print("Comparing default weights vs reduced genre weight")
    print("=" * 50)

    test_user = {"genre": "pop", "mood": "happy", "energy": 0.8}

    print("\n--- Default weights (genre=2.0, mood=1.0, energy=1.0) ---")
    recs_default = recommend_songs(test_user, songs, k=5)
    for rank, (song, rec_score, _) in enumerate(recs_default, 1):
        print(f"  {rank}. {song['title']}: {rec_score:.2f}")

    low_genre_weights = {"genre": 0.5, "mood": 1.0, "energy": 1.0, "acoustic": 0.5}
    print("\n--- Reduced genre weight (genre=0.5, mood=1.0, energy=1.0) ---")
    recs_experiment = recommend_songs(test_user, songs, k=5, weights=low_genre_weights)
    for rank, (song, rec_score, _) in enumerate(recs_experiment, 1):
        print(f"  {rank}. {song['title']}: {rec_score:.2f}")


def run_ai_enhanced_mode(songs: list, profiles: list, knowledge_base: list) -> None:
    """Run AI-enhanced recommendations with confidence scores and RAG explanations."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("  [Note: GEMINI_API_KEY not set. Using static explanations as fallback.]\n")

    for name, user_prefs in profiles:
        print(f"\n{'='*50}")
        print(f"Profile: {name}")
        print(f"Preferences: {user_prefs}")
        print(f"{'='*50}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for rank, rec in enumerate(recommendations, 1):
            song, rec_score, explanation = rec
            conf = confidence_score(song, user_prefs)
            label = confidence_label(conf)

            print(f"  {rank}. {song['title']} by {song['artist']} - Score: {rec_score:.2f} | Confidence: {label} ({conf:.0%})")

            # Generate RAG-powered explanation
            _, reasons = score_song(user_prefs, song)
            ai_explanation = generate_explanation(
                song, user_prefs, rec_score, conf, reasons, knowledge_base
            )
            print(f"     {ai_explanation}")
            print()


def main() -> None:
    load_dotenv()

    songs = load_songs("data/songs.csv")
    knowledge_base = load_knowledge_base("data/song_knowledge.json")
    print(f"Loaded {len(songs)} songs and {len(knowledge_base)} knowledge base entries.")

    print("\nSelect mode:")
    print("  1) Classic (VibeFinder 1.0)")
    print("  2) AI-Enhanced (confidence + RAG explanations)")
    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "2":
        print("\n--- AI-Enhanced Mode ---")
        run_ai_enhanced_mode(songs, PROFILES, knowledge_base)
    else:
        print("\n--- Classic Mode ---")
        run_classic_mode(songs, PROFILES)


if __name__ == "__main__":
    main()
