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


def main():

    query = "My device went offline after an OTA update. What should I check?"

    results = search(query)

    context = build_context(results)

    print()
    print("=" * 70)
    print("CONTEXT FOR LLM")
    print("=" * 70)

    print(context)


if __name__ == "__main__":
    main()