from sqlalchemy.orm import Session
from models import Expense
from schemas import ExpenseCreate, ExpenseUpdate
from crud import expense as expense_crud


def register_expense(db: Session, user_id: int, data: ExpenseCreate) -> Expense:
    """Create a new expense for the given user.

    No uniqueness check: a user can legitimately have many expenses with the same
    amount, category, or date (bought coffee twice today). The category_id comes
    from the client; in a real app the router should verify that category belongs
    to this user before calling here.
    """
    expense = Expense(**data.model_dump(), user_id=user_id)
    return expense_crud.create_expense(db, expense)


def update_expense(db: Session, expense_id: int, data: ExpenseUpdate) -> Expense:
    """Change one expense. Only fields the client actually sent are applied.

    Raises ValueError if the expense does not exist.
    """
    updates = data.model_dump(exclude_unset=True)
    result = expense_crud.update_expense(db, expense_id, updates)
    if not result:
        raise ValueError("Expense not found")
    return result


def get_expense(db: Session, expense_id: int) -> Expense:
    """Fetch one expense by id. Raises ValueError if the expense does not exist."""
    existing = expense_crud.get_expense_by_id(db, expense_id)
    if not existing:
        raise ValueError("Expense not found")
    return existing


def get_all_expenses(db: Session, user_id: int) -> list[Expense]:
    """Return every expense that belongs to one user.

    Empty list is a valid answer (a brand new user has zero expenses).
    """
    return expense_crud.list_expenses(db, user_id)


def delete_expense(db: Session, expense_id: int) -> bool:
    """Delete one expense. Raises ValueError if the expense does not exist."""
    deleted = expense_crud.delete_expense(db, expense_id)
    if not deleted:
        raise ValueError("Expense not found")
    return True
