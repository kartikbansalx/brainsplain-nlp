import numpy as np

from rag import build_prompt, chunk, rank, retrieve


ARTICLE = (
    "Photosynthesis is how plants turn sunlight, water and carbon dioxide into sugar and oxygen. "
    "It happens inside chloroplasts, which contain the green pigment chlorophyll.\n"
    "== History ==\n"
    "The Roman Empire built roads across Europe and traded grain, wine and olive oil. "
    "Legions marched on those roads and cities grew along them.\n"
    "Medieval castles were built from stone and had thick walls, towers and moats."
)


class FakeEmbeddingModel:
    """Tiny deterministic stand-in so retrieval unit tests need no model download."""

    def encode(self, texts, normalize_embeddings=True):
        vectors = []
        for text in texts:
            lowered = text.lower()
            if "plant" in lowered or "photosynthesis" in lowered or "sunlight" in lowered:
                vectors.append([1.0, 0.0])
            elif "quantum" in lowered or "roman" in lowered or "castle" in lowered:
                vectors.append([0.0, 1.0])
            else:
                vectors.append([0.0, 0.0])
        return np.asarray(vectors, dtype=float)


def test_chunk_skips_headings():
    assert all(not c.startswith("=") for c in chunk(ARTICLE, min_words=10))


def test_rank_picks_semantically_relevant_chunk(monkeypatch):
    import rag
    monkeypatch.setattr(rag, "get_embedding_model", lambda: FakeEmbeddingModel())
    chunks = [
        "Photosynthesis allows plants to use sunlight to make sugar.",
        "The Roman Empire built roads across Europe.",
    ]
    assert "Photosynthesis" in rank("how do plants make sugar from sunlight", chunks, k=1)[0]


def test_rank_returns_nothing_for_unrelated_query(monkeypatch):
    import rag
    monkeypatch.setattr(rag, "get_embedding_model", lambda: FakeEmbeddingModel())
    assert rank("quantum entanglement", [
        "Photosynthesis allows plants to use sunlight.",
    ]) == []


def test_long_input_skips_retrieval(monkeypatch):
    import rag
    monkeypatch.setattr(rag, "fetch_article", lambda query: (_ for _ in ()).throw(
        AssertionError("Wikipedia should not be called for long input")
    ))
    assert retrieve("word " * 50) is None


def test_prompt_falls_back_without_context():
    assert build_prompt("black holes", None) == "Please explain this: black holes"


def test_prompt_includes_wikipedia_context():
    prompt = build_prompt("photosynthesis", {
        "title": "Photosynthesis",
        "url": "https://en.wikipedia.org/wiki/Photosynthesis",
        "chunks": ["Plants use sunlight to make food."],
    })
    assert "Wikipedia (Photosynthesis)" in prompt
    assert "Plants use sunlight" in prompt


def test_index_article_persists_chunks_and_reuses_unchanged_page(monkeypatch):
    import rag

    class FakeCollection:
        def __init__(self):
            self.records = {}
            self.upsert_calls = 0
            self.delete_calls = 0

        def get(self, where, include):
            records = {
                key: value for key, value in self.records.items()
                if value["metadata"]["article_key"] == where["article_key"]
            }
            return {
                "ids": list(records),
                "metadatas": [value["metadata"] for value in records.values()],
            }

        def delete(self, where):
            self.delete_calls += 1
            self.records = {
                key: value for key, value in self.records.items()
                if value["metadata"]["article_key"] != where["article_key"]
            }

        def upsert(self, ids, documents, embeddings, metadatas):
            self.upsert_calls += 1
            for item_id, document, embedding, metadata in zip(
                ids, documents, embeddings, metadatas
            ):
                self.records[item_id] = {
                    "document": document,
                    "embedding": embedding,
                    "metadata": metadata,
                }

    class FakeModel:
        def encode(self, texts, normalize_embeddings=True):
            return np.tile(np.array([[1.0, 0.0]]), (len(texts), 1))

    collection = FakeCollection()
    monkeypatch.setattr(rag, "get_collection", lambda: collection)
    monkeypatch.setattr(rag, "get_embedding_model", lambda: FakeModel())
    article = {
        "title": "Photosynthesis",
        "url": "https://en.wikipedia.org/wiki/Photosynthesis",
        "text": "Plants use sunlight to make food.",
    }

    first_key = rag.index_article(article, ["Plants use sunlight to make food."])
    second_key = rag.index_article(article, ["Plants use sunlight to make food."])

    assert first_key == second_key
    assert collection.upsert_calls == 1
    assert collection.delete_calls == 0
    assert len(collection.records) == 1
