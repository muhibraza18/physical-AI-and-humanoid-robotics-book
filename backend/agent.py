import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import function_tool
import cohere
from qdrant_client import QdrantClient

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


result = Runner.run_sync(
    agent,
    input="what is physical ai?",
)

print(result.final_output)