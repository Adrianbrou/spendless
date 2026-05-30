from database import Base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, func, Enum as SQLAlchemyEnum, Date, Boolean
from enum import Enum


# Enums for category type and subscription frequency
class CategoryType(str, Enum):
    """Whether a category tracks money going out or money coming in."""
    EXPENSE = "expense"
    INCOME = "income"


class SubscriptionFrequency(str, Enum):
    """How often a recurring subscription charges."""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


# create the classes for the database or the tables

# User class
class User(Base):
    """A person who uses the app. Owns categories, expenses, incomes, budgets, subscriptions."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    password_hash = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Category class
class Category(Base):
    """A label like "Groceries" or "Salary". Each user has their own set of categories."""

    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"),
                     nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(SQLAlchemyEnum(CategoryType),
                  nullable=False)
    color = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Expense(Base):
    """One spending event. Amount is stored in cents so we never deal with floating point money."""

    __tablename__ = "expense"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey(
        "category.id", ondelete="CASCADE"), nullable=False, index=True)
    amount_cents = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Income(Base):
    """One earning event (paycheck, refund, gift). Amount stored in cents."""

    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey(
        "category.id", ondelete="CASCADE"), nullable=False, index=True)
    amount_cents = Column(Integer, nullable=False)
    source = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Budget(Base):
    """A spending cap for one category in one month. Used to warn when the user is over budget."""

    __tablename__ = "budget"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey(
        "category.id", ondelete="CASCADE"), nullable=False, index=True)

    month = Column(Date, nullable=False)
    amount_cents = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Subscription(Base):
    """A recurring charge (Netflix, gym, etc). `active` flips to False when the user cancels it."""

    __tablename__ = "subscription"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey(
        "category.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    frequency = Column(SQLAlchemyEnum(SubscriptionFrequency), nullable=False)
    start_date = Column(Date, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# option 1: manually create the tables defined above in the database:
#   uv run python -c "from database import engine, Base; from models import *; Base.metadata.create_all(engine); print('Tables created')"
# option 2: using alembic
#   uv run alembic revision --autogenerate -m "initial schema"
#   uv run alembic upgrade head
