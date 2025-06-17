from typing import List, Optional
from sqlmodel import select

from app.config.database import SessionDep
from app.schemas.speaker import SpeakerCreate, SpeakerUpdate
from app.models import Speaker


class SpeakerService:
    """Service class for Speaker CRUD operations"""
    
    def __init__(self, session: SessionDep = SessionDep): # type: ignore
        self.session = session

    async def create_speaker(self, speaker_data: SpeakerCreate) -> Speaker:
        """Create a new speaker"""
        speaker = Speaker(**speaker_data.model_dump())
        self.session.add(speaker)
        await self.session.commit()
        await self.session.refresh(speaker)
        return speaker

    async def get_speaker_by_id(self, speaker_id: int) -> Optional[Speaker]:
        """Get speaker by ID"""
        statement = select(Speaker).where(Speaker.speaker_id == speaker_id)
        result = await self.session.exec(statement)
        return result.first()
    

    async def get_all_speakers(self, skip: int = 0, limit: int = 100) -> List[Speaker]:
        """Get all speakers with pagination"""
        statement = select(Speaker).offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return list(result.all())

    async def get_speakers_by_name(self, name: str) -> List[Speaker]:
        """Get speakers by name"""
        statement = select(Speaker).where(Speaker.speaker_name.ilike(f"%{name}%"))
        result = await self.session.exec(statement)
        return list(result.all())

    async def update_speaker(self, speaker_id: int, speaker_data: SpeakerUpdate) -> Optional[Speaker]:
        """Update speaker"""
        speaker = await self.get_speaker_by_id(speaker_id)
        if not speaker:
            return None
        
        speaker_data_dict = speaker_data.model_dump(exclude_unset=True)
        for key, value in speaker_data_dict.items():
            setattr(speaker, key, value)
        
        self.session.add(speaker)
        await self.session.commit()
        await self.session.refresh(speaker)
        return speaker

    async def delete_speaker(self, speaker_id: int) -> bool:
        """Delete speaker"""
        speaker = self.get_speaker_by_id(speaker_id)
        if not speaker:
            return False
        
        self.session.delete(speaker)
        await self.session.commit()
        return True

