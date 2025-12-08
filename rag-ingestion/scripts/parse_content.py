import os
import re
from typing import List, Dict, Tuple
from markdown_it import MarkdownIt
from slugify import slugify

def extract_frontmatter(content: str) -> Tuple[Dict, str]:
    """Extracts YAML front matter and remaining content."""
    match = re.match(r'---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if match:
        frontmatter_str = match.group(1)
        body = match.group(2)
        frontmatter = {}
        for line in frontmatter_str.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"') # Basic parsing, handle quoted strings
        return frontmatter, body
    return {}, content

def parse_markdown_to_chunks(filepath: str, max_chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict]:
    """
    Parses a Markdown file into text chunks with metadata.
    Implements a heading-aware chunking strategy.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        full_content = f.read()

    frontmatter, content_body = extract_frontmatter(full_content)

    md = MarkdownIt()
    tokens = md.parse(content_body)

    chunks = []
    current_chunk_text = ""
    current_metadata = {
        "source_filepath": filepath,
        "source_chapter_id": frontmatter.get('id', os.path.basename(filepath).replace('.md', '')),
        "source_chapter_title": frontmatter.get('title', os.path.basename(filepath).replace('.md', '')),
        "source_slug": frontmatter.get('slug', f"/docs/{os.path.basename(filepath).replace('.md', '')}"),
        "source_section": "Introduction"
    }

    def add_chunk_if_valid():
        nonlocal current_chunk_text
        if current_chunk_text.strip():
            chunk_id = slugify(f"{current_metadata['source_chapter_id']}-{current_metadata['source_section']}-{len(chunks)}")
            chunks.append({
                "id": chunk_id,
                "content": current_chunk_text.strip(),
                "metadata": current_metadata.copy() # Ensure a copy
            })
            current_chunk_text = ""

    for token in tokens:
        if token.type == 'heading_open':
            add_chunk_if_valid() # Start new chunk on new heading
            # Extract heading level and content
            level = int(token.tag[1])
            heading_content = tokens[tokens.index(token) + 1].content
            current_metadata["source_section"] = heading_content
            current_chunk_text += f"\n{'#' * level} {heading_content}\n"
        elif token.type == 'inline':
            current_chunk_text += token.content
        elif token.type == 'fence' and token.info in ['python', 'js', 'bash', 'json', 'yaml', 'cpp', 'c']: # Code blocks
            add_chunk_if_valid() # Code block is a new chunk
            code_chunk_id = slugify(f"{current_metadata['source_chapter_id']}-{current_metadata['source_section']}-code-{len(chunks)}")
            chunks.append({
                "id": code_chunk_id,
                "content": f"``` {token.info}\n{token.content}\n```",
                "metadata": {
                    **current_metadata.copy(), # Inherit metadata
                    "type": "code_block",
                    "language": token.info
                }
            })
        elif token.type == 'image':
            # Handle images: could extract alt text or caption as metadata
            pass # For now, skip images

    add_chunk_if_valid() # Add any remaining text

    # Further split long chunks into smaller, overlapping chunks
    final_chunks = []
    for chunk in chunks:
        words = chunk["content"].split()
        if len(words) > max_chunk_size:
            for i in range(0, len(words), max_chunk_size - chunk_overlap):
                sub_chunk_words = words[i:i + max_chunk_size]
                sub_chunk_content = " ".join(sub_chunk_words)
                sub_chunk_id = f"{chunk['id']}_{len(final_chunks)}"
                final_chunks.append({
                    "id": sub_chunk_id,
                    "content": sub_chunk_content,
                    "metadata": chunk["metadata"] # Copy existing metadata
                })
        else:
            final_chunks.append(chunk)

    return final_chunks

if __name__ == "__main__":
    # Example usage (adjust path to your Docusaurus docs)
    # This script is meant to be run from the root of the repo,
    # so 'docs' is the correct relative path.
    sample_filepath = "docs/chapter-01.md" 
    
    if os.path.exists(sample_filepath):
        parsed_chunks = parse_markdown_to_chunks(sample_filepath, max_chunk_size=500, chunk_overlap=100)
        for i, chunk in enumerate(parsed_chunks):
            print(f"---" * 10 + f" Chunk {i+1} ---")
            print(f"ID: {chunk['id']}")
            print(f"Source Chapter ID: {chunk['metadata']['source_chapter_id']}")
            print(f"Source Section: {chunk['metadata']['source_section']}")
            print(f"Content ({len(chunk['content'].split())} words):\n{chunk['content'][:200]}...\n")
    else:
        print(f"Sample file not found: {sample_filepath}")
        print("Please ensure the book content is available at the expected path (e.g., 'docs/chapter-01.md').")
