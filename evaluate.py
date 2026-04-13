"""
Evaluation harness for VibeFinder 2.0.

Runs multiple user profiles through the system and checks:
1. Consistency: same input always produces same ranking
2. Scoring distribution: are scores reasonably spread or all clustered?
3. Confidence calibration: do high-confidence recs match on more dimensions?
4. Explanation quality: are explanations non-empty and reference the song?

Usage:
    python evaluate.py
"""

from src.recommender import load_songs, recommend_songs, score_song
from src.confidence import confidence_score, confidence_label
from src.rag_explainer import load_knowledge_base, retrieve_context

EVAL_PROFILES = [
    ("Pop Happy Listener", {"genre": "pop", "mood": "happy", "energy": 0.8}),
    ("Chill Lofi Student", {"genre": "lofi", "mood": "chill", "energy": 0.4, "likes_acoustic": True}),
    ("Intense Rock Fan", {"genre": "rock", "mood": "intense", "energy": 0.9}),
    ("Jazz Relaxer", {"genre": "jazz", "mood": "relaxed", "energy": 0.3, "likes_acoustic": True}),
    ("Edge Case: No Match", {"genre": "metal", "mood": "angry", "energy": 1.0}),
]


def test_consistency(songs):
    """Run each profile twice, verify rankings are identical."""
    passed = 0
    failed = 0
    for name, prefs in EVAL_PROFILES:
        run1 = recommend_songs(prefs, songs, k=5)
        run2 = recommend_songs(prefs, songs, k=5)
        titles1 = [s['title'] for s, _, _ in run1]
        titles2 = [s['title'] for s, _, _ in run2]
        if titles1 == titles2:
            passed += 1
        else:
            failed += 1
            print(f"    FAIL: {name} - rankings differ between runs")
    return {"passed": passed, "failed": failed}


def test_score_distribution(songs):
    """Check that scores are not all identical (degenerate case)."""
    passed = 0
    failed = 0
    for name, prefs in EVAL_PROFILES:
        recs = recommend_songs(prefs, songs, k=5)
        scores = [s for _, s, _ in recs]
        unique_scores = len(set(f"{s:.4f}" for s in scores))
        if unique_scores > 1:
            passed += 1
        else:
            failed += 1
            print(f"    FAIL: {name} - all scores identical ({scores[0]:.2f})")
    return {"passed": passed, "failed": failed}


def test_confidence_calibration(songs):
    """Verify high-confidence songs match on more dimensions than low-confidence ones."""
    passed = 0
    failed = 0
    for name, prefs in EVAL_PROFILES:
        recs = recommend_songs(prefs, songs, k=5)
        confidences = []
        for song, _, _ in recs:
            conf = confidence_score(song, prefs)
            confidences.append(conf)

        # Top recommendation should have >= confidence of last recommendation
        if confidences[0] >= confidences[-1]:
            passed += 1
        else:
            failed += 1
            print(f"    FAIL: {name} - top rec confidence ({confidences[0]:.2f}) < last rec ({confidences[-1]:.2f})")
    return {"passed": passed, "failed": failed}


def test_explanation_quality(songs, knowledge_base):
    """Check that static explanations are non-empty and mention scoring dimensions."""
    passed = 0
    failed = 0
    for name, prefs in EVAL_PROFILES:
        recs = recommend_songs(prefs, songs, k=3)
        for song, rec_score, explanation in recs:
            if not explanation or len(explanation.strip()) == 0:
                failed += 1
                print(f"    FAIL: {name} - empty explanation for {song['title']}")
            elif "Energy similarity" not in explanation:
                failed += 1
                print(f"    FAIL: {name} - explanation missing scoring info for {song['title']}")
            else:
                passed += 1
    return {"passed": passed, "failed": failed}


def test_knowledge_base_coverage(songs, knowledge_base):
    """Verify every song in the catalog has a knowledge base entry."""
    passed = 0
    failed = 0
    for song in songs:
        ctx = retrieve_context(song['id'], knowledge_base)
        if ctx and ctx.get('description'):
            passed += 1
        else:
            failed += 1
            print(f"    FAIL: No knowledge base entry for song {song['id']} ({song['title']})")
    return {"passed": passed, "failed": failed}


def print_eval_report(results):
    """Pretty-print all evaluation results."""
    total_passed = 0
    total_failed = 0

    print("\n" + "=" * 60)
    print("VIBEFINDER 2.0 - EVALUATION REPORT")
    print("=" * 60)

    for test_name, result in results.items():
        p, f = result["passed"], result["failed"]
        total_passed += p
        total_failed += f
        status = "PASS" if f == 0 else "FAIL"
        print(f"\n  [{status}] {test_name}: {p} passed, {f} failed")

    print("\n" + "-" * 60)
    total = total_passed + total_failed
    print(f"  TOTAL: {total_passed}/{total} checks passed")
    if total_failed == 0:
        print("  All checks passed!")
    else:
        print(f"  {total_failed} check(s) failed.")
    print("=" * 60)


if __name__ == "__main__":
    songs = load_songs("data/songs.csv")
    knowledge_base = load_knowledge_base("data/song_knowledge.json")
    print(f"Loaded {len(songs)} songs and {len(knowledge_base)} knowledge base entries.\n")

    results = {}
    print("Running consistency check...")
    results["Consistency"] = test_consistency(songs)
    print("Running score distribution check...")
    results["Score Distribution"] = test_score_distribution(songs)
    print("Running confidence calibration check...")
    results["Confidence Calibration"] = test_confidence_calibration(songs)
    print("Running explanation quality check...")
    results["Explanation Quality"] = test_explanation_quality(songs, knowledge_base)
    print("Running knowledge base coverage check...")
    results["Knowledge Base Coverage"] = test_knowledge_base_coverage(songs, knowledge_base)

    print_eval_report(results)
