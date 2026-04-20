"""Pydantic v2 schemas for authentication."""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=1, max_length=100)
    household_name: str = Field(min_length=1, max_length=255)
    timezone: str = Field(default="America/New_York", max_length=50)
    is_self_learner: bool = False


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    household_id: uuid.UUID
    email: str
    display_name: str
    role: str
    is_active: bool
    created_at: datetime


class RegisterResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class MessageResponse(BaseModel):
    message: str


class InstitutionalRegisterRequest(BaseModel):
    organization_name: str = Field(min_length=1, max_length=255)
    organization_type: str = Field(default="university")  # university, bootcamp, corporate
    admin_email: EmailStr
    admin_password: str = Field(min_length=8, max_length=128)
    admin_display_name: str = Field(min_length=1, max_length=100)


class InviteRequest(BaseModel):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=100)
    institutional_role: str  # instructor, teaching_assistant, student
    learner_name: str | None = None  # required for students


class InviteResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    email: str
    display_name: str
    institutional_role: str
    linked_child_id: uuid.UUID | None = None
