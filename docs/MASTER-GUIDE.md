# RegEngine — Master Guide (Hinglish)

> Ye document sab kuch explain karta hai — project kya hai, kaise kaam karta hai,
> kaunse tools use hue, aur presentation mein kaise bolna hai.
> Padh lo, samajh lo, apne words mein bol dena.

---

## 📌 Table of Contents

1. [Project Kya Hai?](#1-project-kya-hai)
2. [Simple Example Se Samjho](#2-simple-example-se-samjho)
3. [Architecture — System Kaise Bana Hai](#3-architecture)
4. [Kaunse Tools/Libraries Use Hue](#4-tools)
5. [Folder Structure — Har Folder Ka Kaam](#5-folders)
6. [Har File Ka Kaam (Detail Mein)](#6-files)
7. [Docker Kya Hai aur Kyun Use Kiya](#7-docker)
8. [GitHub Workflow — Team Kaise Kaam Karti Hai](#8-github)
9. [Step-by-Step Flow — Upload se Answer Tak](#9-flow)
10. [API Endpoints — Kaunsa Kya Karta Hai](#10-api)
11. [Embedding — ye Kya Hota Hai](#11-embedding)
12. [Qdrant — Vector Database Kya Hai](#12-qdrant)
13. [Presentation Script — Kaise Bolo](#13-presentation)
14. [FAQ — Interview/Common Questions](#14-faq)
15. [Current Status — Abhi Kya Ban Gaya](#15-status)

---

## 1. Project Kya Hai? {#1-project-kya-hai}

**RegEngine** ek **RAG Engine** hai — matlab **Retrieval-Augmented Generation**.

**Simple words mein:**
Tumhare paas bahut saare documents hain (PDF, Word, Text files). RegEngine unhe padhta hai, yaad rakhta hai, aur jab tum kuch poocho toh relevant answer deta hai sources ke saath.

**Ek line mein:** RegEngine ek smart search engine hai jo tumhare documents se sawaal ka jawab deta hai.

**Ye kyun useful hai:**
- Agar tumhare paas 100 PDF hain toh manually dhundna mushkil hai
- RegEngine unhe automatically padh ke answer dega
- Answer ke saath batata hai ki kis document se aaya hai

---

## 2. Simple Example Se Samjho {#2-simple-example-se-samjho}

**Real life example:**

```
Tum: "What is the warranty policy of Product X?"

RegEngine kya karta hai:
1. Tumhara sawaal padhta hai
2. Apne database mein 500 documents hain unme se dhundta hai
3. 3-4 relevant paragraphs dhund ke laata hai
4. Un paragraphs ko padh ke answer likhta hai
5. Tumhe answer deta hai + batata hai ki kis file se aaya
```

**Ek aur example:**

```
Tum: "NEET exam leak ke baare mein kya hai?"

RegEngine:
1. Documents mein dhundta hai "NEET", "leak", "exam" se related
2. Relevant chunks laata hai
3. Answer deta hai with source files
```

**Ye Google se alag kaise hai:**
- Google internet pe dhundta hai
- RegEngine sirf TUMHARE documents pe dhundta hai
- Ye private hai — tumhara data bahar nahi jaata

---

## 3. Architecture — System Kaise Bana Hai {#3-architecture}

```
                    USER (Tum)
                       │
                       ▼
              ┌─────────────────┐
              │   DASHBOARD     │  ← Streamlit website (Megha bana rahi hai)
              │   (Port 8501)   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   FASTAPI API   │  ← Main server (Mrity ne banaya)
              │   (Port 8000)   │
              └────────┬────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │ INGESTION│  │ RETRIEVAL│  │   LLM    │
   │ (Rakhi)  │  │ (Viraj)  │  │ (OpenAI) │
   └────┬─────┘  └────┬─────┘  └──────────┘
        │              │
        ▼              ▼
   ┌──────────────────────────┐
   │      QDRANT DATABASE     │  ← Vectors store hote hain
   │      (Port 6333)         │
   └──────────────────────────┘
```

**Ye 3 main kaam hain:**
1. **Ingestion** — Document padhna, todna, numbers mein convert karna
2. **Retrieval** — Sawaal ka relevant documents dhundna
3. **Generation** — LLM se answer likhwana

---

## 4. Kaunse Tools/Libraries Use Hue {#4-tools}

### Core Framework
| Tool | Kya Hai | Kyun Use Kiya |
|------|---------|---------------|
| **Python 3.11** | Programming language | Sab kuch isme likha hai |
| **FastAPI** | Web framework | API server banane ke liye |
| **Uvicorn** | Server | FastAPI ko run karne ke liye |

### Database
| Tool | Kya Hai | Kyun Use Kiya |
|------|---------|---------------|
| **Qdrant** | Vector database | Embeddings store karne ke liye |
| **qdrant-client** | Python library | Qdrant se baat karne ke liye |

### AI/ML
| Tool | Kya Hai | Kyun Use Kiya |
|------|---------|---------------|
| **sentence-transformers** | Embedding model | Text ko numbers mein convert karne ke liye |
| **all-MiniLM-L6-v2** | Specific model | Fast aur accurate embeddings deta hai |
| **OpenAI API** | LLM | Answer generate karne ke liye |

### Document Processing
| Tool | Kya Hai | Kyun Use Kiya |
|------|---------|---------------|
| **pypdf** | PDF reader | PDF files padhne ke liye |
| **python-docx** | Word reader | DOCX files padhne ke liye |

### Frontend
| Tool | Kya Hai | Kyun Use Kiya |
|------|---------|---------------|
| **Streamlit** | Web framework | Dashboard banane ke liye (simple hai) |

### DevOps
| Tool | Kya Hai | Kyun Use Kiya |
|------|---------|---------------|
| **Docker** | Containerization | Sab ek jagah chalane ke liye |
| **Docker Compose** | Multi-container | Qdrant + API + Dashboard ek saath |

### Config
| Tool | Kya Hai | Kyun Use Kiya |
|------|---------|---------------|
| **python-dotenv** | .env loader | Secret keys safe rakhne ke liye |

---

## 5. Folder Structure — Har Folder Ka Kaam {#5-folders}

```
root/
│
├── api/                  ← "Receptionist" — sab requests yahan aati hain
│   ├── main.py           ← Routes: health, upload, query, collections, stats
│   ├── config.py         ← Settings: API keys, database URL, etc.
│   └── models.py         ← Data format: request/response kaise dikhega
│
├── ingestion/            ← "Reader" — documents padhta hai
│   ├── loader.py         ← PDF, DOCX, TXT files khol ke text nikalta hai
│   ├── chunker.py        ← Bade text ko chhote pieces mein todta hai
│   ├── embedder.py       ← Text ko numbers (vectors) mein convert karta hai
│   └── pipeline.py       ← ye teeno ek saath karta hai
│
├── retrieval/            ← "Searcher" — sawaal ka jawab dhundta hai
│   ├── search.py         ← Qdrant mein similar chunks dhundta hai
│   └── context.py        ← Results ko LLM ke liye format karta hai
│
├── eval/                 ← "Grader" — answer kitna achha hai check karta hai
│   └── metrics.py        ← Relevance, faithfulness, completeness score
│
├── dashboard/            ← "Front Desk" — website jahan user baat karta hai
│   └── app.py            ← Streamlit chat interface
│
├── mcp_server/           ← "AI Connector" — Claude/AI tools se connect karta hai
│   └── server.py         ← MCP protocol implement karta hai
│
├── docs/                 ← "Manual" — saari documentation
│   ├── ARCHITECTURE.md   ← System architecture detail mein
│   ├── GIT_WORKFLOW.md   ← Git kaise use karna hai
│   ├── ROADMAP.md        ← Project plan (sabka)
│   ├── ROADMAP-mrity.md  ← Sirf Mrity ke tasks
│   ├── ROADMAP-rakhi.md  ← Sirf Rakhi ke tasks
│   ├── ROADMAP-viraj.md  ← Sirf Viraj ke tasks
│   └── ROADMAP-megha.md  ← Sirf Megha ke tasks
│
├── Dockerfile            ← Docker image banane ke instructions
├── docker-compose.yml    ← Sab services ek saath start karne ke liye
├── requirements.txt      ← Saari Python libraries ka list
├── .env                  ← Secret keys (OpenAI API key)
├── .env.example          ← Template — keys kahan daalni hain
├── .gitignore            ← Git ko kaunse files ignore karni hain
└── README.md             ← Project ka introduction
```

---

## 6. Har File Ka Kaam (Detail Mein) {#6-files}

### api/main.py — Main Server
```python
# Ye file FastAPI ka main app hai
# Isme 5 routes hain:

GET  /api/health     → Check karta hai ki sab chal raha hai
POST /api/upload     → File upload karta hai, process karta hai, store karta hai
POST /api/query      → Sawaal leke answer deta hai
GET  /api/collections → Saari collections dikhata hai
GET  /api/stats      → System statistics dikhata hai

# Upload flow:
# File aayi → Loader ne padha → Chunker ne toda → Embedder ne numbers banaye → Qdrant mein store

# Query flow:
# Sawaal aaya → Embedder ne numbers banaye → Qdrant ne similar chunks dhunde → Context banaya → LLM ne answer likha
```

### api/config.py — Settings
```python
# Ye file saari settings store karti hai
# .env file se values padhti hai

QDRANT_URL = "http://localhost:6333"    # Qdrant kahan hai
OPENAI_API_KEY = "sk-..."               # OpenAI key (answer generate karne ke liye)
CHUNK_SIZE = 500                         # Text kitne pieces mein todega
CHUNK_OVERLAP = 50                       # Pieces kitne overlap karenge
TOP_K = 5                               # Kitne results dikhane hain
SIMILARITY_THRESHOLD = 0.5              # Minimum match score
EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # Kaunsa model use hoga
```

### ingestion/loader.py — Document Reader
```python
# Ye file different formats ke documents padhti hai

load_document("report.pdf")   → pypdf se padhta hai
load_document("notes.docx")   → python-docx se padhta hai
load_document("readme.txt")   → directly padhta hai
load_document("guide.md")     → directly padhta hai

# Output: ek bada string (poora document ka text)
```

### ingestion/chunker.py — Text Splitter
```python
# Ye file bade text ko chhote pieces mein todta hai

# Example:
# Bada text: "RegEngine is a RAG engine. It processes documents. It answers questions."
# Chunk size: 50 chunks
# Output:
# [
#   {"text": "RegEngine is a RAG engine...", "start": 0, "end": 50},
#   {"text": "...engine. It processes...", "start": 0, "end": 100},
# ]

# Chunking kyun zaroori hai?
# - LLM ke paas limited memory hai (context window)
# - Bada text daaloge toh kuch yaad nahi rakhega
# - Chhote pieces se better results milte hain
```

### ingestion/embedder.py — Text to Numbers Converter
```python
# Ye file text ko numbers mein convert karti hai
# Isse "embedding" kehte hain

# Example:
# "hello" → [0.12, -0.34, 0.56, ...]  (384 numbers)

# Ye kyun karte hain?
# - Computers ko text samajh nahi aata
# - Numbers se similarity calculate ho sakti hai
# - "cat" aur "kitten" ke numbers paas honge
# - "cat" aur "car" ke numbers door honge

# Model: all-MiniLM-L6-v2
# - Fast hai
# - Free hai (no API key needed)
# - 384 dimensions (384 numbers har text ke liye)
```

### retrieval/search.py — Vector Search
```python
# Ye file Qdrant mein similar chunks dhundti hai

# Example:
# Sawaal: "What is warranty policy?"
# Embedding: [0.12, -0.34, 0.56, ...]
# Qdrant mein 500 stored chunks hain

# Search result:
# [
#   {"text": "Warranty covers 2 years...", "score": 0.85},
#   {"text": "For warranty claims...", "score": 0.78},
#   {"text": "Product guarantee...", "score": 0.72},
# ]

# Score 0 se 1 tak hota hai — jitna zyada, utna relevant
```

### retrieval/context.py — Prompt Builder
```python
# Ye file LLM ke liye prompt banati hai

# Format:
# "You are a helpful assistant. Based on these sources:
#  [Source 1 | Relevance: 0.85] Warranty covers 2 years...
#  [Source 2 | Relevance: 0.78] For warranty claims...
#
#  QUESTION: What is warranty policy?
#  ANSWER:"

# Ye isliye karte hain taaki LLM ko clear instruction mile
```

### eval/metrics.py — Quality Checker
```python
# Ye file check karti hai ki answer kitna achha hai

# 3 metrics hain:
# 1. Relevance — Kya answer sawaal se related hai?
# 2. Faithfulness — Kya answer source documents se match karta hai?
# 3. Completeness — Kya answer ne poora sawaal cover kiya?

# Score 0 se 1 tak hota hai — jitna zyada, utna achha
```

### dashboard/app.py — Website
```python
# Ye Streamlit ka app hai
# Isme 2 cheezein hain:
# 1. Sidebar — File upload + settings
# 2. Main area — Chat interface

# User kya karta hai:
# 1. Sidebar mein file upload karta hai
# 2. Chat box mein sawaal likhta hai
# 3. Answer dikhta hai with sources
```

---

## 7. Docker Kya Hai aur Kyun Use Kiya {#7-docker}

### Docker Kya Hai?
Docker ek tool hai jo applications ko **containers** mein chalata hai.

**Simple analogy:**
- Pehle: Har machine pe alag se software install karna padta tha
- Ab: Docker sab kuch ek box mein de deta hai — bas box kholo, kaam karo

### Humne Kyun Use Kiya?
```
Problem: Qdrant alag chahiye, API alag chahiye, Dashboard alag chahiye
         Agar manually install karo toh bahut mushkil

Solution: Docker Compose — ek command se sab start
          docker-compose up --build
          → Qdrant start (port 6333)
          → API start (port 8000)
          → Dashboard start (port 8501)
```

### Docker Compose File Kya Karti Hai?
```yaml
services:
  qdrant:        # Vector database container
    image: qdrant/qdrant:latest
    ports: 6333, 6334

  backend:       # FastAPI server container
    build: .
    ports: 8000
    depends_on: qdrant

  dashboard:     # Streamlit UI container
    build: .
    ports: 8501
    depends_on: backend
```

### Docker Commands:
```bash
docker-compose up --build    # Sab start karo (build + run)
docker-compose up -d         # Background mein chalao
docker-compose down          # Sab band karo
docker-compose ps            # Dekho kaun chal raha hai
docker-compose logs -f       # Live logs dekho
```

---

## 8. GitHub Workflow — Team Kaise Kaam Karti Hai {#8-github}

### Branches:
```
main        ← Official version (protected — koi directly push nahi karega)
  └── develop  ← Testing version (sab yahan merge karenge)
        ├── feature/api-layer           ← Mrity ka kaam
        ├── feature/ingestion-pipeline  ← Rakhi ka kaam
        ├── feature/retrieval-engine    ← Viraj ka kaam
        └── feature/dashboard           ← Megha ka kaam
```

### Kaam Kaise Hota Hai:
```
1. Apne branch pe kaam karo
2. Jab kaam ho jaye → git push
3. GitHub pe Pull Request banao (feature/xxx → develop)
4. Mrity review karega
5. Approve hone pe develop mein merge hoga
6. Jab sab ready ho → develop → main
```

### Git Commands:
```bash
git clone https://github.com/NOVA-RRMV/nova-rrmv-local.git
git checkout feature/api-layer        # Apne branch pe jao
git add .                              # Sab files stage karo
git commit -m "feat: naya feature"     # Save karo
git push origin feature/api-layer      # GitHub pe bhejo
```

---

## 9. Step-by-Step Flow — Upload se Answer Tak {#9-flow}

### Phase A: Document Upload
```
Step 1: User file upload karta hai (PDF/DOCX/TXT)
        ↓
Step 2: Loader file padhta hai → text nikalta hai
        Example: "RegEngine is a RAG engine built by Team..."
        ↓
Step 3: Chunker text ko chhote pieces mein todta hai
        Example: [
          "RegEngine is a RAG engine built by Team",
          "Nova RRMV. It allows users to upload...",
          "documents like PDFs, Word files..."
        ]
        ↓
Step 4: Embedder har piece ko numbers mein convert karta hai
        Example: [0.12, -0.34, 0.56, ...]  (384 numbers)
        ↓
Step 5: Qdrant database mein store hota hai
        Har chunk ke saath: text + vector + metadata
        ↓
Step 6: Response aata hai: "3 chunks stored successfully"
```

### Phase B: Question Answering
```
Step 1: User sawaal poochta hai: "What is RegEngine?"
        ↓
Step 2: Embedder sawaal ko numbers mein convert karta hai
        Example: [0.15, -0.32, 0.58, ...]
        ↓
Step 3: Qdrant mein similar vectors dhundta hai
        Ye "vector similarity search" kehte hain
        ↓
Step 4: Top 5 similar chunks milte hain (scores ke saath)
        Example:
        - Score 0.85: "RegEngine is a RAG engine..."
        - Score 0.78: "It processes documents..."
        - Score 0.72: "Vector database stores..."
        ↓
Step 5: Context banaya jaata hai (sab chunks mila ke)
        ↓
Step 6: LLM ko context + sawaal diya jaata hai
        ↓
Step 7: LLM answer deta hai with source citations
        Example: "RegEngine is a RAG engine built by
                  Team Nova RRMV that processes documents
                  and answers questions. [Source: regengine.pdf]"
```

---

## 10. API Endpoints — Kaunsa Kya Karta Hai {#10-api}

### Health Check
```
GET /api/health
→ Check karta hai ki Qdrant chal raha hai
→ Response: {"status": "ok", "qdrant_connected": true, "version": "0.1.0"}
```

### Upload Document
```
POST /api/upload
→ File bhejo (PDF/DOCX/TXT)
→ System padhega, todega, numbers banayega, store karega
→ Response: {"filename": "report.pdf", "chunks_stored": 15, "collection": "default"}
```

### Query (Sawaal Poocho)
```
POST /api/query
→ Sawaal bhejo
→ System dhundega aur answer dega
→ Response: {
    "answer": "RegEngine is a RAG engine...",
    "sources": [{"text": "...", "filename": "report.pdf", "score": 0.85}],
    "confidence": 0.85
  }
```

### List Collections
```
GET /api/collections
→ Kitne collections hain aur kitne documents hain
→ Response: {"collections": [{"name": "default", "points_count": 50}]}
```

### Stats
```
GET /api/stats
→ System statistics
→ Response: {
    "total_collections": 1,
    "total_vectors": 50,
    "total_uploads": 5,
    "collections": ["default"]
  }
```

---

## 11. Embedding — Ye Kya Hota Hai {#11-embedding}

### Embedding Simple Words Mein:
Text ko numbers mein convert karna.

### Kyun Karte Hain?
```
Computer ko text samajh nahi aata.
Numbers se similarity calculate ho sakti hai.

"cat"   → [0.2, 0.8, 0.1, ...]
"kitten" → [0.2, 0.7, 0.1, ...]  ← paas hai (similar meaning)
"car"   → [0.9, 0.1, 0.6, ...]  ← door hai (different meaning)
```

### Kaise Kaam Karta Hai?
```
1. Model (all-MiniLM-L6-v2) text padhta hai
2. Har word ka meaning samajhta hai
3. Context dekh ke 384 numbers deta hai
4. Ye numbers "vector" ya "embedding" kehte hain
```

### Example:
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Ek sentence
vector = model.encode("What is RegEngine?")
print(vector)  # [0.12, -0.34, 0.56, ...]  (384 numbers)

# Do sentences compare karo
vectors = model.encode(["cat", "kitten", "car"])
# "cat" aur "kitten" similar honge
# "car" alag hoga
```

---

## 12. Qdrant — Vector Database Kya Hai {#12-qdrant}

### Qdrant Simple Words Mein:
Ek database jo vectors (numbers ke arrays) store karta hai aur unhe search karta hai.

### Regular Database vs Vector Database:
```
MySQL/PostgreSQL:
  "SELECT * FROM documents WHERE text LIKE '%warranty%'"
  → Text matching — exact words dhundhta hai

Qdrant (Vector DB):
  "Find documents SIMILAR to this question"
  → Meaning matching — concept samajhta hai
  → "warranty policy" aur "guarantee terms" dono mil sakte hain
```

### Qdrant Kaise Kaam Karta Hai?
```
1. Collection banao (jaise table)
2. Vectors + payload (metadata) store karo
3. Query vector do → similar vectors milenge
4. Score milega — kitna similar hai (0 se 1)
```

### Commands:
```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

# Collection banao
client.create_collection(
    collection_name="default",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Data store karo
client.upsert(
    collection_name="default",
    points=[PointStruct(id=1, vector=[...], payload={"text": "..."})]
)

# Search karo
results = client.query_points(
    collection_name="default",
    query=[...],  # query vector
    limit=5       # top 5 results
)
```

---

## 13. Presentation Script — Kaise Bolo {#13-presentation}

### Opening (1-2 minute):
```
"Good morning/afternoon everyone. Today I'm presenting RegEngine —
a Retrieval-Augmented Generation engine built by Team Nova RRMV.

The problem we're solving is: when you have hundreds of documents,
finding specific information is time-consuming. RegEngine makes this
instant — upload your documents, ask a question, get an answer with sources."
```

### Architecture (2-3 minute):
```
"Our system has 5 main components:

1. INGESTION PIPELINE — Built by Rakhi
   Takes PDF, Word, or Text files, splits them into chunks,
   and converts them to embeddings using sentence-transformers.

2. VECTOR DATABASE — Built by Viraj
   Uses Qdrant to store embeddings. When a question comes in,
   it finds the most similar document chunks using vector similarity.

3. API LAYER — Built by Mrity
   FastAPI backend that connects everything. Handles upload,
   query, and serves as the central hub.

4. DASHBOARD — Built by Megha
   Streamlit-based web interface where users can upload documents
   and chat with their documents.

5. EVALUATION — Built together
   Metrics to measure answer quality — relevance, faithfulness, completeness."
```

### How It Works (2-3 minute):
```
"The flow is simple:

UPLOAD: User uploads a document → system reads it → splits into
500-character chunks → converts each chunk to a 384-dimensional
vector → stores in Qdrant.

QUERY: User asks a question → system converts question to vector →
finds top 5 similar chunks in Qdrant → builds context →
sends to LLM for answer generation → returns answer with sources.

The key insight is: we're not searching by keywords — we're searching
by MEANING. So 'warranty policy' and 'guarantee terms' will both match."
```

### Tech Stack (1 minute):
```
"We're using Python with FastAPI for the backend, Qdrant for vector storage,
sentence-transformers for embeddings, OpenAI for LLM generation,
Streamlit for the dashboard, and Docker for deployment."
```

### Demo (2-3 minute):
```
[Show live demo]
1. Open dashboard at localhost:8501
2. Upload a PDF file
3. Show that chunks are stored in Qdrant
4. Ask a question
5. Show the answer with source citations
6. Show Qdrant dashboard with stored vectors
```

### Closing (1 minute):
```
"RegEngine demonstrates how RAG architecture can make document
retrieval intelligent and conversational. The modular design
means each component can be improved independently.

Future work includes: multi-language support, larger document handling,
and real-time collaboration features.

Thank you."
```

### Expected Questions & Answers:

**Q: How is this different from Google?**
```
A: Google searches the entire internet. RegEngine searches ONLY your
   private documents. It's like having a personal assistant who has
   read all your files and can answer questions about them.
```

**Q: What if the answer is wrong?**
```
A: We have an evaluation pipeline that checks relevance, faithfulness,
   and completeness. The system also shows source documents so users
   can verify the answer themselves.
```

**Q: Can it handle any file format?**
```
A: Currently PDF, DOCX, TXT, and MD. We can easily add more formats
   by extending the loader module.
```

**Q: How many documents can it handle?**
```
A: Qdrant can handle millions of vectors. Our current bottleneck would
   be the embedding step, but we can optimize with batching.
```

**Q: Why Qdrant and not other vector DBs?**
```
A: Qdrant is open-source, fast, easy to set up with Docker,
   and has a great Python client. Alternatives include Pinecone,
   Weaviate, and Milvus.
```

---

## 14. FAQ — Interview/Common Questions {#14-faq}

### RAG ke baare mein:
```
Q: RAG kya hai?
A: Retrieval-Augmented Generation. Ye ek technique hai jismein pehle
   relevant documents dhundte hain (Retrieval), phir unhe LLM ko dete
   hain taaki wo context ke basis pe answer generate kare (Generation).

Q: RAG sirf LLM se better kyun hai?
A: Sirf LLM ke paas training data tak access hai. RAG ke paas tumhara
   actual documents hain. Toh answers zyada accurate aur up-to-date hote hain.

Q: Chunking kyun zaroori hai?
A: LLM ke paas limited context window hai. Agar poora document daal
   do toh kuch yaad nahi rakhega. Chhote chunks se relevant info
   milti hai aur LLM better answer deta hai.
```

### Technical Questions:
```
Q: Embedding model kyun all-MiniLM-L6-v2?
A: Ye fast hai, free hai, aur 384 dimensions mein accurate results
   deta hai. Production mein larger models use kar sakte hain.

Q: Cosine similarity kya hai?
A: Ye measure karta hai ki do vectors kitne similar hain.
   1 = bilkul same, 0 = bilkul alag, -1 = ulta.

Q: FastAPI vs Flask?
A: FastAPI asynchronous hai (fast), automatic docs deta hai,
   aur type checking built-in hai. Flask se better hai modern APIs ke liye.
```

---

## 15. Current Status — Abhi Kya Ban Gaya {#15-status}

### ✅ Done (Phase 1 Complete):
- [x] Project structure
- [x] Docker setup (Qdrant + API)
- [x] GitHub repo + branches
- [x] Team roles + roadmaps
- [x] API: 5 endpoints working
- [x] Ingestion: loader + chunker + embedder
- [x] Retrieval: search + context builder
- [x] Eval: metrics (relevance, faithfulness, completeness)
- [x] Tested: upload → store → query → answer flow

### ⏳ Pending:
- [ ] OpenAI API key for LLM answers
- [ ] Dashboard (Megha working on it)
- [ ] Production deployment
- [ ] More document formats
- [ ] Multi-collection support
- [ ] Performance optimization

### 🔗 Key Links:
```
GitHub:     https://github.com/NOVA-RRMV/nova-rrmv-local
API Docs:   http://localhost:8000/docs (when running)
Dashboard:  http://localhost:8501 (when running)
Qdrant:     http://localhost:6333/dashboard (when running)
```

---

*Last updated: July 21, 2026*
*Team: Nova RRMV (Mrity, Rakhi, Viraj, Megha)*
