"""
Lightweight retrieval engine (the 'R' in RAG) using TF-IDF + cosine similarity.
No external API, no downloaded model weights - runs instantly on any free tier.
"""

from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from knowledge_base import KB

# Confidence threshold below which we admit we don't have a good answer.
MIN_SCORE = 0.12


@dataclass
class Match:
    topic: str
    answer: str
    score: float


class FitnessRetriever:
    def __init__(self, kb=None):
        self.kb = kb or KB
        # Combine topic + question variants into one searchable string per entry
        corpus = [f"{e['topic']}. {e['q']}" for e in self.kb]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.doc_matrix = self.vectorizer.fit_transform(corpus)

    def query(self, text: str, top_k: int = 2) -> list[Match]:
        if not text.strip():
            return []
        vec = self.vectorizer.transform([text])
        sims = cosine_similarity(vec, self.doc_matrix)[0]
        ranked = sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)

        matches = []
        for i in ranked[:top_k]:
            if sims[i] >= MIN_SCORE:
                matches.append(
                    Match(topic=self.kb[i]["topic"], answer=self.kb[i]["a"], score=float(sims[i]))
                )
        return matches

    def answer(self, text: str) -> str:
        matches = self.query(text, top_k=2)
        if not matches:
            return (
                "I don't have a confident answer for that in my knowledge base yet. "
                "Try asking about workout splits, exercise form (squat/deadlift/bench), "
                "warm-ups, recovery, nutrition basics, or common training aches."
            )

        best = matches[0]
        out = f"**{best.topic}**\n\n{best.answer}"

        # If there's a strong second match on a different topic, surface it too
        if len(matches) > 1 and matches[1].topic != best.topic and matches[1].score >= MIN_SCORE:
            out += f"\n\n---\nYou might also mean **{matches[1].topic}**:\n\n{matches[1].answer}"

        return out
