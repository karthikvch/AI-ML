# Vector Database Learning

## 1. What is a Vector Database?

A vector database stores and searches numerical representations
(embeddings) of data.

## 2. What is an Embedding?

An embedding is a numerical representation of text or other data
that allows semantic similarity comparisons.

Text → Embedding Model → Vector

## 3. Embedding Model

Example:

all-MiniLM-L6-v2

Text → 384-dimensional vector

## 4. Vector Dimension

VECTOR(384) means each vector contains 384 numerical dimensions.

It does NOT mean 384 characters.

## 5. Tokens

A token is a piece of text processed by an AI model.

Input limits are generally measured in tokens.

Tokens ≠ characters.

## 6. PostgreSQL + pgvector

CREATE EXTENSION IF NOT EXISTS vector;

This enables pgvector functionality in PostgreSQL.

## 7. Vector Table

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(384)
);

Each row contains its own 384-dimensional vector.

## 8. Semantic Search

Query
  ↓
Embedding Model
  ↓
Query Vector
  ↓
pgvector
  ↓
Similar Documents


####

Vector DB
   ↓
Embeddings
   ↓
Tokens
   ↓
Chunking
   ↓
Similarity
   ↓
Vector Index
   ↓
RAG
   ↓
LLM