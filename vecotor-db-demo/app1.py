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

text = "My IoT device cannot connect to MQTT"

embedding = model.encode(text).tolist()

cursor.execute(
    """
    INSERT INTO documents (content, embedding)
    VALUES (%s, %s)
    """,
    (text, embedding),
)

conn.commit()

print("Document inserted successfully!")

cursor.close()
conn.close()