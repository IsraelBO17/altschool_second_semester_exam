from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    user_name: str
    user_email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None


class UserResponse(UserBase):
    user_id: int
    user_is_active: bool

    class Config:
        from_attributes = True

