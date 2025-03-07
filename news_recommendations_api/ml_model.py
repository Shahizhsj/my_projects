from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict
from models import News, UserNewsInteraction


class ContentBasedRecommender:
    def __init__(self):
        self.tfidf = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 2)
        )
        self.news_vectors = None
        self.news_items = None

    def _prepare_news_content(self, news: News) -> str:
        """Combine news features into a single text string"""
        # Handle None values
        title = news.title or ""
        description = news.description or ""
        content = news.content or ""
        return f"{title} {description} {content}".strip()

    def fit(self, news_items: List[News]):
        """Create TF-IDF vectors for all news items"""
        if not news_items:
            raise ValueError("No news items provided for fitting")

        self.news_items = news_items
        content_texts = [self._prepare_news_content(news) for news in news_items]

        # Filter out empty content
        valid_indices = [i for i, text in enumerate(content_texts) if text.strip()]
        if not valid_indices:
            raise ValueError("No valid content found in news items")

        valid_texts = [content_texts[i] for i in valid_indices]
        self.news_items = [news_items[i] for i in valid_indices]

        self.news_vectors = self.tfidf.fit_transform(valid_texts)

    def get_user_profile(self, user_interactions: List[UserNewsInteraction]) -> np.ndarray:
        """Create user profile based on their interactions"""
        if not user_interactions or not self.news_items:
            return None

        interacted_indices = []
        for interaction in user_interactions:
            try:
                idx = next(i for i, news in enumerate(self.news_items)
                           if news.id == interaction.post_id)
                interacted_indices.append(idx)
            except StopIteration:
                continue

        if not interacted_indices:
            return None

        # Create user profile by averaging the vectors of interacted items
        interacted_vectors = self.news_vectors[interacted_indices]
        if interacted_vectors.shape[0] == 0:
            return None

        user_profile = interacted_vectors.mean(axis=0)
        return np.asarray(user_profile).reshape(1, -1)

    def recommend(self,
                  user_profile: np.ndarray,
                  n_recommendations: int = 5,
                  exclude_news_ids: List[int] = None) -> List[Dict]:
        """Generate recommendations for a user"""
        if user_profile is None or self.news_vectors is None:
            return []

        # Calculate similarity between user profile and all news items
        similarities = cosine_similarity(user_profile, self.news_vectors)[0]

        # Create list of (index, similarity) tuples
        news_scores = list(enumerate(similarities))

        # Filter out already interacted items
        if exclude_news_ids:
            news_scores = [
                (idx, score) for idx, score in news_scores
                if self.news_items[idx].id not in exclude_news_ids
            ]

        if not news_scores:
            return []

        # Sort by similarity and get top N
        news_scores.sort(key=lambda x: x[1], reverse=True)
        top_recommendations = news_scores[:n_recommendations]

        # Format recommendations
        recommendations = []
        for idx, similarity_score in top_recommendations:
            news = self.news_items[idx]
            recommendations.append({
                'news_id': news.id,
                'title': news.title,
                'similarity_score': float(similarity_score),
                'description': news.description,
                'url': news.url
            })

        return recommendations