from sqlalchemy.orm import Session
from models import Income


ALLOWED_INCOME_UPDATES = {"amount_cents", "source", "date"}


def create_income(db: Session, income: Income) -> Income:
    """Save a new income to the database. Returns the saved income with its new id filled in."""
    db.add(income)
    db.commit()
    db.refresh(income)

    return income


def get_income_by_id(db: Session, income_id: int) -> Income | None:
    """Fetch one income by its unique id. Returns None if no row matches.

    Note: not scoped by user. The caller should check the returned income
    actually belongs to the logged-in user before exposing it.
    """
    return db.query(Income).filter(Income.id == income_id).first()


def list_incomes(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list[Income]:
    """Return a page of one user's incomes. `skip` is how many rows to jump over, `limit` is the max returned."""
    return db.query(Income).filter(Income.user_id == user_id).offset(skip).limit(limit).all()


def update_income(db: Session, income_id: int, updates: dict) -> Income | None:
    """Change one income. Only keys in ALLOWED_INCOME_UPDATES are written; other keys are ignored.

    This protects fields like id, user_id, category_id, or created_at from being
    overwritten by whatever the API client sends. Returns None if no income matches.
    """
    income = get_income_by_id(db, income_id)
    if not income:
        return None

    for key, value in updates.items():
        if key in ALLOWED_INCOME_UPDATES:
            setattr(income, key, value)

    db.commit()
    db.refresh(income)

    return income


def delete_income(db: Session, income_id: int) -> bool:
    """Delete one income. Returns True if a row was deleted, False if no income matched."""
    income = get_income_by_id(db, income_id)
    if not income:
        return False

    db.delete(income)
    db.commit()

    return True
