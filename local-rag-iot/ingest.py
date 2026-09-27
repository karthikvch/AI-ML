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

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_chunks(text: str, chunk_size: int = 500) -> list[str]:
    """
    Split text into simple word-based chunks.

    This is intentionally simple for our first RAG implementation.
    Later we will improve this with better chunking strategies.
    """

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