"""
RAG-powered explanation generator for VibeFinder 2.0.

Retrieves relevant song context from the knowledge base and uses
the Google Gemini API to generate natural, personalized
recommendation explanations.
"""

import json
import os
from typing import List, Dict, Optional

from .confidence import confidence_label


def load_knowledge_base(path: str = "data/song_knowledge.json") -> List[Dict]:
    """Load the song knowledge base from JSON."""
    with open(path, "r") as f:
        return json.load(f)


def retrieve_context(song_id: int, knowledge_base: List[Dict]) -> Optional[Dict]:
    """Retrieve the knowledge base entry for a given song ID."""
    for entry in knowledge_base:
        if entry["song_id"] == song_id:
            return entry
    return None


def build_explanation_prompt(
    song: dict,
    user_prefs: dict,
    score: float,
    confidence: float,
    reasons: list,
    context: Optional[dict],
) -> str:
    """
    Build the prompt sent to Gemini.

    Includes the user's preferences, song features, score breakdown,
    confidence level, and retrieved knowledge base context.
    """
    context_block = ""
    if context:
        context_block = (
            f"\nAdditional context about this song:\n"
            f"{context.get('description', 'No description available.')}\n"
            f"Similar artists: {', '.join(context.get('similar_artists', []))}\n"
            f"Best for: {', '.join(context.get('best_for', []))}\n"
            f"Vibe: {', '.join(context.get('vibe_tags', []))}\n"
        )

    prompt = f"""You are a music recommendation assistant for VibeFinder. Explain why
this song was recommended for this listener.

User preferences:
- Favorite genre: {user_prefs.get('genre', 'unknown')}
- Favorite mood: {user_prefs.get('mood', 'unknown')}
- Target energy: {user_prefs.get('energy', 0.5)}
- Likes acoustic: {user_prefs.get('likes_acoustic', False)}

Recommended song: "{song.get('title', '')}" by {song.get('artist', '')}
- Genre: {song.get('genre', '')}, Mood: {song.get('mood', '')}, Energy: {song.get('energy', '')}
- Match score: {score:.2f}
- Confidence: {confidence_label(confidence)} ({confidence:.0%})
- Score breakdown: {'; '.join(reasons)}
{context_block}
Write a 2-3 sentence explanation of why this song fits the listener.
Be specific and reference the context provided. Do not invent information
beyond what is given above."""

    return prompt


def generate_explanation(
    song: dict,
    user_prefs: dict,
    score: float,
    confidence: float,
    reasons: list,
    knowledge_base: List[Dict],
) -> str:
    """
    Full RAG pipeline: retrieve context, build prompt, call Gemini API.

    Falls back to static explanation if no API key or on API error.
    """
    # Retrieve context from knowledge base
    context = retrieve_context(song.get("id", -1), knowledge_base)

    # Build prompt
    prompt = build_explanation_prompt(
        song, user_prefs, score, confidence, reasons, context
    )

    # Try Gemini API call
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "; ".join(reasons)

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        text = response.text or ""
        return text.strip() if text.strip() else "; ".join(reasons)
    except Exception:
        return "; ".join(reasons)
