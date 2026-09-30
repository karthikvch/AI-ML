# LangChain with Google Gemini

This folder contains a beginner-friendly example for building an AI application using **Python, LangChain, and Google Gemini**.

---

## What is LangChain?

**LangChain** is a framework for developing applications powered by Large Language Models (LLMs).

It helps developers:

* Connect Python applications to LLMs
* Create reusable prompt templates
* Organize multi-step AI workflows
* Integrate external tools and APIs
* Build chatbots and AI assistants

In simple terms:

> **LangChain makes it easier to turn an LLM into a working application.**

---

## What is Google Gemini?

**Google Gemini** is a family of generative AI models from Google.

It can be used for:

* Text generation
* Question answering
* Summarization
* Reasoning
* Conversational AI

---

## End-to-End Flow

```text
User Prompt
     ↓
Python Application
     ↓
LangChain
     ↓
Google Gemini Model
     ↓
Generated Response
```

---

## Prerequisites

Before starting, make sure you have:

* Python 3.10 or above
* `pip` installed
* A valid Google AI API key
* A virtual environment (recommended)

---

## Step 1: Create a Virtual Environment

Go to the AI/ML project directory:

```bash
cd /home/karthik/AI-ML
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

You should see something similar to:

```text
(venv)
```

at the beginning of your terminal prompt.

---

## Step 2: Install Dependencies

Upgrade `pip`:

```bash
pip install --upgrade pip
```

Install the required packages:

```bash
pip install langchain-google-genai python-dotenv
```

### Packages used

| Package                  | Purpose                                 |
| ------------------------ | --------------------------------------- |
| `langchain-google-genai` | Integrates LangChain with Google Gemini |
| `python-dotenv`          | Loads environment variables from `.env` |

---

## Step 3: Create a `.env` File

Create a `.env` file in the project root or inside this folder.

Example:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### Important

**Never hardcode your API key directly in the source code.**

Also make sure `.env` is included in `.gitignore`:

```gitignore
.env
```

This prevents accidentally committing your API key to GitHub.

---

## Step 4: Run the Example

Navigate to the LangChain project:

```bash
cd /home/karthik/AI-ML/langchain
```

Run the Python script:

```bash
python3 LangChain_google.py
```

If everything is configured correctly, the application will send the prompt to Gemini and print the generated response.

---

## What This Script Does

The script performs the following steps:

```text
.env
 ↓
Load GOOGLE_API_KEY
 ↓
Create Gemini model
 ↓
LangChain
 ↓
Send prompt
 ↓
Gemini
 ↓
Generated response
 ↓
Print response
```

More specifically, the script:

1. Loads environment variables from `.env`
2. Reads the Google API key
3. Creates a Gemini model using LangChain
4. Sends a prompt to the model
5. Receives the generated response
6. Prints the response

---

## Model Name Note

Google may update, replace, or retire model names over time.

If you receive an error such as:

```text
404 NOT_FOUND
```

check the currently supported Gemini model name and update the model configuration accordingly.

For example:

```python
model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash"
)
```

> **Note:** Model availability and names can change over time. Always verify the model name supported by your Google AI account/API when troubleshooting a `404 NOT_FOUND` error.

---

## Common Issues

### 1. Missing API Key

If you see:

```text
GOOGLE_API_KEY is missing
```

check that:

* `.env` exists
* The variable is named correctly
* The API key is valid
* The application is running from the expected project directory

Example:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

---

### 2. Model Not Found

If you see:

```text
404 NOT_FOUND
```

the configured model may no longer be available.

Update the model name to one currently supported by your Google AI API/account.

---

### 3. SDK Warnings

You may see warnings related to automatic function calling or SDK behavior.

These warnings are often **non-fatal** and do not necessarily prevent the application from running.

First check whether the script successfully produces a response.

---

## Project Structure

A simple project structure could look like:

```text
langchain/
├── README.md
├── LangChain_google.py
└── .env
```

Recommended:

```text
langchain/
├── README.md
├── LangChain_google.py
├── .env
└── .gitignore
```

Example `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## Next Ideas

Once the basic LangChain + Gemini example works, you can extend the project with:

### 1. Chat Memory

Maintain conversation history so the application can remember previous messages.

```text
User
 ↓
LangChain
 ↓
Conversation History
 ↓
Gemini
 ↓
Response
```

### 2. Document Q&A

Allow users to ask questions about PDFs, Markdown files, or other documents.

```text
Documents
 ↓
Chunking
 ↓
Embeddings
 ↓
Vector Database
 ↓
Relevant Context
 ↓
Gemini
 ↓
Answer
```

### 3. Custom Prompt Templates

Create reusable prompts for specific tasks.

### 4. CSV or Database Search

Connect LangChain to structured data such as:

* CSV files
* PostgreSQL
* Other databases

### 5. AI-Powered APIs or Web Applications

Expose the AI functionality through:

* FastAPI
* REST APIs
* Web applications

### 6. Agent-Based Workflows

Allow the LLM to select and use tools to perform multi-step tasks.

---

## Conclusion

This project provides the basic foundation for building **LangChain + Google Gemini applications**.

The learning path can be:

```text
LangChain + Gemini
        ↓
Prompt Templates
        ↓
Chat Applications
        ↓
Embeddings
        ↓
Vector Database
        ↓
RAG
        ↓
Tools / Agents
        ↓
Production AI Application
```

Once this basic example works, you can move toward more advanced AI use cases such as:

* Chatbots
* Document assistants
* RAG applications
* Database Q&A
* AI-powered APIs
* Agent-based workflows
* IoT/EDP AI assistants
