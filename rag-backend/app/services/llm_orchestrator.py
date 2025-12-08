from typing import List, Dict, Optional
import os
from openai import OpenAI

# Initialize OpenAI client to work with Gemini API via OpenAI-compatible endpoint
gemini_api_key = os.environ.get("GEMINI_API_KEY")
gemini_base_url = os.environ.get("GEMINI_BASE_URL")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable must be set.")
if not gemini_base_url:
    raise ValueError("GEMINI_BASE_URL environment variable must be set.")

client = OpenAI(api_key=gemini_api_key, base_url=gemini_base_url)

def generate_llm_response(query: str, retrieved_chunks: List[Dict], selected_text: Optional[str] = None) -> Dict:
    """
    Orchestrates the LLM to generate a response based on the query and retrieved chunks.
    Also handles prompt engineering for grounding and evidence citation.
    """
    if not retrieved_chunks:
        return {"answer": "Insufficient data. No relevant information found in the book.", "evidence": []}

    context = "\n\n".join([chunk["content"] for chunk in retrieved_chunks])
    
    if selected_text:
        context = f"User selected the following text: '{selected_text}'\n\n" + context

    # LLM call and prompt engineering
    prompt_messages = [
        {"role": "system", "content": "You are a helpful assistant providing answers based on the provided book content. Answer *only* based on the context given. If the answer is not available in the provided content, state 'Insufficient data.'"},
        {"role": "user", "content": f"Context from the book:\n---\n{context}\n---\nBased *only* on the provided book content, answer the following question: {query}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash", # Using the specified Gemini model
            messages=prompt_messages,
            temperature=0.0, # Make responses deterministic and grounded
            max_tokens=250 # Limit response length
        )
        answer_text = response.choices[0].message.content
    except Exception as e:
        answer_text = f"Error generating response from LLM: {e}"
        print(f"LLM Error: {e}")
    
    # Placeholder for extracting evidence/citations from LLM response
    evidence = [{"source": chunk.get("source", "unknown"), "text": chunk["content"]} for chunk in retrieved_chunks]

    return {"answer": answer_text, "evidence": evidence}

if __name__ == "__main__":
    # Example usage - ensure GEMINI_API_KEY and GEMINI_BASE_URL are set in environment
    os.environ["GEMINI_API_KEY"] = "AIzaSyBhF75iGl7KaTk5yYxktUnv8GYUx33u4y8" # Placeholder: Use your actual key
    os.environ["GEMINI_BASE_URL"] = "https://generativelanguage.googleapis.com/v1beta/openai/"

    dummy_chunks = [
        {"content": "Physical AI focuses on embodied intelligence, where an agent learns through interaction with its environment.", "source": "chapter-01"},
        {"content": "Humanoid robotics involves complex kinematics and dynamics for bipedal locomotion and manipulation.", "source": "chapter-03"}
    ]
    
    test_query = "What is embodied intelligence?"
    response = generate_llm_response(test_query, dummy_chunks)
    
    print(f"\n--- LLM Response ---")
    print(f"Answer: {response['answer']}")
    print("Evidence:")
    for ev in response['evidence']:
        print(f"  - Source: {ev['source']}, Text: {ev['text']}")

    test_query_no_data = "What is the meaning of life?"
    response_no_data = generate_llm_response(test_query_no_data, [])
    print(f"\n--- LLM Response (no data) ---")
    print(f"Answer with no data: {response_no_data['answer']}")