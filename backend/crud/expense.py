from sqlalchemy.orm import Session
from models import Expense


ALLOWED_EXPENSE_UPDATES = {"amount_cents", "description", "date"}


def create_expense(db: Session, expense: Expense) -> Expense:
    """Save a new expense to the database. Returns the saved expense with its new id filled in."""
    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


def get_expense_by_id(db: Session, expense_id: int) -> Expense | None:
    """Fetch one expense by its unique id. Returns None if no row matches.

    Note: not scoped by user. The caller should check the returned expense
    actually belongs to the logged-in user before exposing it.
    """
    return db.query(Expense).filter(Expense.id == expense_id).first()


def list_expenses(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list[Expense]:
    """Return a page of one user's expenses. `skip` is how many rows to jump over, `limit` is the max returned."""
    return db.query(Expense).filter(Expense.user_id == user_id).offset(skip).limit(limit).all()


def update_expense(db: Session, expense_id: int, updates: dict) -> Expense | None:
    """Change one expense. Only keys in ALLOWED_EXPENSE_UPDATES are written; other keys are ignored.

    This protects fields like id, user_id, category_id, or created_at from being
    overwritten by whatever the API client sends. Returns None if no expense matches.
    """
    expense = get_expense_by_id(db, expense_id)
    if not expense:
        return None

    for key, value in updates.items():
        if key in ALLOWED_EXPENSE_UPDATES:
            setattr(expense, key, value)

    db.commit()
    db.refresh(expense)

    return expense


def delete_expense(db: Session, expense_id: int) -> bool:
    """Delete one expense. Returns True if a row was deleted, False if no expense matched."""
    expense = get_expense_by_id(db, expense_id)
    if not expense:
        return False

    db.delete(expense)
    db.commit()

    return True
