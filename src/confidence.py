"""
Confidence scoring for VibeFinder recommendations.

Computes a 0.0-1.0 confidence score based on how many dimensions
the song matches the user profile across. A high score means the
recommendation is well-supported; a low score means the system is
less certain this is a good fit.
"""


def confidence_score(song: dict, user_prefs: dict) -> float:
    """
    Returns a confidence float between 0.0 and 1.0.

    Dimensions checked (weights sum to 1.0):
    - genre match (binary): 0.35
    - mood match (binary): 0.25
    - energy similarity (continuous): 0.25
    - acousticness fit (conditional): 0.15
    """
    score = 0.0

    # Genre match
    if song.get('genre', '').lower() == user_prefs.get('genre', '').lower():
        score += 0.35

    # Mood match
    if song.get('mood', '').lower() == user_prefs.get('mood', '').lower():
        score += 0.25

    # Energy similarity (1.0 when identical, 0.0 when maximally different)
    energy_sim = 1.0 - abs(song.get('energy', 0.5) - user_prefs.get('energy', 0.5))
    score += 0.25 * energy_sim

    # Acoustic fit
    if user_prefs.get('likes_acoustic', False) and song.get('acousticness', 0.0) > 0.7:
        score += 0.15

    return min(score, 1.0)


def confidence_label(score: float) -> str:
    """
    Returns a human-readable label for the confidence score.

    >= 0.75: 'High'
    >= 0.45: 'Medium'
    <  0.45: 'Low'
    """
    if score >= 0.75:
        return "High"
    elif score >= 0.45:
        return "Medium"
    else:
        return "Low"
