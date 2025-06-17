from typing import List, Optional
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.config.database import SessionDep
from app.schemas.user import UserCreate, UserUpdate
from app.models import User, Registration


class UserService:
    """Service class for User CRUD operations"""

    def __init__(self, session: SessionDep = SessionDep): # type: ignore
        self.session = session
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        try:
            user = User(**user_data.model_dump())
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        statement = select(User).where(User.user_id == user_id)
        result = await self.session.exec(statement)
        return result.first()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        statement = select(User).where(User.user_email == email)
        result = await self.session.exec(statement)
        return result.first()
    
    async def get_all_users(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[User]:
        """Get all users with pagination"""
        statement = select(User)
        if active_only:
            statement = statement.where(User.user_is_active == True)
        statement = statement.offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return list(result.all())
    
    async def get_users_who_attended_events(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users who attended at least one event"""
        statement = (
            select(User)
            .join(Registration)
            .where(Registration.user_attended == True)
            .distinct()
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.exec(statement)
        return list(result.all())
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user by ID"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        
        user_data_dict = user_data.model_dump(exclude_unset=True)
        for key, value in user_data_dict.items():
            setattr(user, key, value)
        
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
    
    async def delete_user(self, user_id: int) -> bool:
        """Delete user by ID"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.user_is_active = False
        self.session.add(user)
        await self.session.commit()
        return True
    
