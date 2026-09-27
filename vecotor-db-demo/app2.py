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

documents = [
    "How to restart an edge device safely",
    "MQTT connection failures can be caused by network connectivity problems",
    "Device certificates must be renewed before they expire",
    "OTA updates require the device to download and install the firmware package",
    "A device heartbeat indicates that the edge device is online",
    "If a device stops sending heartbeat messages, check the MQTT connection",
    "Device onboarding requires a claim code and device certificate",
    "TLS certificates are used to establish secure MQTT communication",
]

for text in documents:

    embedding = model.encode(text).tolist()

    cursor.execute(
        """
        INSERT INTO documents (content, embedding)
        VALUES (%s, %s)
        """,
        (text, embedding),
    )

conn.commit()

print(f"Inserted {len(documents)} documents")

cursor.close()
conn.close()