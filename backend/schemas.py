from pydantic import BaseModel
from datetime import datetime, date
from models import CategoryType, SubscriptionFrequency


"""create user schemas
"""


class UserCreate(BaseModel):
    email: str
    name: str


class UserUpdate(BaseModel):
    email: str | None = None
    name: str | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime
    model_config = {"from_attributes": True}


"""create category schemas
"""


class CategoryCreate(BaseModel):
    name: str
    type: CategoryType
    color: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    type: CategoryType | None = None
    color: str | None = None


class CategoryResponse(BaseModel):
    id: int
    user_id: int
    name: str
    type: CategoryType
    color: str | None = None
    created_at: datetime
    model_config = {"from_attributes": True}
