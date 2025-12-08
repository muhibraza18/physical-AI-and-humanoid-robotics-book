import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base # Import sessionmaker
from sqlalchemy import text
from urllib.parse import urlparse, parse_qs, urlunparse

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable must be set for Neon Serverless Postgres.")

# Parse the database URL to handle special connection args for asyncpg
parsed_url = urlparse(DATABASE_URL)
connect_args = {}
# Check for sslmode and if it's 'require', configure ssl for asyncpg
if 'sslmode' in parse_qs(parsed_url.query):
    if parse_qs(parsed_url.query)['sslmode'][0] == 'require':
        connect_args['ssl'] = True
    # Rebuild URL without the unsupported sslmode parameter
    query_params = parse_qs(parsed_url.query)
    query_params.pop('sslmode', None)
    DATABASE_URL = urlunparse(parsed_url._replace(query=new_query if (new_query := '&'.join([f"{k}={v[0]}" for k, v in query_params.items()])) else ""))

engine = create_async_engine(DATABASE_URL, connect_args=connect_args, echo=True, future=True) # Added future=True
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) # Renamed AsyncSessionLocal to SessionLocal
Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        # In a real app, use Alembic. For this setup, run_sync is okay.
        # await conn.run_sync(Base.metadata.create_all)
        pass # Alembic will handle table creation
    print("Database connection ready. Schema should be managed by Alembic.")

async def get_db():
    async with SessionLocal() as session: # Use SessionLocal
        try:
            yield session
        finally:
            await session.close()

async def check_db_connection():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("Successfully connected to Neon Serverless Postgres.")
        return True
    except Exception as e:
        print(f"Failed to connect to Neon Serverless Postgres: {e}")
        return False
