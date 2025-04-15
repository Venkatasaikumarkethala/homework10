from datetime import datetime
from urllib.parse import urlparse
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator
from typing import List, Optional
from uuid import UUID
from app.schemas.link_schema import Link
from app.schemas.pagination_schema import EnhancedPagination
import re


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    first_name: Optional[str] = None  # ✅ Add this
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    nickname: Optional[str] = None  # ✅ Add this
    github_profile_url: Optional[HttpUrl] = None  # ✅ Add this
    linkedin_profile_url: Optional[HttpUrl] = None  # ✅ Add this

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Username can only contain letters, numbers, underscores, and hyphens.")
        return v

    @validator('full_name')
    def validate_full_name(cls, v):
        if v and not re.match(r"^[a-zA-Z\s'-]+$", v):
            raise ValueError("Full name can only contain letters, spaces, hyphens, or apostrophes.")
        return v

    @validator('nickname')
    def validate_nickname(cls, v):
        if v and not re.match(r"^[a-zA-Z0-9_-]{3,50}$", v):
            raise ValueError("Nickname must be 3-50 characters long, using only letters, numbers, underscores, and hyphens.")
        return v

    @validator('profile_picture_url', pre=True, always=True)
    def validate_profile_picture_url(cls, v):
        if v is None:
            return v
        parsed_url = urlparse(v)
        if not re.search(r"\.(jpg|jpeg|png)$", parsed_url.path):
            raise ValueError("Profile picture URL must point to a valid image file (JPEG, PNG).")
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character.")
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    first_name: Optional[str] = None  # ✅ Add this
    bio: Optional[str] = None
    profile_picture_url: Optional[HttpUrl] = None
    nickname: Optional[str] = None  # ✅ Add this
    github_profile_url: Optional[HttpUrl] = None  # ✅ Add this
    linkedin_profile_url: Optional[HttpUrl] = None  # ✅ Add this

    @validator('profile_picture_url', pre=True, always=True)
    def validate_profile_picture_url(cls, v):
        if v is not None:
            parsed_url = urlparse(str(v))
            if not re.search(r"\.(jpg|jpeg|png)$", parsed_url.path):
                raise ValueError("Profile picture URL must point to a valid image file (JPEG, PNG).")
        return v


class UserResponse(UserBase):
    id: UUID  # ✅ Use UUID to match DB
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    links: List[Link] = []

    @validator('id', pre=True)
    def convert_uuid(cls, value):
        return str(value) if isinstance(value, UUID) else value


class UserListResponse(BaseModel):
    items: List[UserResponse]
    pagination: EnhancedPagination


class LoginRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None  # ✅ Add this
    password: str


class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
