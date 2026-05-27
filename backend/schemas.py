from pydantic import BaseModel, PositiveInt, EmailStr
from datetime import datetime, date
from models import CategoryType, SubscriptionFrequency


# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    name: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime
    model_config = {"from_attributes": True}


# Category schemas
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


# Expense schemas
class ExpenseCreate(BaseModel):
    amount_cents: PositiveInt
    category_id: int
    description: str | None = None
    date: date


class ExpenseUpdate(BaseModel):
    amount_cents: PositiveInt | None = None
    category_id: int | None = None
    description: str | None = None
    date: date | None = None


class ExpenseResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount_cents: PositiveInt
    description: str | None = None
    date: date
    created_at: datetime
    model_config = {"from_attributes": True}


# Income schemas
class IncomeCreate(BaseModel):
    amount_cents: PositiveInt
    category_id: int
    source: str
    date: date


class IncomeUpdate(BaseModel):
    amount_cents: PositiveInt | None = None
    category_id: int | None = None
    source: str | None = None
    date: date | None = None


class IncomeResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount_cents: PositiveInt
    source: str
    date: date
    created_at: datetime
    model_config = {"from_attributes": True}


# Budget schemas
class BudgetCreate(BaseModel):
    category_id: int
    month: date
    amount_cents: PositiveInt


class BudgetUpdate(BaseModel):
    category_id: int | None = None
    month: date | None = None
    amount_cents: PositiveInt | None = None


class BudgetResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    month: date
    amount_cents: PositiveInt
    created_at: datetime
    model_config = {"from_attributes": True}


# Subscription schemas
class SubscriptionCreate(BaseModel):
    category_id: int
    name: str
    frequency: SubscriptionFrequency
    start_date: date
    active: bool = True


class SubscriptionUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = None
    frequency: SubscriptionFrequency | None = None
    start_date: date | None = None
    active: bool | None = None


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    name: str
    frequency: SubscriptionFrequency
    start_date: date
    active: bool
    created_at: datetime
    model_config = {"from_attributes": True}
