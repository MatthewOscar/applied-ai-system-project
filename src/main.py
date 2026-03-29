"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # --- Three user profiles ---
    profiles = [
        ("Pop Happy Listener", {"genre": "pop", "mood": "happy", "energy": 0.8}),
        ("Chill Lofi Student", {"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True}),
        ("Intense Rock Fan", {"genre": "rock", "mood": "intense", "energy": 0.9}),
    ]

    for name, user_prefs in profiles:
        print(f"\n{'='*50}")
        print(f"Profile: {name}")
        print(f"Preferences: {user_prefs}")
        print(f"{'='*50}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for rank, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            print(f"  {rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
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
    for rank, (song, score, _) in enumerate(recs_default, 1):
        print(f"  {rank}. {song['title']}: {score:.2f}")

    low_genre_weights = {"genre": 0.5, "mood": 1.0, "energy": 1.0, "acoustic": 0.5}
    print("\n--- Reduced genre weight (genre=0.5, mood=1.0, energy=1.0) ---")
    recs_experiment = recommend_songs(test_user, songs, k=5, weights=low_genre_weights)
    for rank, (song, score, _) in enumerate(recs_experiment, 1):
        print(f"  {rank}. {song['title']}: {score:.2f}")


if __name__ == "__main__":
    main()
