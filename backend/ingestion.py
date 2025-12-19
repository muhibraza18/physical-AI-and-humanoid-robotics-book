import requests
import xml.etree.ElementTree as ET
import trafilatura
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import cohere

# -------------------------------------
# CONFIG
# -------------------------------------
# Your Deployment Link:
SITEMAP_URL = "https://physical-ai-and-humanoid-robotics-b-seven.vercel.app/sitemap.xml"
BASE_URL = "https://physical-ai-and-humanoid-robotics-b-seven.vercel.app"
COLLECTION_NAME = "humanoid_ai_book"

cohere_client = cohere.Client("QqHPH4IvJOEym6X7jQ2gCtOBwpbAs28QzArlzcU0")
EMBED_MODEL = "embed-english-v3.0"

# Connect to Qdrant Cloud
qdrant = QdrantClient(
    url="https://a6ae135d-580b-4a28-9803-0adb84ab9d55.us-east4-0.gcp.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Ve7ohi2ESSOOUBF6QFNv-YiZKQeOfQ5d_B5b3PG7ptM" 
)

# -------------------------------------
# Step 1 – Extract URLs from sitemap
# -------------------------------------
def get_all_urls(sitemap_url):
    xml = requests.get(sitemap_url).text
    root = ET.fromstring(xml)

    urls = []
    for child in root:
        loc_tag = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc_tag is not None:
            original_url = loc_tag.text
            
            # FIX: Replace GitHub Pages URL with Vercel URL
            if "muhibraza18.github.io" in original_url:
                # Extract the path after the domain
                path = original_url.split("muhibraza18.github.io")[1]
                corrected_url = BASE_URL + path
                urls.append(corrected_url)
            else:
                urls.append(original_url)

    print("\nFOUND URLS:")
    for u in urls:
        print(" -", u)

    return urls


# -------------------------------------
# Step 2 – Download page + extract text
# -------------------------------------
def extract_text_from_url(url):
    try:
        html = requests.get(url, timeout=10).text
        text = trafilatura.extract(html)

        if not text:
            print(f"[WARNING] No text extracted from: {url}")
            return None

        return text
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


# -------------------------------------
# Step 3 – Chunk the text
# -------------------------------------
def chunk_text(text, max_chars=1200):
    chunks = []
    while len(text) > max_chars:
        split_pos = text[:max_chars].rfind(". ")
        if split_pos == -1:
            split_pos = max_chars
        chunks.append(text[:split_pos].strip())
        text = text[split_pos:].strip()
    if text:  # Add remaining text
        chunks.append(text)
    return chunks


# -------------------------------------
# Step 4 – Create embedding
# -------------------------------------
def embed(text):
    response = cohere_client.embed(
        model=EMBED_MODEL,
        input_type="search_document",  # Use search_document for indexing
        texts=[text],
    )
    return response.embeddings[0]


# -------------------------------------
# Step 5 – Store in Qdrant
# -------------------------------------
def create_collection():
    print("\nCreating Qdrant collection...")
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1024,        # Cohere embed-english-v3.0 dimension
            distance=Distance.COSINE
        )
    )

def save_chunk_to_qdrant(chunk, chunk_id, url):
    vector = embed(chunk)

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=chunk_id,
                vector=vector,
                payload={
                    "url": url,
                    "text": chunk,
                    "chunk_id": chunk_id
                }
            )
        ]
    )


# -------------------------------------
# MAIN INGESTION PIPELINE
# -------------------------------------
def ingest_book():
    urls = get_all_urls(SITEMAP_URL)

    create_collection()

    global_id = 1

    for url in urls:
        print(f"\nProcessing: {url}")
        text = extract_text_from_url(url)

        if not text:
            print(f"Skipping {url} - no content extracted")
            continue

        chunks = chunk_text(text)
        print(f"Created {len(chunks)} chunks from {url}")

        for ch in chunks:
            if len(ch.strip()) > 50:  # Only save chunks with meaningful content
                save_chunk_to_qdrant(ch, global_id, url)
                print(f"✓ Saved chunk {global_id} ({len(ch)} chars)")
                global_id += 1

    print("\n✅ Ingestion completed!")
    print(f"Total chunks stored: {global_id - 1}")


if __name__ == "__main__":
    ingest_book()
