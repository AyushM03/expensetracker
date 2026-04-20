from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.expense import Category


# ── Auth schemas ──────────────────────────────────────
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime


# ── Expense schemas ───────────────────────────────────
class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: Category
    note: Optional[str] = None
    date: Optional[datetime] = None


class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[Category] = None
    note: Optional[str] = None
    date: Optional[datetime] = None


class ExpenseResponse(BaseModel):
    id: str
    title: str
    amount: float
    category: str
    note: Optional[str]
    date: datetime
    created_at: datetime


# ── Summary schema ────────────────────────────────────
class MonthlySummary(BaseModel):
    month: str
    total: float
    by_category: dict
    count: int
