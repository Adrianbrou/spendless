from sqlalchemy.orm import Session
from models import Income
from schemas import IncomeCreate, IncomeUpdate
from crud import income as income_crud


def register_income(db: Session, user_id: int, data: IncomeCreate) -> Income:
    """Create a new income for the given user.

    No uniqueness check: a user can have multiple incomes with the same source
    (paid every two weeks by the same employer). The category_id comes from
    the client; in a real app the router should verify that category belongs
    to this user before calling here.
    """
    income = Income(**data.model_dump(), user_id=user_id)
    return income_crud.create_income(db, income)


def update_income(db: Session, income_id: int, data: IncomeUpdate) -> Income:
    """Change one income. Only fields the client actually sent are applied.

    Raises ValueError if the income does not exist.
    """
    updates = data.model_dump(exclude_unset=True)
    result = income_crud.update_income(db, income_id, updates)
    if not result:
        raise ValueError("Income not found")
    return result


def get_income(db: Session, income_id: int) -> Income:
    """Fetch one income by id. Raises ValueError if the income does not exist."""
    existing = income_crud.get_income_by_id(db, income_id)
    if not existing:
        raise ValueError("Income not found")
    return existing


def get_all_incomes(db: Session, user_id: int) -> list[Income]:
    """Return every income that belongs to one user.

    Empty list is a valid answer.
    """
    return income_crud.list_incomes(db, user_id)


def delete_income(db: Session, income_id: int) -> bool:
    """Delete one income. Raises ValueError if the income does not exist."""
    deleted = income_crud.delete_income(db, income_id)
    if not deleted:
        raise ValueError("Income not found")
    return True
