<div align="center">

<!-- BANNER — save banner.svg inside screenshots/ folder in your repo -->
<img src="screenshots/banner.svg" alt="Brainsplain Banner" width="860"/>

<br/><br/>
<p align="center">
  <em>"Turn complex jargon into crystal clear concepts. Like a pop-up book for your brain."</em>
</p>
<br/>

<a href="https://brainsplain-ai.onrender.com/" target="_blank">
  <img src="https://img.shields.io/badge/🌐%20Live%20Demo-brainsplain--ai.onrender.com-0d6e7a?style=for-the-badge" alt="Live Demo"/>
</a>

<br/><br/>

<img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini"/>
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
<img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Render"/>
<img src="https://img.shields.io/badge/License-MIT-FBBF24?style=for-the-badge" alt="MIT"/>

</div>

---

## 📸 Screenshots

<div align="center">

| 🏠 Homepage |
|:-----------:|
| ![Homepage](screenshots/homepage.png) |

</div>



---

## 🎬 Demo Video

<div align="center">

[![Watch Demo](https://img.shields.io/badge/▶%20Watch%20Demo-YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtube.com)

> 📌 Record a 30–60 sec walkthrough on [Loom](https://loom.com) or OBS, then replace the link above.

</div>

---

## ✨ What is Brainsplain?

**Brainsplain** is a web app that takes any complex topic — a scientific concept, a news article, a confusing technical term — and explains it in plain, engaging language using Google's Gemini AI.

Choose your explanation level:

| Level | What it feels like |
|-------|--------------------|
| 🧒 **Age 5** | A bedtime story — emojis, fun analogies, pure simplicity |
| 🧑 **Age 10** | Clear and engaging — like a cool teacher explaining it |
| 🧑‍🎓 **Teen** | Conversational, accurate, completely jargon-free |

The app also keeps a **History** of your past explanations so you can revisit them anytime.

---

## 🚀 Features

- 🧠 **AI-Powered** — Google Gemini generates smart, contextual simplifications
- 🎚️ **3 Explanation Levels** — Age 5, Age 10, Teen — each with a tailored system prompt
- 🕓 **Explanation History** — Revisit your past queries anytime
- 🔬 **NLP Analysis** — Extracts jargon and named entities from your input and checks that the explanation matches the chosen reading level
- 📚 **RAG Grounding** — Short topics are grounded in the best-matching Wikipedia article (retrieved, chunked, embedded and searched semantically with ChromaDB) before Gemini explains them, with a source link
- ⚡ **Fast Results** — Explanations generated in seconds
- 📱 **Fully Responsive** — Clean experience on mobile and desktop
- 🐳 **Dockerized** — Runs consistently anywhere with Docker
- 🔒 **Secure** — API key stored as an environment variable, never in code
- 🌐 **Live on Render** — [brainsplain-ai.onrender.com](https://brainsplain-ai.onrender.com)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python · Flask · Flask-CORS |
| **AI Engine** | Google Gemini API (`gemini-flash-latest`) |
| **NLP** | spaCy (`en_core_web_sm`) · textstat · wordfreq |
| **RAG** | Wikipedia API · Sentence Transformers (`all-MiniLM-L6-v2`) · ChromaDB vector database |
| **Config** | python-dotenv |
| **Containerization** | Docker |
| **Deployment** | Render |

---

## 📁 Project Structure

```
Brainsplain-ai/
│
├── 📂 backend/                # Flask API server
│   ├── app.py                 # Main server — routes & Gemini integration
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # API key (local only — never commit)
│
├── 📂 frontend/               # Static frontend
│   ├── index.html             # Main page
│   ├── style.css              # Styling & gradient design
│   └── script.js              # Frontend logic & API calls
│
├── 📄 Dockerfile              # Docker config for unified deployment
├── 📄 .gitignore              # Keeps .env out of GitHub
└── 📄 README.md
```

---

## ⚙️ Run Locally

### Option A — Without Docker

#### Prerequisites
- Python 3.8+
- A Google Gemini API key from [aistudio.google.com](https://aistudio.google.com)

```bash
# 1. Clone the repo
git clone https://github.com/kartikbansalx/Brainsplain-ai.git
cd Brainsplain-ai/backend

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 3b. Download the spaCy English model
python -m spacy download en_core_web_sm

# 4. Create your .env file
echo "Gemini_API_KEY=your_actual_api_key_here" > .env

# 5. Start the server
python app.py
```

Open **http://localhost:5000** in your browser. 🎉

---

### Option B — With Docker 🐳

```bash
# 1. Clone the repo
git clone https://github.com/kartikbansalx/Brainsplain-ai.git
cd Brainsplain-ai

# 2. Build the Docker image
docker build -t brainsplain .

# 3. Run the container
docker run -p 5000:5000 \
  -v brainsplain_chroma:/data/chroma_db \
  -e CHROMA_DB_PATH=/data/chroma_db \
  -e Gemini_API_KEY=your_key_here \
  brainsplain
```

Open **http://localhost:5000** in your browser. 🎉

---

## 🌐 Deploy on Render

1. Push your code to GitHub *(ensure `.env` is in `.gitignore`)*
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repo: `kartikbansalx/Brainsplain-ai`
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Build Command** | `pip install -r backend/requirements.txt && python -m spacy download en_core_web_sm` |
| **Start Command** | `python backend/app.py` |
| **Environment Variable** | `Gemini_API_KEY` → your key |

5. Click **Deploy** — your site goes live in ~2 minutes ✅

**Important for ChromaDB:** attach a Render persistent disk to the service (for example, mount it at `/var/data`) and add `CHROMA_DB_PATH=/var/data/chroma_db` under Environment Variables. Without a persistent disk, the vector index may be lost when Render replaces the instance.

> 💡 If using the Dockerfile, select **Docker** as the environment instead and Render will handle the rest.

---

## 🔐 API Key Safety

> ⚠️ **Never hardcode your API key.** Google's scanners detect exposed keys on GitHub within seconds and auto-revoke them.

```python
# ✅ Safe — reads from environment
api_key = os.environ.get("Gemini_API_KEY")

# ❌ Never do this — will get your key revoked instantly
api_key = "AIzaSy...."
```

Set your key only via Render's **Environment** tab in the dashboard — not in your code.

---

## 🔬 NLP Pipeline

```
input text → tokenize → POS tag → drop stop words → lemmatize → keep rare words → key terms
                     └→ named entity recognition → entities

Gemini output → strip emojis → Flesch-Kincaid grade → compare with level target → "Level fit" badge
```

| Step | Technique | Why |
|------|-----------|-----|
| Key terms | spaCy POS tagging + lemmatization + stop-word removal, then a word-frequency (Zipf) filter via `wordfreq` | Nouns that are rare in everyday English are the likely jargon |
| Entities | spaCy NER | Surfaces people, places and organisations in the input |
| Level fit | Flesch-Kincaid grade (`textstat`) vs. a per-level target | Checks the LLM actually followed the Age 5 / Age 10 / Teen instruction |

Code lives in [`backend/nlp_utils.py`](backend/nlp_utils.py). Grade targets are starting values and are meant to be tuned.

---

## 📚 RAG Pipeline

```
topic (≤ 12 words) → Wikipedia search → plain-text article → paragraph-based chunks
                  → Sentence Transformer embeddings (384-dimensional dense vectors)
                  → persistent ChromaDB cosine search → top 3 relevant chunks
                  → added to the Gemini prompt as reference → explanation + source link
```

| Step | What happens |
|------|--------------|
| Retrieve | The Wikipedia API returns the best-matching article as plain text (references and "See also" are cut) |
| Chunk | Paragraphs are grouped into chunks of about 100 words |
| Embed | `sentence-transformers/all-MiniLM-L6-v2` converts each chunk and query into a dense 384-dimensional semantic vector |
| Index | ChromaDB stores each chunk, its embedding, and metadata (Wikipedia title, URL, chunk index and article content hash) |
| Search | The query embedding is compared with chunks using cosine distance; the top 3 relevant chunks are returned |
| Cache | Previously indexed articles are reused. If Wikipedia's article text changes, its old chunks are replaced |
| Augment | Retrieved chunks are added to the Gemini prompt as reference text, with an instruction to simplify and not copy |
| Fallback | Long input, no relevant chunks, or an unavailable retrieval service leaves the existing Gemini-only response path intact |

The knowledge source remains Wikipedia only. The vector database is a persistent index/cache for Wikipedia content, not an additional source. Retrieval is implemented in [`backend/rag.py`](backend/rag.py), with offline unit tests in [`backend/test_rag.py`](backend/test_rag.py). The embedding model is downloaded and loaded on the first retrieval request, so the first request can take longer than subsequent requests.

### Vector database storage

- Local development: ChromaDB persists to `backend/chroma_db/` when running from the `backend` directory.
- Docker: mount a persistent volume at `/data/chroma_db` and set `CHROMA_DB_PATH=/data/chroma_db`.
- Render: attach a persistent disk (for example, mounted at `/var/data`) and set `CHROMA_DB_PATH=/var/data/chroma_db`. Without a persistent disk, the database can be lost when the service is redeployed or its instance is replaced.
- Optional settings: `EMBEDDING_MODEL`, `CHROMA_DB_PATH`, `RAG_TOP_K` (default `3`) and `RAG_MIN_SIMILARITY` (default cosine similarity `0.20`). The similarity threshold is a starting point and should be tuned against representative queries.

### Run tests

```bash
cd backend
pytest -q
```

---

## 📡 API Reference

### `POST /api/explain`

**Request body:**
```json
{
  "topic": "How does the internet work?",
  "level": "Age 5"
}
```

**Response:**
```json
{
  "explanation": "Imagine the internet is like a giant post office... 📬",
  "nlp": {
    "terms": ["protocol", "router"],
    "entities": ["ARPANET"],
    "readability": { "grade": 5.2, "target": 6, "fits": true }
  },
  "rag": {
    "used": true,
    "title": "Internet",
    "url": "https://en.wikipedia.org/wiki/Internet"
  }
}
```

Valid `level` values: `"Age 5"` · `"Age 10"` · `"Teen"`

---

### `GET /api/health`

```json
{ "status": "healthy" }
```

---

## 🗺️ Roadmap

- [x] AI explanation engine with 3 age levels
- [x] Explanation history panel
- [x] Flask REST API with error handling
- [x] Secure API key via environment variables
- [x] Dockerized for consistent deployment
- [x] Live on Render
- [ ] Copy & Share to Twitter button
- [ ] URL input — paste an article link to explain it
- [ ] Dark mode
- [ ] Text-to-speech (read explanation aloud)
- [ ] Browser extension — right-click any text to explain it

---

## 🤝 Contributing

Contributions, ideas, and bug reports are welcome!

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
# Open a Pull Request on GitHub
```

---

## 📄 License

Licensed under the **MIT License** — free to use, remix, and build on.

---

<div align="center">

Made with ❤️ by **[@kartikbansalx](https://github.com/kartikbansalx)**

<br/>

**⭐ Found this useful? Star the repo — it means a lot! ⭐**

<br/>

[![GitHub stars](https://img.shields.io/github/stars/kartikbansalx/Brainsplain-ai?style=social)](https://github.com/kartikbansalx/Brainsplain-ai/stargazers)
&nbsp;&nbsp;
[![GitHub forks](https://img.shields.io/github/forks/kartikbansalx/Brainsplain-ai?style=social)](https://github.com/kartikbansalx/Brainsplain-ai/fork)

</div>
