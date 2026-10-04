from rag import build_prompt, chunk, rank, retrieve

ARTICLE = (
    "Photosynthesis is how plants turn sunlight, water and carbon dioxide into sugar and oxygen. "
    "It happens inside chloroplasts, which contain the green pigment chlorophyll.\n"
    "== History ==\n"
    "The Roman Empire built roads across Europe and traded grain, wine and olive oil. "
    "Legions marched on those roads and cities grew along them.\n"
    "Medieval castles were built from stone and had thick walls, towers and moats."
)


def test_chunk_skips_headings():
    assert all(not c.startswith("=") for c in chunk(ARTICLE, min_words=10))


def test_rank_picks_relevant_chunk():
    chunks = chunk(ARTICLE, min_words=10)
    assert "chlorophyll" in rank("how do plants make sugar from sunlight", chunks, k=1)[0]


def test_rank_returns_nothing_for_unrelated_query():
    assert rank("quantum entanglement", chunk(ARTICLE, min_words=10)) == []


def test_long_input_skips_retrieval():
    assert retrieve("word " * 50) is None


def test_prompt_falls_back_without_context():
    assert build_prompt("black holes", None) == "Please explain this: black holes"
