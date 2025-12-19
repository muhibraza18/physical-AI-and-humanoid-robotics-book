from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import function_tool

# Retrieve API keys and URLs from environment variables

provider = AsyncOpenAI(
    api_key = "AIzaSyAx4QjjFARqHJlnL4-Tcy8qhxJq_xBy6dQ", # Use env var
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=provider
)

import cohere
from qdrant_client import QdrantClient

# Initialize Cohere client
cohere_client = cohere.Client("QqHPH4IvJOEym6X7jQ2gCtOBwpbAs28QzArlzcU0") # Use env var
# Connect to Qdrant
qdrant = QdrantClient(
    url="https://a6ae135d-580b-4a28-9803-0adb84ab9d55.us-east4-0.gcp.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Ve7ohi2ESSOOUBF6QFNv-YiZKQeOfQ5d_B5b3PG7ptM" 
)

def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",  # Use search_query for queries
        texts=[text],
    )
    return response.embeddings[0]  # Return the first embedding


@function_tool
def retrieve(query):
    embedding = get_embedding(query)
    result = qdrant.query_points(
        collection_name="humanoid_ai_book",
        query=embedding,
        limit=5
    )
    return [point.payload["text"] for point in result.points]


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
)
