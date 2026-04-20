from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class Category(str, Enum):
    food = "food"
    travel = "travel"
    shopping = "shopping"
    rent = "rent"
    utilities = "utilities"
    entertainment = "entertainment"
    health = "health"
    education = "education"
    other = "other"


class ExpenseModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    title: str
    amount: float
    category: Category
    note: Optional[str] = None
    date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        use_enum_values = True
