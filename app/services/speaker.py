from typing import List, Optional

from app.models import Speaker
from app.database import speakers
from app.schemas.speaker import SpeakerCreate, SpeakerUpdate, SpeakerResponse


class SpeakerService:
    """Service class for Speaker CRUD operations"""
    
    def create_speaker(self, speaker_data: SpeakerCreate) -> Speaker:
        """Create a new speaker"""
        # Generate new ID
        new_id = max([s.id for s in speakers], default=0) + 1
        
        speaker = Speaker(
            id=new_id,
            name=speaker_data.name,
            topic=speaker_data.topic
        )
        speakers.append(speaker)
        return speaker
    
    def get_speaker_by_id(self, speaker_id: int) -> Optional[Speaker]:
        """Get speaker by ID"""
        return next((speaker for speaker in speakers if speaker.id == speaker_id), None)
    
    def get_all_speakers(self) -> List[Speaker]:
        """Get all speakers"""
        return speakers
    
    def update_speaker(self, speaker_id: int, speaker_data: SpeakerUpdate) -> Optional[Speaker]:
        """Update speaker by ID"""
        speaker = self.get_speaker_by_id(speaker_id)
        if not speaker:
            return None
        
        # Update fields from schema
        speaker_data_dict = speaker_data.model_dump(exclude_unset=True)
        for key, value in speaker_data_dict.items():
            setattr(speaker, key, value)
        
        return speaker
    
    def delete_speaker(self, speaker_id: int) -> bool:
        """Delete speaker by ID"""
        speaker = self.get_speaker_by_id(speaker_id)
        if not speaker:
            return False
        
        speakers.remove(speaker)
        return True
    
    def search_speakers_by_name(self, name_query: str) -> List[Speaker]:
        """Search speakers by name (case-insensitive partial match)"""
        return [speaker for speaker in speakers if name_query.lower() in speaker.name.lower()]
    
    def search_speakers_by_topic(self, topic_query: str) -> List[Speaker]:
        """Search speakers by topic (case-insensitive partial match)"""
        return [speaker for speaker in speakers if topic_query.lower() in speaker.topic.lower()]


