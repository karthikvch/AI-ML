import json

import psycopg2
import requests
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5434,
    "database": "ragdb",
    "user": "raguser",
    "password": "ragpass",
}

OLLAMA_URL = "http://localhost:11434/api/generate"

# Use the model you currently have.
# If you later install qwen3:4b, change this to "qwen3:4b".
OLLAMA_MODEL = "qwen3:8b"

TOP_K = 5


# --------------------------------------------------
# Embedding Model
# --------------------------------------------------

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# Vector Search
# --------------------------------------------------

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


# --------------------------------------------------
# Build Context
# --------------------------------------------------

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


# --------------------------------------------------
# Call Ollama
# --------------------------------------------------

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


# --------------------------------------------------
# Main RAG Pipeline
# --------------------------------------------------

def main():

    question = input("\nAsk your IoT question: ").strip()

    if not question:
        print("Question cannot be empty.")
        return

    print("\n" + "=" * 70)
    print("RAG PIPELINE")
    print("=" * 70)

    # ----------------------------------------------
    # Step 1: Retrieval
    # ----------------------------------------------

    print("\n1. Retrieving relevant documents...")

    results = retrieve_documents(question)

    if not results:
        print("No relevant documents found.")
        return

    # ----------------------------------------------
    # Step 2: Build context
    # ----------------------------------------------

    print("2. Building context...")

    context = build_context(results)

    # ----------------------------------------------
    # Step 3: Generate answer
    # ----------------------------------------------

    print("3. Sending context to Ollama...")

    answer = generate_answer(
        question,
        context,
    )

    # ----------------------------------------------
    # Step 4: Display answer
    # ----------------------------------------------

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)

    print(answer)

    # ----------------------------------------------
    # Step 5: Display sources
    # ----------------------------------------------

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