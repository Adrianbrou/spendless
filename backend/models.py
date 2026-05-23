from database import Base
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, func, Enum as SQLAlchemyEnum, Date, Boolean
from enum import Enum
from sqlalchemy.orm import relationship

"""Create Enum for category and Subscription Frequency
    """


class CategoryType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"


class SubscriptionFrequency(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


# create the classes for the database or the tables

# User class
class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    password_hash = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Category class
class Category(Base):
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
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey(
        "category.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey(
        "category.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    source = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Budget(Base):

    __tablename__ = "budget"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey(
        "category.id", ondelete="CASCADE"), nullable=False, index=True)

    month = Column(Date, nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Subscription(Base):

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

    """option 1: manually create the tables defined above in the databse would be :
    uv run python -c "from database import engine, Base; from models import *; Base.metadata.create_all(engine); print('Tables created')"
         option 2 : using alembic

         - uv run alembic revision --autogenerate -m "initial schema"
         
         - check the migration file that was generated: uv run alembic upgrade head


    """
