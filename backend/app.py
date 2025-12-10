import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import function_tool
import cohere
from qdrant_client import QdrantClient
import uvicorn

# Load environment variables
load_dotenv()

# Initialize clients
try:
    groq_api_key = os.getenv("GROQ_API_KEY")
    cohere_api_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not all([groq_api_key, cohere_api_key, qdrant_url, qdrant_api_key]):
        raise ValueError("One or more environment variables are not set.")

    provider = AsyncOpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
    model = OpenAIChatCompletionsModel(model="llama-3.3-70b-versatile", openai_client=provider)
    cohere_client = cohere.Client(cohere_api_key)
    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

except (ValueError, Exception) as e:
    # Handle initialization errors
    print(f"Error during client initialization: {e}")
    # You might want to exit or handle this more gracefully
    # For now, we'll let it proceed but endpoints will likely fail
    provider = None
    model = None
    cohere_client = None
    qdrant = None


app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    if not cohere_client:
        raise HTTPException(status_code=500, detail="Cohere client not initialized")
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",
        texts=[text],
    )
    return response.embeddings[0]

@function_tool
def retrieve(query: str):
    """
    Retrieves relevant text from the Qdrant collection based on the query.
    """
    if not qdrant:
        raise HTTPException(status_code=500, detail="Qdrant client not initialized")
    try:
        embedding = get_embedding(query)
        result = qdrant.search(
            collection_name="humanoid_ai_book",
            query_vector=embedding,
            limit=5,
            with_payload=True
        )
        # The user's provided snippet had an error here, it should be qdrant.search and with_payload
        # Also, the return was `point.payload["text"]`, but it should probably include sources
        # For now, I'm keeping it as is, but this might need refinement.
        # Let's check what the payload looks like
        # It seems payload is a dict, and the user wants the 'text' and 'url'
        return [{"text": point.payload["text"], "url": point.payload.get("url", "N/A")} for point in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during retrieval: {e}")


agent = Agent(
    name="Assistant",
    instructions="""
You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
To answer the user question, first call the tool `retrieve` with the user query.
Use ONLY the returned content from `retrieve` to answer.
If the answer is not in the retrieved content, say "I don't know".
""",
    model=model,
    tools=[retrieve]
) if model else None

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(request: ChatRequest):
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    try:
        result = await Runner.run(
            agent,
            input=request.message,
        )
        # The result from retrieve is a list of dicts with 'text' and 'url'
        # We need to extract the sources and the response
        sources = []
        if result.intermediate_steps:
            for step in result.intermediate_steps:
                if step.tool_name == 'retrieve':
                    # The tool output is a list of dicts
                    for item in step.tool_output:
                        if isinstance(item, dict) and 'url' in item:
                            sources.append(item['url'])

        return {"response": str(result.final_output), "sources": list(set(sources))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during chat processing: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)