from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_job_matches(
    user_text: str,
    job_texts: list[str],
) -> list[float]:
    """Calculate similarity scores between a user profile and job texts."""

    if not user_text.strip():
        return [0.0] * len(job_texts)

    if not job_texts:
        return []

    documents = [user_text, *job_texts]

    vectorizer = TfidfVectorizer(
        stop_words="english",
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    user_vector = tfidf_matrix[0:1]
    job_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(
        user_vector,
        job_vectors,
    )[0]

    return similarities.tolist()