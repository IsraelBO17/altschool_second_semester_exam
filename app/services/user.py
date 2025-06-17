from typing import List, Optional
from fastapi import HTTPException, status

from app.models import User
from app.database import users, registrations
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service class for User CRUD operations"""
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if email already exists
        for user in users:
            if user.email == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
        
        # Generate new ID
        new_id = len(users) + 1
        
        user = User(id=new_id, name=user_data.name, email=user_data.email)
        users.append(user)
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        for user in users:
            if user.id == user_id:
                return user
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        for user in users:
            if user.email == email:
                return user
        return None
    
    def get_all_users(self, active_only: bool = True) -> List[User]:
        """Get all users"""
        if active_only:
            filtered_users = [u for u in users if u.is_active]
        else:
            filtered_users = users
        
        return filtered_users
    
    def get_users_who_attended_events(self) -> List[User]:
        """Get users who attended at least one event"""
        # Get user IDs who attended events
        attended_user_ids = set()
        for registration in registrations:
            if registration.attended:
                attended_user_ids.add(registration.user_id)
        
        # Get users who attended events
        attended_users = []
        for user in users:
            if user.id in attended_user_ids:
                attended_users.append(user)
        
        return attended_users
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user by ID"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Check if email already exists (if updating email)
        if user_data.email is not None and user_data.email != user.email:
            for existing_user in users:
                if existing_user.email == user_data.email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already exists"
                    )
        
        # Update fields
        if user_data.name is not None:
            user.name = user_data.name
        if user_data.email is not None:
            user.email = user_data.email
        
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID (mark as inactive)"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        return True
    
    def search_users_by_name(self, name_query: str) -> List[User]:
        """Search users by name (case-insensitive partial match)"""
        return [user for user in users if name_query.lower() in user.name.lower()]
    
