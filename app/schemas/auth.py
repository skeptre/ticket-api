from pydantic import BaseModel, Field


class Token(BaseModel):
    """Schema for access token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""

    user_id: int | None = None


class LoginRequest(BaseModel):
    """Schema for login request."""

    username: str = Field(description="Username or email")
    password: str = Field(description="User's password")


class RegisterRequest(BaseModel):
    """Schema for user registration."""

    email: str = Field(description="User's email address")
    username: str = Field(min_length=3, max_length=50, description="Desired username")
    password: str = Field(min_length=8, max_length=100, description="Desired password")
