from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
# from dotenv import load_dotenv # Add this import

# os.environ["OPENAI_API_KEY"] = "sk-XXXXXXXXXXXXXXXX"
# os.environ["COHERE_API_KEY"] = "XXXXXXXXXXXXXXXX"
# os.environ["QDRANT_URL"] = "https://your-qdrant-url"
# os.environ["QDRANT_API_KEY"] = "XXXXXXXXXXXXXXXX"

from agent import agent, Runner

app = FastAPI(
    title="RAG Chatbot Backend",
    description="Backend for the RAG Chatbot using OpenAI Agents SDK and Qdrant.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None # Not used by the agent directly, but can be logged

class ChatResponse(BaseModel):
    answer: str
    # Source references are not directly available from the current agent.py output
    # If required, agent.py would need to be modified to return this structured data.
    source_references: list = [] 

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Run the agent with the user's query
        # The agent is synchronous, so we run it directly.
        # In a real-world async app, you might run this in a thread pool executor
        # to avoid blocking the event loop.
        result = await Runner.run(
            agent,
            input=request.query,
        )
        
        answer = result.final_output
        
        # Check if the agent explicitly says "I don't know"
        if "i don't know" in answer.lower():
            answer = "This information is not found in the book."
            
        return ChatResponse(answer=answer)
    except Exception as e:
        # Log the exception for debugging
        print(f"Error processing chat request: {e}")
        return ChatResponse(answer="Sorry, an error occurred while processing your request.")

@app.get("/")
async def root():
    return {"message": "RAG Chatbot Backend is running."}
