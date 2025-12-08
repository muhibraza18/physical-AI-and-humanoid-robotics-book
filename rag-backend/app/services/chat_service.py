from typing import List, Dict, Optional
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.db_models import ChatHistory, UserSession # Changed to relative import

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_new_session(self, user_id: Optional[str] = None) -> str:
        """Creates a new user session and returns its ID."""
        session_id = str(uuid4())
        new_session = UserSession(session_id=session_id, user_id=user_id)
        self.db.add(new_session)
        await self.db.commit()
        await self.db.refresh(new_session)
        return session_id

    async def get_session(self, session_id: str) -> Optional[UserSession]:
        """Retrieves a user session by its ID."""
        result = await self.db.execute(
            select(UserSession).where(UserSession.session_id == session_id)
        )
        return result.scalars().first()

    async def save_chat_history(
        self,
        session_id: str,
        query: str,
        response: str,
        retrieved_evidence: Optional[List[Dict]] = None,
        user_id: Optional[str] = None,
    ) -> ChatHistory:
        """Saves a chat interaction to the database."""
        # Ensure session exists or create a dummy one if not
        session = await self.get_session(session_id)
        if not session:
            # Optionally create session if it doesn't exist, or raise error
            print(f"Warning: Session {session_id} not found. Creating a new one.")
            session = UserSession(session_id=session_id, user_id=user_id)
            self.db.add(session)
            await self.db.flush() # Flush to get ID if needed, but not critical for history table

        new_entry = ChatHistory(
            session_id=session_id,
            user_id=user_id,
            query=query,
            response=response,
            retrieved_evidence=retrieved_evidence,
        )
        self.db.add(new_entry)
        await self.db.commit()
        await self.db.refresh(new_entry)
        return new_entry

    async def get_chat_history(self, session_id: str, limit: int = 100) -> List[ChatHistory]:
        """Retrieves chat history for a given session ID."""
        result = await self.db.execute(
            select(ChatHistory)
            .where(ChatHistory.session_id == session_id)
            .order_by(ChatHistory.timestamp.asc())
            .limit(limit)
        )
        return result.scalars().all()