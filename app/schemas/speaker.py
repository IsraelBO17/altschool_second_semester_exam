from typing import Optional
from pydantic import BaseModel


class SpeakerBase(BaseModel):
    name: str
    topic: str


class SpeakerCreate(SpeakerBase):
    pass


class SpeakerUpdate(BaseModel):
    name: Optional[str] = None
    topic: Optional[str] = None


class SpeakerResponse(SpeakerBase):
    id: int

    class Config:
        from_attributes = True

