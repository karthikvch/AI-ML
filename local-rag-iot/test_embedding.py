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