# Local RAG IoT Assistant

A hands-on local Retrieval-Augmented Generation (RAG) project built to understand how vector databases, embeddings, semantic search, and local LLMs work together.

The project uses:

* Python
* Sentence Transformers
* PostgreSQL
* pgvector
* Ollama
* Qwen3
* Docker

The goal is to understand RAG **from the fundamentals**, without hiding the architecture behind frameworks such as LangChain.

---

# 1. Project Goal

Build a local IoT troubleshooting assistant that can answer questions using a private knowledge base.

Example:

> My device went offline after an OTA update. What should I check?

The application retrieves relevant information from local IoT documentation and provides the retrieved context to a local LLM.

The complete pipeline is:

```text
Documents
    ↓
Chunking
    ↓
Embedding Model
    ↓
Vector Database
    ↓
Semantic Retrieval
    ↓
Relevant Context
    ↓
Local LLM
    ↓
Grounded Answer
```

---

# 2. Why RAG?

A normal LLM works approximately like:

```text
Question
   ↓
LLM
   ↓
Answer
```

The problem is that the LLM may not know our private or project-specific information.

RAG adds a retrieval layer:

```text
Question
   ↓
Retrieve relevant knowledge
   ↓
Add knowledge to prompt
   ↓
LLM
   ↓
Answer
```

This allows an LLM to answer questions using information from our own documents.

---

# 3. Local Machine

The project is designed to run on a local Linux machine.

Current machine configuration:

```text
CPU:
12th Gen Intel Core i7-1255U × 12

RAM:
16 GB

GPU:
Mesa Intel Graphics (ADL GT2)

Disk:
512 GB

OS:
Ubuntu/Linux
```

The system uses CPU-based inference because the machine has integrated Intel graphics rather than a dedicated NVIDIA GPU.

---

# 4. Architecture

Current architecture:

```text
                         LOCAL MACHINE
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
     Documents           Embedding Model       Ollama
      (*.md)          all-MiniLM-L6-v2        Qwen3
          │                   │                   │
          ▼                   ▼                   │
       Chunking          384 Dimensions           │
          │                   │                   │
          └───────────┐       │                   │
                      ▼       ▼                   │
                 PostgreSQL + pgvector            │
                      │                           │
                      │                           │
                 User Question                    │
                      │                           │
                      ▼                           │
                Query Embedding                   │
                      │                           │
                      ▼                           │
                Vector Search                     │
                      │                           │
                      ▼                           │
                Top K Chunks                      │
                      │                           │
                      ▼                           │
               Context Building                   │
                      │                           │
                      └───────────────┬───────────┘
                                      ▼
                              Question + Context
                                      │
                                      ▼
                                   Qwen3
                                      │
                                      ▼
                                   Answer
```

---

# 5. Technology Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python                |
| Database             | PostgreSQL 16         |
| Vector Database      | PostgreSQL + pgvector |
| Embedding Model      | `all-MiniLM-L6-v2`    |
| Embedding Dimension  | 384                   |
| Local LLM            | Ollama + Qwen3        |
| Containerization     | Docker                |
| API                  | Ollama HTTP API       |
| Operating System     | Ubuntu/Linux          |

---

# 6. Project Structure

Current project:

```text
local-rag-iot/
│
├── .venv/
│
├── documents/
│   ├── mqtt.md
│   ├── ota.md
│   ├── certificates.md
│   ├── heartbeat.md
│   └── onboarding.md
│
├── docker-compose.yml
├── init.sql
├── requirements.txt
│
├── test_embedding.py
├── ingest.py
├── search.py
├── rag.py
└── app.py
```

---

# 7. Step 1 — Create the Project

Create the project:

```bash
mkdir -p ~/AI-ML/local-rag-iot
cd ~/AI-ML/local-rag-iot
```

Create the directories:

```bash
mkdir documents
```

Create the files:

```bash
touch docker-compose.yml
touch init.sql
touch requirements.txt
touch test_embedding.py
touch ingest.py
touch search.py
touch rag.py
touch app.py
```

---

# 8. Step 2 — Python Virtual Environment

Create:

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Verify:

```bash
python --version
```

Example:

```text
Python 3.10.12
```

---

# 9. Step 3 — PostgreSQL + pgvector

PostgreSQL is used as the vector database.

The pgvector extension allows PostgreSQL to store and search embeddings.

## docker-compose.yml

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: local-rag-postgres
    environment:
      POSTGRES_DB: ragdb
      POSTGRES_USER: raguser
      POSTGRES_PASSWORD: ragpass
    ports:
      - "5434:5432"
    volumes:
      - rag_pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  rag_pgdata:
```

Port `5434` is used on the host to avoid conflicts with other PostgreSQL instances.

Start PostgreSQL:

```bash
docker compose up -d
```

Check:

```bash
docker ps
```

---

# 10. Database Initialization

## init.sql

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,

    document_name TEXT NOT NULL,

    chunk_index INTEGER NOT NULL,

    content TEXT NOT NULL,

    metadata JSONB,

    embedding VECTOR(384),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX document_chunks_document_idx
ON document_chunks(document_name);
```

The important column is:

```sql
embedding VECTOR(384)
```

because our embedding model produces 384-dimensional vectors.

---

# 11. Verify pgvector

Connect:

```bash
docker exec -it local-rag-postgres \
psql -U raguser -d ragdb
```

Check:

```sql
SELECT extname FROM pg_extension;
```

Expected:

```text
vector
```

Test vector functionality:

```sql
SELECT '[1,2,3]'::vector;
```

Test vector distance:

```sql
SELECT '[1,2,3]'::vector <=> '[1,2,4]'::vector;
```

`<=>` is the pgvector cosine-distance operator.

Exit:

```sql
\q
```

---

# 12. Step 4 — Knowledge Base

The first knowledge base contains IoT troubleshooting information.

Documents:

```text
documents/
├── mqtt.md
├── ota.md
├── certificates.md
├── heartbeat.md
└── onboarding.md
```

Examples of information contained in these documents:

### MQTT

* MQTT connectivity
* TLS
* certificates
* broker connectivity
* heartbeat
* disconnects

### OTA

* OTA update failures
* device reboot
* device offline after OTA
* OTA agent
* logs

### Certificates

* certificate expiration
* certificate chain
* private keys
* CA
* TLS

### Heartbeat

* device health
* connectivity
* heartbeat failures
* edge agent

### Onboarding

* device registration
* claim code
* device identity
* certificates
* MQTT
* initial heartbeat

---

# 13. Step 5 — Embedding Model

Install dependencies.

## requirements.txt

```text
sentence-transformers
psycopg2-binary
requests
```

Install:

```bash
pip install -r requirements.txt
```

The embedding model used is:

```text
all-MiniLM-L6-v2
```

It converts text into a 384-dimensional vector.

Conceptually:

```text
"My device cannot connect to MQTT"
                 ↓
        Embedding Model
                 ↓
[0.12, -0.03, 0.77, ...]
                 ↓
           384 values
```

---

# 14. Test Embeddings

## test_embedding.py

```python
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

text = "My IoT device cannot connect to MQTT"

embedding = model.encode(text)

print("Text:")
print(text)

print()
print("Embedding dimensions:")
print(len(embedding))

print()
print("First 10 values:")
print(embedding[:10])
```

Run:

```bash
python test_embedding.py
```

Expected:

```text
Embedding dimensions:
384
```

---

# 15. Step 6 — Document Ingestion

The ingestion pipeline is:

```text
Markdown Files
      ↓
Read Document
      ↓
Split Into Chunks
      ↓
Generate Embeddings
      ↓
Store in PostgreSQL
```

## ingest.py

```python
from pathlib import Path

import psycopg2
import psycopg2.extras
from sentence_transformers import SentenceTransformer


DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5434,
    "database": "ragdb",
    "user": "raguser",
    "password": "ragpass",
}

DOCUMENTS_DIR = Path("documents")

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_chunks(text: str, chunk_size: int = 500) -> list[str]:

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)

    return chunks


def main():

    print("Connecting to PostgreSQL...")

    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    print("Connected successfully.")

    markdown_files = list(DOCUMENTS_DIR.glob("*.md"))

    print(f"Found {len(markdown_files)} documents.")

    total_chunks = 0

    for document_path in markdown_files:

        print()
        print(f"Processing: {document_path.name}")

        text = document_path.read_text(encoding="utf-8")

        chunks = create_chunks(text)

        print(f"Created {len(chunks)} chunks.")

        for chunk_index, chunk in enumerate(chunks):

            print(
                f"  Embedding chunk {chunk_index + 1}/{len(chunks)}"
            )

            embedding = model.encode(chunk).tolist()

            metadata = {
                "source": document_path.name,
                "type": "iot-knowledge",
            }

            cursor.execute(
                """
                INSERT INTO document_chunks
                (
                    document_name,
                    chunk_index,
                    content,
                    metadata,
                    embedding
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    document_path.name,
                    chunk_index,
                    chunk,
                    psycopg2.extras.Json(metadata),
                    embedding,
                ),
            )

            total_chunks += 1

    conn.commit()

    cursor.close()
    conn.close()

    print()
    print("=" * 50)
    print("Ingestion completed.")
    print(f"Documents processed: {len(markdown_files)}")
    print(f"Total chunks inserted: {total_chunks}")
    print("=" * 50)


if __name__ == "__main__":
    main()
```

Run:

```bash
python ingest.py
```

---

# 16. Verify Ingested Data

Connect:

```bash
docker exec -it local-rag-postgres \
psql -U raguser -d ragdb
```

Check:

```sql
SELECT COUNT(*) FROM document_chunks;
```

View documents:

```sql
SELECT
    id,
    document_name,
    chunk_index,
    LEFT(content, 100) AS content_preview
FROM document_chunks
ORDER BY id;
```

Check embedding dimensions:

```sql
SELECT
    id,
    document_name,
    vector_dims(embedding) AS dimensions
FROM document_chunks;
```

Expected:

```text
384
```

---

# 17. Step 7 — Semantic Search

Semantic search converts the user's question into an embedding and searches for the closest vectors.

Pipeline:

```text
Question
   ↓
Embedding
   ↓
Query Vector
   ↓
pgvector
   ↓
Similarity Search
   ↓
Top K Results
```

## search.py

```python
import psycopg2
from sentence_transformers import SentenceTransformer


DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5434,
    "database": "ragdb",
    "user": "raguser",
    "password": "ragpass",
}


model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query: str, top_k: int = 5):

    print("Creating query embedding...")

    query_embedding = model.encode(query).tolist()

    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            document_name,
            chunk_index,
            content,
            embedding <=> %s::vector AS distance
        FROM document_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (
            query_embedding,
            query_embedding,
            top_k,
        ),
    )

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results
```

The important query is:

```sql
ORDER BY embedding <=> %s::vector
```

This finds the chunks whose embeddings are closest to the question embedding.

---

# 18. Example Semantic Query

Question:

```text
My device went offline after an OTA update. What should I check?
```

The vector search may return:

```text
1. ota.md
2. heartbeat.md
3. mqtt.md
4. certificates.md
5. onboarding.md
```

The exact ranking depends on the embeddings.

---

# 19. Step 8 — Install Ollama

Ollama is used to run a local LLM.

Install:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify:

```bash
ollama --version
```

Check service:

```bash
systemctl status ollama
```

---

# 20. Local LLM

The current model downloaded for testing is:

```text
qwen3:8b
```

Download:

```bash
ollama pull qwen3:8b
```

Check:

```bash
ollama list
```

Run:

```bash
ollama run qwen3:8b
```

Example:

```text
Explain RAG in simple terms.
```

Exit:

```text
/bye
```

---

# 21. Local Hardware Consideration

Current machine:

```text
16 GB RAM
Intel i7-1255U
Integrated Intel GPU
```

Qwen3 8B runs using CPU:

```text
PROCESSOR: 100% CPU
```

The 8B model consumed approximately:

```text
~5.9 GB
```

during the test and caused significant swap usage.

Therefore, a smaller model is recommended for comfortable long-term local development.

The RAG architecture does not depend on the LLM being 8B.

We can later switch to a smaller model such as a 4B-class model.

---

# 22. Step 9 — Complete RAG Pipeline

The complete pipeline is:

```text
                       USER QUESTION
                             │
                             ▼
                  all-MiniLM-L6-v2
                             │
                             ▼
                       Query Vector
                             │
                             ▼
                    PostgreSQL/pgvector
                             │
                             ▼
                      Top 5 Chunks
                             │
                             ▼
                     Context Building
                             │
                             ▼
                  Question + Context
                             │
                             ▼
                       Ollama / Qwen
                             │
                             ▼
                         ANSWER
```

---

# 23. `rag.py`

The complete first RAG implementation:

```python
import psycopg2
import requests
from sentence_transformers import SentenceTransformer


DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5434,
    "database": "ragdb",
    "user": "raguser",
    "password": "ragpass",
}

OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODEL = "qwen3:8b"

TOP_K = 5


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_documents(query: str, top_k: int = TOP_K):

    print("Creating query embedding...")

    query_embedding = embedding_model.encode(query).tolist()

    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            document_name,
            chunk_index,
            content,
            embedding <=> %s::vector AS distance
        FROM document_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (
            query_embedding,
            query_embedding,
            top_k,
        ),
    )

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


def build_context(results):

    context_parts = []

    for rank, result in enumerate(results, start=1):

        document_id, document_name, chunk_index, content, distance = result

        context_parts.append(
            f"""
SOURCE {rank}
Document: {document_name}
Chunk: {chunk_index}

{content}
"""
        )

    return "\n".join(context_parts)


def generate_answer(question: str, context: str):

    prompt = f"""
You are an IoT troubleshooting assistant.

Answer the user's question using ONLY the information
provided in the context below.

Do not invent information.

If the context does not contain enough information to answer
the question, clearly say that the available documentation
does not contain enough information.

When possible, mention the source document that supports
your answer.

CONTEXT:
-------------------------
{context}
-------------------------

USER QUESTION:
{question}

ANSWER:
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300,
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]


def main():

    question = input("\nAsk your IoT question: ").strip()

    if not question:
        print("Question cannot be empty.")
        return

    print("\n" + "=" * 70)
    print("RAG PIPELINE")
    print("=" * 70)

    print("\n1. Retrieving relevant documents...")

    results = retrieve_documents(question)

    if not results:
        print("No relevant documents found.")
        return

    print("2. Building context...")

    context = build_context(results)

    print("3. Sending context to Ollama...")

    answer = generate_answer(
        question,
        context,
    )

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)

    print(answer)

    print("\n" + "=" * 70)
    print("SOURCES")
    print("=" * 70)

    for rank, result in enumerate(results, start=1):

        document_id, document_name, chunk_index, content, distance = result

        similarity = 1 - distance

        print(
            f"{rank}. {document_name} "
            f"(chunk {chunk_index}, similarity={similarity:.4f})"
        )


if __name__ == "__main__":
    main()
```

---

# 24. Run the RAG Application

Make sure PostgreSQL is running:

```bash
docker ps
```

Make sure Ollama is available:

```bash
curl http://localhost:11434/api/tags
```

Activate Python:

```bash
source .venv/bin/activate
```

Run:

```bash
python rag.py
```

Ask:

```text
My device went offline after an OTA update. What should I check?
```

The application performs:

```text
1. Create question embedding
2. Search pgvector
3. Retrieve relevant chunks
4. Build context
5. Send question + context to Ollama
6. Generate answer
7. Display sources
```

---

# 25. What We Have Built

We now have a basic end-to-end local RAG system:

```text
                    ┌───────────────┐
                    │ IoT Documents │
                    └───────┬───────┘
                            │
                            ▼
                       Chunking
                            │
                            ▼
                  Embedding Model
                  all-MiniLM-L6-v2
                            │
                            ▼
                 384-dimensional Vector
                            │
                            ▼
                ┌──────────────────────┐
                │ PostgreSQL           │
                │ + pgvector           │
                └──────────┬───────────┘
                           │
                           │
                     User Question
                           │
                           ▼
                    Query Embedding
                           │
                           ▼
                    Vector Search
                           │
                           ▼
                   Relevant Chunks
                           │
                           ▼
                      Build Context
                           │
                           ▼
                 ┌──────────────────────┐
                 │ Ollama               │
                 │ Qwen3                │
                 └──────────┬───────────┘
                            │
                            ▼
                          Answer
```

---

# 26. Important RAG Concepts Learned

So far we have covered:

## Embeddings

Converting text into vectors representing semantic meaning.

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

---

## Vector Database

A database that can store and search vectors efficiently.

Our implementation:

```text
PostgreSQL
     +
pgvector
```

---

## Chunking

Breaking large documents into smaller pieces.

```text
Document
   ↓
Chunk 1
Chunk 2
Chunk 3
...
```

---

## Semantic Search

Finding information based on meaning rather than exact keywords.

```text
Question
   ↓
Vector
   ↓
Similarity Search
   ↓
Relevant Content
```

---

## Retrieval

Selecting the most relevant pieces of information for the question.

```text
Knowledge Base
      ↓
Retriever
      ↓
Top K Chunks
```

---

## Generation

The LLM uses the retrieved context to generate the final response.

```text
Question + Retrieved Context
              ↓
             LLM
              ↓
            Answer
```

---

# 27. RAG vs Normal LLM

Normal LLM:

```text
Question
   ↓
LLM
   ↓
Answer
```

RAG:

```text
Question
   │
   ├──────────────► Vector Search
   │                      │
   │                      ▼
   │                 Relevant Data
   │                      │
   └──────────────┬───────┘
                  ▼
                 LLM
                  │
                  ▼
                Answer
```

The retrieval step gives the LLM access to external/private knowledge.

---

# 28. Current Limitations

This is intentionally a **learning implementation**, not production RAG.

Current limitations include:

### Simple chunking

Current implementation:

```python
words[i : i + 500]
```

Better approaches will include:

* Paragraph-aware chunking
* Sentence-aware chunking
* Recursive chunking
* Section-aware chunking
* Chunk overlap

---

### Vector search only

Currently:

```text
Vector Search
```

A production system may use:

```text
Hybrid Search
├── Vector Search
└── Keyword Search
```

---

### No reranking

Currently:

```text
Top K vector results
       ↓
LLM
```

A better architecture:

```text
Vector Search
      ↓
Top 20
      ↓
Reranker
      ↓
Top 5
      ↓
LLM
```

---

### No evaluation framework

We still need to measure:

* Retrieval precision
* Recall
* Answer quality
* Groundedness
* Hallucination
* Context relevance

---

# 29. Future RAG Roadmap

The planned progression is:

```text
PHASE 1
Basic Vector Database
        ↓
PHASE 2
Document Ingestion
        ↓
PHASE 3
Semantic Retrieval
        ↓
PHASE 4
Local LLM + RAG
        ↓
PHASE 5
Better Chunking
        ↓
PHASE 6
Hybrid Search
        ↓
PHASE 7
Reranking
        ↓
PHASE 8
Query Rewriting
        ↓
PHASE 9
RAG Evaluation
        ↓
PHASE 10
Production Architecture
```

---

# 30. Future Integration With EDP

Once the standalone RAG system is understood, it can be integrated with the Edge Device Platform.

The future architecture could look like:

```text
                         EDP
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
 Device Registry       OTA Data          Device Logs
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                          ▼
                     RAG Pipeline
                          │
              ┌───────────┴───────────┐
              │                       │
        Vector Search             SQL/Data
              │                       │
              └───────────┬───────────┘
                          ▼
                        LLM
                          │
                          ▼
                   EDP AI Assistant
```

Eventually a user could ask:

```text
Why did device dev-f87080d8 go offline
after yesterday's OTA update?
```

The system could combine:

* Device information
* OTA history
* Heartbeat data
* MQTT events
* Device logs
* Certificates
* Troubleshooting documentation

and produce a grounded diagnostic response.

---

# 31. Important Principle

For learning RAG, don't immediately hide the architecture behind a framework.

First understand:

```text
Chunking
   ↓
Embedding
   ↓
Vector Storage
   ↓
Similarity Search
   ↓
Retrieval
   ↓
Context
   ↓
LLM
```

Once these concepts are clear, frameworks such as LangChain or LlamaIndex become much easier to understand and evaluate.

---

# 32. Current Status

The local project currently has:

```text
[x] Python environment
[x] Docker
[x] PostgreSQL
[x] pgvector
[x] Knowledge documents
[x] Document chunking
[x] Embedding model
[x] Vector ingestion
[x] Semantic search
[x] Ollama
[x] Local Qwen model
[x] End-to-end RAG pipeline
```

Next major focus:

```text
[ ] Improve chunking
[ ] Improve retrieval
[ ] Hybrid search
[ ] Reranking
[ ] Citations
[ ] RAG evaluation
[ ] Better prompts
[ ] Query rewriting
[ ] API layer
[ ] EDP integration
```

---

# 33. Final Mental Model

The simplest way to remember RAG is:

```text
RAG = Retrieve + Generate
```

More precisely:

```text
                   RETRIEVE
                      │
Question ─────────────┤
                      ▼
                Relevant Knowledge
                      │
                      ▼
                   GENERATE
                      │
                      ▼
                    Answer
```

The vector database does **not** generate the answer.

The embedding model does **not** generate the answer.

The LLM does **not** search the vector database by itself.

Each component has a specific responsibility:

```text
Embedding Model
      ↓
Understand semantic similarity

Vector Database
      ↓
Find relevant knowledge

Retriever
      ↓
Select context

LLM
      ↓
Generate the answer
```

This separation of responsibilities is the foundation of the RAG architecture.
