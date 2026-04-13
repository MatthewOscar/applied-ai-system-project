import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and converts numeric fields."""
    songs = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict,
               weights: Optional[Dict[str, float]] = None) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    if weights is None:
        weights = {"genre": 2.0, "mood": 1.0, "energy": 1.0, "acoustic": 0.5}

    user_genre = user_prefs.get('genre', '')
    user_mood = user_prefs.get('mood', '')
    user_energy = user_prefs.get('energy', 0.5)
    user_likes_acoustic = user_prefs.get('likes_acoustic', False)

    song_genre = song.get('genre', '')
    song_mood = song.get('mood', '')
    song_energy = song.get('energy', 0.5)
    song_acousticness = song.get('acousticness', 0.0)

    score = 0.0
    reasons = []

    if song_genre.lower() == user_genre.lower():
        pts = weights["genre"]
        score += pts
        reasons.append(f"Genre match ({song_genre}): +{pts:.1f}")

    if song_mood.lower() == user_mood.lower():
        pts = weights["mood"]
        score += pts
        reasons.append(f"Mood match ({song_mood}): +{pts:.1f}")

    energy_sim = weights["energy"] * (1.0 - abs(song_energy - user_energy))
    score += energy_sim
    reasons.append(f"Energy similarity: +{energy_sim:.2f}")

    if user_likes_acoustic and song_acousticness > 0.7:
        pts = weights["acoustic"]
        score += pts
        reasons.append(f"Acoustic bonus (acousticness={song_acousticness:.2f}): +{pts:.1f}")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    weights: Optional[Dict[str, float]] = None) -> List[Tuple[Dict, float, str]]:
    """Scores all songs, ranks them, and returns the top k with explanations."""
    scored = []
    for song in songs:
        song_score, reasons = score_song(user_prefs, song, weights=weights)
        explanation = "; ".join(reasons)
        scored.append((song, song_score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _to_dicts(user: UserProfile, song: Song):
        """Convert dataclass objects to dicts for score_song."""
        user_dict = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic,
        }
        song_dict = {
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'acousticness': song.acousticness,
        }
        return user_dict, song_dict

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs ranked by match to the user profile."""
        scored = []
        for song in self.songs:
            user_dict, song_dict = self._to_dicts(user, song)
            song_score, _ = score_song(user_dict, song_dict)
            scored.append((song, song_score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation for why a song was recommended."""
        user_dict, song_dict = self._to_dicts(user, song)
        _, reasons = score_song(user_dict, song_dict)
        return "; ".join(reasons)
