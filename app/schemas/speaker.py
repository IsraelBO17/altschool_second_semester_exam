from typing import Optional
from pydantic import BaseModel


class SpeakerBase(BaseModel):
    speaker_name: str
    speaker_topic: str


class SpeakerCreate(SpeakerBase):
    pass


class SpeakerUpdate(BaseModel):
    speaker_name: Optional[str] = None
    speaker_topic: Optional[str] = None


class SpeakerResponse(SpeakerBase):
    speaker_id: int

    class Config:
        from_attributes = True

