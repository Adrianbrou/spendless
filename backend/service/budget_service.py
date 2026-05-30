from sqlalchemy.orm import Session
from models import Budget
from schemas import BudgetCreate, BudgetUpdate
from crud import budget as budget_crud


def register_budget(db: Session, user_id: int, data: BudgetCreate) -> Budget:
    """Create a new budget for the given user.

    Real-world uniqueness would be (user_id, category_id, month) - a user has at most
    one budget per category per month. That check needs a CRUD lookup function we
    don't have yet, so it's left out for now. Add it before going to production.
    """
    budget = Budget(**data.model_dump(), user_id=user_id)
    return budget_crud.create_budget(db, budget)


def update_budget(db: Session, budget_id: int, data: BudgetUpdate) -> Budget:
    """Change one budget. Only fields the client actually sent are applied.

    Only `amount_cents` will actually change because of the CRUD whitelist;
    sending month or category_id is silently ignored. Raises ValueError if the budget does not exist.
    """
    updates = data.model_dump(exclude_unset=True)
    result = budget_crud.update_budget(db, budget_id, updates)
    if not result:
        raise ValueError("Budget not found")
    return result


def get_budget(db: Session, budget_id: int) -> Budget:
    """Fetch one budget by id. Raises ValueError if the budget does not exist."""
    existing = budget_crud.get_budget_by_id(db, budget_id)
    if not existing:
        raise ValueError("Budget not found")
    return existing


def get_all_budgets(db: Session, user_id: int) -> list[Budget]:
    """Return every budget that belongs to one user.

    Empty list is a valid answer.
    """
    return budget_crud.list_budgets(db, user_id)


def delete_budget(db: Session, budget_id: int) -> bool:
    """Delete one budget. Raises ValueError if the budget does not exist."""
    deleted = budget_crud.delete_budget(db, budget_id)
    if not deleted:
        raise ValueError("Budget not found")
    return True
