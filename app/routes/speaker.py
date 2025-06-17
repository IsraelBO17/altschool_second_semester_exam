from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from app.config.database import SessionDep
from app.services.speaker import SpeakerService
from app.schemas.speaker import SpeakerCreate, SpeakerUpdate, SpeakerResponse

router = APIRouter(prefix="/speakers", tags=["speakers"])


@router.post("/", response_model=SpeakerResponse, status_code=status.HTTP_201_CREATED)
async def create_speaker(
    speaker_data: SpeakerCreate,
    session: SessionDep = SessionDep # type: ignore
):
    """Create a new speaker"""
    speaker_service = SpeakerService(session)
    return await speaker_service.create_speaker(speaker_data)


@router.get("/", response_model=List[SpeakerResponse])
async def get_speakers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: SessionDep = SessionDep # type: ignore
):
    """Get all speakers with optional topic filter"""
    speaker_service = SpeakerService(session)
    return await speaker_service.get_all_speakers(skip=skip, limit=limit)


@router.get("/{speaker_id}", response_model=SpeakerResponse)
async def get_speaker(
    speaker_id: int,
    session: SessionDep = SessionDep # type: ignore
):
    """Get speaker by ID"""
    speaker_service = SpeakerService(session)
    speaker = await speaker_service.get_speaker_by_id(speaker_id)
    if not speaker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Speaker not found")
    return speaker


@router.patch("/{speaker_id}", response_model=SpeakerResponse)
async def update_speaker(
    speaker_id: int,
    speaker_data: SpeakerUpdate,
    session: SessionDep = SessionDep # type: ignore
):
    """Update speaker"""
    speaker_service = SpeakerService(session)
    speaker = await speaker_service.update_speaker(speaker_id, speaker_data)
    if not speaker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Speaker not found")
    return speaker


@router.delete("/{speaker_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_speaker(
    speaker_id: int,
    session: SessionDep = SessionDep # type: ignore
):
    """Delete speaker"""
    speaker_service = SpeakerService(session)
    success = speaker_service.delete_speaker(session, speaker_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Speaker not found"
        )

