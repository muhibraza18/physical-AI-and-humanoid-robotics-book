from sqlalchemy import Column, Integer, String, DateTime, func, Text
from sqlalchemy.dialects.postgresql import JSONB
from ..core.database import Base # Changed to relative import

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=True) # Optional user ID
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    retrieved_evidence = Column(JSONB, nullable=True) # Store JSON of retrieved chunks
    
    def __repr__(self):
        return f"<ChatHistory(id={self.id}, session_id='{self.session_id}', query='{self.query[:50]}...')>"

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=True) # Optional, links to external user system
    created_at = Column(DateTime, default=func.now(), nullable=False)
    last_accessed = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    extra_metadata = Column(JSONB, nullable=True) # Renamed from metadata
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, session_id='{self.session_id}', user_id='{self.user_id}')>"

class IngestionRecord(Base):
    __tablename__ = "ingestion_records"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String, index=True, nullable=False) # e.g., chapter-01
    filepath = Column(String, nullable=False)
    chunk_count = Column(Integer, nullable=False)
    status = Column(String, nullable=False) # e.g., "completed", "failed"
    ingested_at = Column(DateTime, default=func.now(), nullable=False)
    extra_metadata = Column(JSONB, nullable=True) # Renamed from metadata
    
    def __repr__(self):
        return f"<IngestionRecord(id={self.id}, document_id='{self.document_id}', status='{self.status}')>"