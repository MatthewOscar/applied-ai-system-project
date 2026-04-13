"""Tests for the RAG explainer module (no API key needed)."""

from src.rag_explainer import load_knowledge_base, retrieve_context, build_explanation_prompt


def test_load_knowledge_base():
    """Knowledge base loads and has 30 entries."""
    kb = load_knowledge_base()
    assert len(kb) == 30


def test_retrieve_context_found():
    """Retrieving context for song_id 1 returns a dict with 'description'."""
    kb = load_knowledge_base()
    ctx = retrieve_context(1, kb)
    assert ctx is not None
    assert "description" in ctx


def test_retrieve_context_not_found():
    """Retrieving context for a nonexistent song_id returns None."""
    kb = load_knowledge_base()
    ctx = retrieve_context(999, kb)
    assert ctx is None


def test_build_prompt_contains_song_title():
    """The generated prompt should contain the song title."""
    prompt = build_explanation_prompt(
        song={"id": 1, "title": "Sunrise City", "artist": "Neon Echo",
              "genre": "pop", "mood": "happy", "energy": 0.82},
        user_prefs={"genre": "pop", "mood": "happy", "energy": 0.8},
        score=3.82,
        confidence=0.87,
        reasons=["Genre match (pop): +2.0"],
        context={
            "description": "An upbeat pop anthem",
            "similar_artists": ["CHVRCHES"],
            "best_for": ["morning"],
            "vibe_tags": ["uplifting"],
        },
    )
    assert "Sunrise City" in prompt
    assert "upbeat pop anthem" in prompt
