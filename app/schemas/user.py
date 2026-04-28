from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr = Field(description="User's email address")
    username: str = Field(
        min_length=3,
        max_length=50,
        description="User's username"
    )


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(
        min_length=8,
        max_length=100,
        description="User's password"
    )


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    email: EmailStr | None = None
    username: str | None = Field(None, min_length=3, max_length=50)
    password: str | None = Field(None, min_length=8, max_length=100)
    is_active: bool | None = None


class UserResponse(UserBase):
    """Schema for user response (excludes sensitive data)."""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)