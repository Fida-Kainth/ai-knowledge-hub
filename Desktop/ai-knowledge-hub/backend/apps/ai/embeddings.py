"""
Embeddings helper. Try provider (OpenAI) first, then fallback to
SentenceTransformers if available. If both unavailable, return
zero-vectors as a safe placeholder (useful for local dev).
"""

import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Synchronous helper to produce embeddings for a list of strings.
    Returns list of vectors (list of floats), one per input text.

    Provider selection:
      - If EMBEDDING_PROVIDER == 'openai' and OPENAI_API_KEY exists -> call OpenAI embeddings
      - Else if sentence-transformers installed -> use local model (small)
      - Else -> return zero vectors (dimension 384)
    """
    provider = getattr(settings, "EMBEDDING_PROVIDER", os.getenv("EMBEDDING_PROVIDER", "openai"))
    api_key = getattr(settings, "OPENAI_API_KEY", "") or os.getenv("OPENAI_API_KEY", "")

    if provider == "openai" and api_key:
        try:
            import openai
            openai.api_key = api_key
            model = getattr(settings, "EMBEDDING_MODEL", os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
            resp = openai.Embedding.create(model=model, input=texts)
            vectors = []
            for item in resp["data"]:
                vectors.append(item["embedding"])
            return vectors
        except Exception:
            logger.exception("OpenAI embeddings failed, trying local model...")

    # Try local sentence-transformers
    try:
        from sentence_transformers import SentenceTransformer
        model_name = "all-MiniLM-L6-v2"
        model = SentenceTransformer(model_name)
        vectors = model.encode(texts, show_progress_bar=False).tolist()
        return vectors
    except Exception:
        logger.exception("Local SentenceTransformer not available or failed.")

    # Final fallback: zero vectors
    dim = 384
    return [[0.0] * dim for _ in texts]
