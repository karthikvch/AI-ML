import os
import warnings

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

warnings.filterwarnings(
    "ignore",
    message="Direct use of automatic function calling.*",
    category=UserWarning,
)

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY is missing. Set it in your environment or .env file.")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=api_key,
)

response = llm.invoke("What is Java? Explain it in simple words.")
print(response.content)