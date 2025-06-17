from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    """Create a new user"""
    user = user_service.create_user(user_data)
    return UserResponse.model_validate(user)


@router.get("/", response_model=List[UserResponse])
def get_users(active_only: bool = Query(True)):
    """Get all users"""
    users = user_service.get_all_users(active_only=active_only)
    return [UserResponse.model_validate(user) for user in users]


@router.get("/attended-events", response_model=List[UserResponse])
def get_users_who_attended_events():
    """Filter users who attended at least one event"""
    users = user_service.get_users_who_attended_events()
    return [UserResponse.model_validate(user) for user in users]


@router.get("/search", response_model=List[UserResponse])
def search_users_by_name(name: str = Query(..., description="Name to search for")):
    """Search users by name"""
    users = user_service.search_users_by_name(name)
    return [UserResponse.model_validate(user) for user in users]


@router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email(email: str):
    """Get user by email"""
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.model_validate(user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Get user by ID"""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate):
    """Update user"""
    user = user_service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.model_validate(user)


@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Delete user (soft delete - marks as inactive)"""
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


