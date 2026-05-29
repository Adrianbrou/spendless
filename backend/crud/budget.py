from sqlalchemy.orm import Session
from models import Budget


ALLOWED_BUDGET_UPDATES = {"amount_cents"}


def create_budget(db: Session, budget: Budget) -> Budget:
    """Save a new budget to the database. Returns the saved budget with its new id filled in."""
    db.add(budget)
    db.commit()
    db.refresh(budget)

    return budget


def get_budget_by_id(db: Session, budget_id: int) -> Budget | None:
    """Fetch one budget by its unique id. Returns None if no row matches.

    Note: not scoped by user. The caller should check the returned budget
    actually belongs to the logged-in user before exposing it.
    """
    return db.query(Budget).filter(Budget.id == budget_id).first()


def list_budgets(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list[Budget]:
    """Return a page of one user's budgets. `skip` is how many rows to jump over, `limit` is the max returned."""
    return db.query(Budget).filter(Budget.user_id == user_id).offset(skip).limit(limit).all()


def update_budget(db: Session, budget_id: int, updates: dict) -> Budget | None:
    """Change one budget. Only keys in ALLOWED_BUDGET_UPDATES are written; other keys are ignored.

    Only `amount_cents` is updatable. Month and category are part of the budget's identity,
    so to change those you'd delete this budget and create a new one. Returns None if no
    budget matches.
    """
    budget = get_budget_by_id(db, budget_id)
    if not budget:
        return None

    for key, value in updates.items():
        if key in ALLOWED_BUDGET_UPDATES:
            setattr(budget, key, value)

    db.commit()
    db.refresh(budget)

    return budget


def delete_budget(db: Session, budget_id: int) -> bool:
    """Delete one budget. Returns True if a row was deleted, False if no budget matched."""
    budget = get_budget_by_id(db, budget_id)
    if not budget:
        return False

    db.delete(budget)
    db.commit()

    return True
