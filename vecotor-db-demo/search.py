import psycopg2
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

conn = psycopg2.connect(
    host="localhost",
    port=5433,
    database="vectordb",
    user="vectoruser",
    password="vectorpass",
)

cursor = conn.cursor()

query = "My gateway is not communicating with the MQTT broker"

query_embedding = model.encode(query).tolist()

cursor.execute(
    """
    SELECT
        content,
        embedding <=> %s::vector AS distance
    FROM documents
    ORDER BY embedding <=> %s::vector
    LIMIT 3
    """,
    (query_embedding, query_embedding),
)

results = cursor.fetchall()

print("\nQuery:")
print(query)

print("\nMost relevant documents:")

for content, distance in results:
    print(f"\nDistance: {distance:.4f}")
    print(content)

cursor.close()
conn.close()