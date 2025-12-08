# Placeholder for FastAPI Backend Load Testing Script

import httpx
import asyncio
import time
from typing import List

async def send_chat_query(client: httpx.AsyncClient, query: str, url: str) -> dict:
    try:
        response = await client.post(url, json={"query": query})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e}")
        return {"error": str(e)}
    except httpx.RequestError as e:
        print(f"Request Error: {e}")
        return {"error": str(e)}

async def run_load_test(num_requests: int, concurrency: int, base_url: str):
    chat_url = f"{base_url}/chat"
    queries = ["What is Physical AI?", "Explain embodied intelligence.", "How do humanoid robots move?"] * (num_requests // 3 + 1)
    queries = queries[:num_requests]

    start_time = time.time()
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = []
        for i in range(num_requests):
            task = asyncio.create_task(send_chat_query(client, queries[i], chat_url))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)

    end_time = time.time()
    
    successful_requests = [r for r in results if "answer" in r]
    failed_requests = [r for r in results if "error" in r]

    print(f"\n--- Load Test Results ---")
    print(f"Total Requests: {num_requests}")
    print(f"Successful Requests: {len(successful_requests)}")
    print(f"Failed Requests: {len(failed_requests)}")
    print(f"Total Time: {end_time - start_time:.2f} seconds")
    print(f"Requests per second: {num_requests / (end_time - start_time):.2f}")

if __name__ == "__main__":
    # Example usage:
    # Set your FastAPI backend URL here (e.g., local or deployed) 
    # base_url = "http://localhost:8000" 
    # num_requests = 100
    # concurrency = 10

    # print(f"Running load test for {num_requests} requests with {concurrency} concurrency against {base_url}")
    # asyncio.run(run_load_test(num_requests, concurrency, base_url))
    print("Load testing script placeholder created. Run with actual backend URL.")
