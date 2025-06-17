from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from app.services.speaker import SpeakerService
from app.schemas.speaker import SpeakerCreate, SpeakerUpdate, SpeakerResponse

router = APIRouter(prefix="/speakers", tags=["speakers"])
speaker_service = SpeakerService()


@router.post("/", response_model=SpeakerResponse, status_code=status.HTTP_201_CREATED)
def create_speaker(speaker_data: SpeakerCreate):
    """Create a new speaker"""
    speaker = speaker_service.create_speaker(speaker_data)
    return SpeakerResponse.model_validate(speaker)


@router.get("/", response_model=List[SpeakerResponse])
def get_speakers():
    """Get all speakers with pagination"""
    speakers = speaker_service.get_all_speakers()
    return [SpeakerResponse.model_validate(speaker) for speaker in speakers]


@router.get("/search/name", response_model=List[SpeakerResponse])
def search_speakers_by_name(name: str = Query(..., description="Name to search for")):
    """Search speakers by name"""
    speakers = speaker_service.search_speakers_by_name(name)
    return [SpeakerResponse.model_validate(speaker) for speaker in speakers]


@router.get("/search/topic", response_model=List[SpeakerResponse])
def search_speakers_by_topic(topic: str = Query(..., description="Topic to search for")):
    """Search speakers by topic"""
    speakers = speaker_service.search_speakers_by_topic(topic)
    return [SpeakerResponse.model_validate(speaker) for speaker in speakers]


@router.get("/{speaker_id}", response_model=SpeakerResponse)
def get_speaker(speaker_id: int):
    """Get speaker by ID"""
    speaker = speaker_service.get_speaker_response(speaker_id)
    if not speaker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speaker not found"
        )
    return SpeakerResponse.model_validate(speaker)


@router.put("/{speaker_id}", response_model=SpeakerResponse)
def update_speaker(speaker_id: int, speaker_data: SpeakerUpdate):
    """Update speaker"""
    speaker = speaker_service.update_speaker(speaker_id, speaker_data)
    if not speaker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speaker not found"
        )
    return SpeakerResponse.model_validate(speaker)


@router.delete("/{speaker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_speaker(speaker_id: int):
    """Delete speaker"""
    success = speaker_service.delete_speaker(speaker_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speaker not found"
        )

