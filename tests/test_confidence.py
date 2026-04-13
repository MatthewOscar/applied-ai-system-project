"""Tests for the confidence scoring module."""

from src.confidence import confidence_score, confidence_label


def test_perfect_match_high_confidence():
    """A song matching all user preferences should have high confidence."""
    song = {"genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.2}
    user = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    score = confidence_score(song, user)
    assert score >= 0.75
    assert confidence_label(score) == "High"


def test_no_match_low_confidence():
    """A song matching nothing should have low confidence."""
    song = {"genre": "rock", "mood": "intense", "energy": 0.9, "acousticness": 0.1}
    user = {"genre": "jazz", "mood": "relaxed", "energy": 0.3, "likes_acoustic": True}
    score = confidence_score(song, user)
    assert score < 0.45
    assert confidence_label(score) == "Low"


def test_confidence_bounded():
    """Confidence must always be between 0.0 and 1.0."""
    song = {"genre": "pop", "mood": "happy", "energy": 0.5, "acousticness": 0.9}
    user = {"genre": "pop", "mood": "happy", "energy": 0.5, "likes_acoustic": True}
    score = confidence_score(song, user)
    assert 0.0 <= score <= 1.0
