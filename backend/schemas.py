
from pydantic import BaseModel, PositiveInt, EmailStr
from datetime import datetime, date as DateType
from models import CategoryType, SubscriptionFrequency


# Pydantic schemas are the shape of JSON going in and out of the API.
# For each resource we have three: Create (what the client sends to make one),
# Update (what they send to change one - every field optional), and
# Response (what we send back - includes server-set fields like id, user_id, created_at).
# `model_config = {"from_attributes": True}` lets Pydantic build a Response straight
# from a SQLAlchemy row object, instead of needing a plain dict.


# User schemas
class UserCreate(BaseModel):
    """Payload to register a new user."""
    email: EmailStr
    name: str


class UserUpdate(BaseModel):
    """Payload to change a user's email or name. Both fields optional."""
    email: EmailStr | None = None
    name: str | None = None


class UserResponse(BaseModel):
    """User data returned by the API. No password hash is ever exposed."""
    id: int
    email: EmailStr
    name: str
    created_at: datetime
    model_config = {"from_attributes": True}


# Category schemas
class CategoryCreate(BaseModel):
    """Payload to create a category. `user_id` is set by the server from the logged-in user."""
    name: str
    type: CategoryType
    color: str | None = None


class CategoryUpdate(BaseModel):
    """Payload to change a category. Every field optional."""
    name: str | None = None
    type: CategoryType | None = None
    color: str | None = None


class CategoryResponse(BaseModel):
    """Category data returned by the API."""
    id: int
    user_id: int
    name: str
    type: CategoryType
    color: str | None = None
    created_at: datetime
    model_config = {"from_attributes": True}


# Expense schemas
class ExpenseCreate(BaseModel):
    """Payload to log a new expense. Amount must be positive cents (so 12.50 EUR is 1250)."""
    amount_cents: PositiveInt
    category_id: int
    description: str | None = None
    date: DateType


class ExpenseUpdate(BaseModel):
    """Payload to change an existing expense. Every field optional."""
    amount_cents: PositiveInt | None = None
    category_id: int | None = None
    description: str | None = None
    date: DateType | None = None


class ExpenseResponse(BaseModel):
    """Expense data returned by the API."""
    id: int
    user_id: int
    category_id: int
    amount_cents: PositiveInt
    description: str | None = None
    date: DateType
    created_at: datetime
    model_config = {"from_attributes": True}


# Income schemas
class IncomeCreate(BaseModel):
    """Payload to log a new income. `source` is a free-text label like "Employer" or "Refund"."""
    amount_cents: PositiveInt
    category_id: int
    source: str
    date: DateType


class IncomeUpdate(BaseModel):
    """Payload to change an existing income. Every field optional."""
    amount_cents: PositiveInt | None = None
    category_id: int | None = None
    source: str | None = None
    date: DateType | None = None


class IncomeResponse(BaseModel):
    """Income data returned by the API."""
    id: int
    user_id: int
    category_id: int
    amount_cents: PositiveInt
    source: str
    date: DateType
    created_at: datetime
    model_config = {"from_attributes": True}


# Budget schemas
class BudgetCreate(BaseModel):
    """Payload to set a spending cap for one category in one month."""
    category_id: int
    month: DateType
    amount_cents: PositiveInt


class BudgetUpdate(BaseModel):
    """Payload to change a budget. Every field optional."""
    category_id: int | None = None
    month: DateType | None = None
    amount_cents: PositiveInt | None = None


class BudgetResponse(BaseModel):
    """Budget data returned by the API."""
    id: int
    user_id: int
    category_id: int
    month: DateType
    amount_cents: PositiveInt
    created_at: datetime
    model_config = {"from_attributes": True}


# Subscription schemas
class SubscriptionCreate(BaseModel):
    """Payload to add a recurring charge. New subscriptions are active by default."""
    category_id: int
    name: str
    frequency: SubscriptionFrequency
    start_date: DateType
    active: bool = True


class SubscriptionUpdate(BaseModel):
    """Payload to change a subscription. Set `active` to False to cancel it."""
    category_id: int | None = None
    name: str | None = None
    frequency: SubscriptionFrequency | None = None
    start_date: DateType | None = None
    active: bool | None = None


class SubscriptionResponse(BaseModel):
    """Subscription data returned by the API."""
    id: int
    user_id: int
    category_id: int
    name: str
    frequency: SubscriptionFrequency
    start_date: DateType
    active: bool
    created_at: datetime
    model_config = {"from_attributes": True}
