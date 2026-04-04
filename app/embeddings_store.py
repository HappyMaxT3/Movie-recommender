import os
import numpy as np
from app.config import EMBEDDINGS_FILE
from app.embedding_model import get_model


def load_or_create_embeddings(texts):
    model = get_model()

    if os.path.exists(EMBEDDINGS_FILE):
        embeddings = np.load(EMBEDDINGS_FILE)

        if len(embeddings) == len(texts):
            return embeddings

    embeddings = model.encode(texts, show_progress_bar=True)
    np.save(EMBEDDINGS_FILE, embeddings)

    return embeddings