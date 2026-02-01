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

# for i in list(Ai.models.list()):
#     print(i.name)
    
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

def chunk_text(text, chunk_size=100, overlap=10):
    chunks = []
    text = text.replace("\n", " ")
    text = text.split(" ")
    for i in range(0, len(text), chunk_size - overlap):
        chunk = " ".join(text[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def load_data(chunks):
    global collection
    try:
        for chunk in chunks:
            collection.add(
                documents=[chunk],
                ids=[f"id_{hash(chunk)}"]
            )
        return True
    except Exception as e:
        print(f"Error loading data: {e}")

def get_context(query, n_results=8):
    global collection
    
    result = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    context = "\n".join([item for item in result['documents'][0]])
    return context

def generate_response(query, past_messages= None):
    global collection
    context = get_context(query, n_results=4)
    if past_messages:
        past = ""
        for msg in past_messages:
            past += f"{msg['role']}: {msg['content']}\n"
    else:
        past = "no conversation yet"
    prompt = f"""
    Past conversation:
    {past}

    Context:
    {context}

    Question: {query}
    
    Guidelines:
    Answer the question based on the context above. And do not mention about the context in the answer. And if the answer is not found in do not use the context but reply normally based on your knowledge.
    Use markdown formatting for any code snippets in your response.
    do not use any other formatting other than markdown unless required.
    """

    return gemini(prompt)

# pprint(collection.query(
#     query_texts=["What is bitnet"],
#     n_results=5
# ))

