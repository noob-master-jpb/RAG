import chromadb
from google import genai
from pprint import pprint
import os
from dotenv import load_dotenv



load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY")
GENAI_MODEL = os.getenv("GENAI_MODEL")

DB_API_KEY = os.getenv("DB_API_KEY")
DB_NAME = os.getenv("DB_NAME")
DB_LOGIN_ID = os.getenv("DB_LOGIN_ID") # tenant id

Ai = genai.Client(api_key=GENAI_API_KEY)


def gemini(prompt):
    response = Ai.models.generate_content(
        model=GENAI_MODEL,
        contents=prompt,
    )
    return response.text

client = chromadb.CloudClient(
  api_key=DB_API_KEY,
  tenant=DB_LOGIN_ID,
  database=DB_NAME
)

collection = client.get_or_create_collection(name = "data")

data = open("test.txt", "r").read()


def chunk_text(text, chunk_size=20, overlap=5):
    chunks = []
    text = text.replace("\n", " ")
    text = text.split(" ")
    for i in range(0, len(text), chunk_size - overlap):
        chunk = " ".join(text[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# print(chunk_text(data))

# chunks = chunk_text(data, chunk_size=20, overlap=5)

def load_data(chunks, collection):
    for chunk in chunks:
        collection.add(
            documents=[chunk],
            ids=[f"id_{hash(chunk)}"]
        )

def get_context(query, collection, n_results=4):
    result = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    context = "\n".join([item for item in result['documents'][0]])
    return context




query = "explain types of learining in detail"

context = get_context(query, collection, n_results=4)

prompt = f"""
Context:
{context}

Question: {query}
Answer the question based on the context above. And do not mention about the context in the answer.
"""

print(gemini(prompt))