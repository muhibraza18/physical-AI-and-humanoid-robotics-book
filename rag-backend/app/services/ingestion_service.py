from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from rag_backend.app.models.db_models import IngestionRecord
from datetime import datetime

class IngestionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_ingestion(
        self,
        document_id: str,
        filepath: str,
        chunk_count: int,
        status: str = "completed",
        metadata: Optional[Dict] = None,
    ) -> IngestionRecord:
        """Records an ingestion event in the database."""
        new_record = IngestionRecord(
            document_id=document_id,
            filepath=filepath,
            chunk_count=chunk_count,
            status=status,
            ingested_at=datetime.now(),
            metadata=metadata,
        )
        self.db.add(new_record)
        await self.db.commit()
        await self.db.refresh(new_record)
        return new_record

    async def get_ingestion_records(self, document_id: Optional[str] = None, limit: int = 100) -> List[IngestionRecord]:
        """Retrieves ingestion records from the database."""
        stmt = select(IngestionRecord).order_by(IngestionRecord.ingested_at.desc())
        if document_id:
            stmt = stmt.where(IngestionRecord.document_id == document_id)
        stmt = stmt.limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
