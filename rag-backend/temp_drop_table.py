import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs, urlunparse

async def drop_alembic_version_table():
    """Connects to the database and drops the alembic_version table if it exists."""
    load_dotenv() # Load environment variables from .env file
    
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("Error: DATABASE_URL environment variable must be set.")
        return

    # Parse the database URL
    parsed_url = urlparse(database_url)
    
    # Handle sslmode=require and channel_binding=require
    connect_args = {}
    if parsed_url.scheme == 'postgresql+asyncpg':
        query_params = parse_qs(parsed_url.query)
        if 'sslmode' in query_params:
            if query_params['sslmode'][0] == 'require':
                connect_args['ssl'] = True
            query_params.pop('sslmode', None)
        if 'channel_binding' in query_params:
            # channel_binding is not directly supported in asyncpg connect_args
            # For now, we will remove it. This might be acceptable if not strictly required.
            query_params.pop('channel_binding', None)
            
        # Rebuild the URL without the handled query params
        new_query = '&'.join([f"{k}={v[0]}" for k, v in query_params.items()])
        database_url = urlunparse(parsed_url._replace(query=new_query))

    try:
        engine = create_async_engine(database_url, connect_args=connect_args, echo=True)
        async with engine.connect() as conn:
            await conn.execute(text("DROP TABLE IF EXISTS alembic_version;"))
            await conn.commit()
        print("Successfully dropped alembic_version table (if it existed).")
    except Exception as e:
        print(f"An error occurred while dropping the table: {e}")

if __name__ == "__main__":
    asyncio.run(drop_alembic_version_table())
