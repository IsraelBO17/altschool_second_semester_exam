from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from app.config.database import SessionDep
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: SessionDep = SessionDep # type: ignore
):
    """Create a new user"""
    user_service = UserService(session)
    
    # Check if email already exists
    existing_user = await user_service.get_user_by_email(user_data.user_email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return await user_service.create_user(user_data)


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    session: SessionDep = SessionDep # type: ignore
):
    """Get all users with pagination"""
    user_service = UserService(session)
    users = await user_service.get_all_users(skip=skip, limit=limit, active_only=active_only)
    return users


@router.get("/attended-events", response_model=List[UserResponse])
async def get_users_who_attended_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: SessionDep = SessionDep  # type: ignore
):
    """Filter users who attended at least one event"""
    user_service = UserService(session)
    users = await user_service.get_users_who_attended_events(skip=skip, limit=limit)
    return users


@router.get("/email/{email}", response_model=UserResponse)
async def get_user_by_email(
    email: str,
    session: SessionDep = SessionDep # type: ignore
):
    """Get user by email"""
    user_service = UserService(session)
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: SessionDep = SessionDep # type: ignore
):
    """Get user by ID"""
    user_service = UserService(session)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: SessionDep = SessionDep # type: ignore
):
    """Update user"""
    user_service = UserService(session)
    
    # Check if email is being updated and already exists
    if user_data.user_email:
        existing_user = await user_service.get_user_by_email(user_data.user_email)
        if existing_user and existing_user.user_id != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    user = await user_service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: SessionDep = SessionDep # type: ignore
):
    """Delete user"""
    user_service = UserService(session)
    success = await user_service.delete_user(user_id)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

