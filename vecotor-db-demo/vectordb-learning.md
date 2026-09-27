# Local Vector Database — Setup & Learning Guide

## 1. Objective

Build a simple **Vector Database locally** to understand:

* Embeddings
* Vector storage
* Semantic search
* PostgreSQL + pgvector
* Sentence Transformers
* Foundation for RAG (Retrieval-Augmented Generation)

This setup is intended as a learning project and can later be extended into the **Edge Device Platform (EDP)**.

---

# 2. Architecture

```text
                    Local Machine
                         │
                         ▼
                  Python Application
                         │
                         ▼
                Sentence Transformer
                         │
                         ▼
                    Embedding
                 [384 dimensions]
                         │
                         ▼
                PostgreSQL + pgvector
                         │
                         ▼
                  Vector Similarity
                       Search
```

---

# 3. Technologies

| Component            | Technology       |
| -------------------- | ---------------- |
| Programming Language | Python           |
| Database             | PostgreSQL 16    |
| Vector Extension     | pgvector         |
| Embedding Model      | all-MiniLM-L6-v2 |
| Containerization     | Docker           |
| Python DB Driver     | psycopg2         |
| Future API           | FastAPI          |
| Future AI Layer      | LLM + RAG        |

---

# 4. Project Structure

```text
vector-db-demo/
├── docker-compose.yml
├── init.sql
├── requirements.txt
├── app.py
└── search.py
```

---

# 5. Start PostgreSQL + pgvector

`docker-compose.yml`

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: vector-db-postgres
    environment:
      POSTGRES_DB: vectordb
      POSTGRES_USER: vectoruser
      POSTGRES_PASSWORD: vectorpass
    ports:
      - "5433:5432"
    volumes:
      - vector_pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  vector_pgdata:
```

Start:

```bash
docker compose up -d
```

Check:

```bash
docker ps
```

---

# 6. Enable pgvector

`init.sql`

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(384)
);
```

If the database was already initialized:

```bash
docker compose down -v
docker compose up -d
```

> Do not use `docker compose down -v` on a real database because it removes the database volume.

---

# 7. Verify PostgreSQL

Connect:

```bash
docker exec -it vector-db-postgres \
psql -U vectoruser -d vectordb
```

Check the extension:

```sql
SELECT extname FROM pg_extension;
```

Expected:

```text
vector
```

Check the table:

```sql
\d documents
```

Exit:

```sql
\q
```

---

# 8. Create Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

`requirements.txt`

```text
sentence-transformers
psycopg2-binary
```

Install:

```bash
pip install -r requirements.txt
```

---

# 9. Generate an Embedding

Use:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "My IoT device cannot connect to MQTT"

embedding = model.encode(text)

print("Embedding dimensions:", len(embedding))
print("First 10 values:", embedding[:10])
```

Expected:

```text
Embedding dimensions: 384
```

The text is converted into a numerical vector:

```text
Text
 ↓
Embedding Model
 ↓
[0.02, -0.18, 0.44, ...]
```

The vector contains **384 numerical dimensions** for this model.

---

# 10. Insert Documents

Example IoT documents:

```text
How to restart an edge device safely

MQTT connection failures can be caused by network connectivity problems

Device certificates must be renewed before they expire

OTA updates require the device to download and install the firmware package

A device heartbeat indicates that the edge device is online

If a device stops sending heartbeat messages, check the MQTT connection

Device onboarding requires a claim code and device certificate

TLS certificates are used to establish secure MQTT communication
```

Each document goes through:

```text
Document
   ↓
Embedding Model
   ↓
384-dimensional vector
   ↓
PostgreSQL
```

The database stores:

```text
id
content
embedding
```

---

# 11. Semantic Search

Example user query:

```text
My gateway is not communicating with the MQTT broker
```

The query is converted into an embedding.

PostgreSQL then compares that vector with stored vectors.

Example:

```sql
SELECT
    content,
    embedding <=> %s::vector AS distance
FROM documents
ORDER BY embedding <=> %s::vector
LIMIT 3;
```

The `<=>` operator represents **cosine distance** in pgvector.

Smaller distance means greater similarity.

Example:

```text
0.10 → Very similar
0.20 → Similar
0.50 → Somewhat related
0.90 → Very different
```

---

# 12. Why Vector Search Is Different

Traditional SQL search:

```text
"MQTT connection"
        ↓
Find matching words
```

Vector search:

```text
"My gateway is not communicating"
        ↓
Understand semantic meaning
        ↓
Find related concepts
```

For example:

Query:

```text
My gateway is not communicating with the MQTT broker
```

Can find:

```text
MQTT connection failures can be caused by
network connectivity problems
```

even though the wording is different.

---

# 13. What Has Been Built

At this stage we have:

```text
                 User Query
                     │
                     ▼
            Sentence Transformer
                     │
                     ▼
                Query Vector
                     │
                     ▼
          PostgreSQL + pgvector
                     │
                     ▼
             Similarity Search
                     │
                     ▼
           Relevant Documents
```

This is the foundation of a **RAG system**.

---

# 14. What Is RAG?

RAG stands for:

**Retrieval-Augmented Generation**

Basic architecture:

```text
User Question
      │
      ▼
Embedding Model
      │
      ▼
Vector Database
      │
      ▼
Relevant Documents
      │
      ▼
      LLM
      │
      ▼
Generated Answer
```

The vector database retrieves relevant information, and the LLM uses that information to generate the response.

---

# 15. Future EDP + AI Architecture

This can eventually become an AI assistant for the Edge Device Platform.

```text
                    EDP
                     │
        ┌────────────┼────────────┐
        │            │            │
      Devices      Events        Logs
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
                PostgreSQL
                     │
                + pgvector
                     │
                     ▼
                 RAG Layer
                     │
                     ▼
                    LLM
                     │
                     ▼
             AI Device Assistant
```

Example question:

> Why did device dev-123 go offline after the OTA update?

The system could retrieve:

* Device heartbeat information
* MQTT errors
* OTA deployment information
* Certificate information
* Historical troubleshooting documents
* Device events

The LLM can then use those retrieved records to generate an explanation.

---

# 16. Recommended Learning Path

### Phase 1 — Vector Database

* PostgreSQL
* pgvector
* Embeddings
* Vector storage
* Similarity search

### Phase 2 — Python Integration

* Python
* Sentence Transformers
* PostgreSQL connection
* Search API

### Phase 3 — FastAPI

Create APIs such as:

```text
POST /documents
POST /search
GET  /documents
```

### Phase 4 — RAG

Add:

```text
Vector DB
    +
Retriever
    +
LLM
```

### Phase 5 — EDP Integration

Connect the AI layer with:

```text
Device Registry
Heartbeat
MQTT Events
OTA
Device Logs
Alerts
Troubleshooting Knowledge
```

---

# 17. Key Concepts to Remember

### Embedding

Converts information into numbers representing its semantic meaning.

```text
Text → Vector
```

### Vector Database

Stores and searches these vectors.

```text
Vector → Similar Vectors
```

### Semantic Search

Searches based on meaning rather than exact keywords.

### pgvector

PostgreSQL extension that adds vector storage and similarity search.

### RAG

Combines:

```text
Vector Search + LLM
```

to provide answers based on retrieved information.

---

# 18. Final Mental Model

Remember this simple flow:

```text
              DOCUMENT
                  │
                  ▼
            EMBEDDING MODEL
                  │
                  ▼
               VECTOR
                  │
                  ▼
          VECTOR DATABASE
                  │
                  │
             USER QUERY
                  │
                  ▼
            QUERY VECTOR
                  │
                  ▼
          SIMILARITY SEARCH
                  │
                  ▼
        RELEVANT INFORMATION
                  │
                  ▼
                 LLM
                  │
                  ▼
              ANSWER
```

The immediate goal is **not to build a full AI system**.

First understand this pipeline:

**Text → Embedding → Vector DB → Similarity Search**

Once that is clear, adding **RAG + LLM + EDP data** becomes much easier.
