from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from schemas import BudgetCreate, BudgetResponse, BudgetUpdate
from service import budget_service
from database import get_db


router = APIRouter(prefix="/budgets", tags=["budgets"])


# Note: until auth is wired up, routes that need the logged-in user's id take
# `user_id` as a query parameter. Once auth exists, this comes from the token.


@router.post(
    "/",
    response_model=BudgetResponse,
    status_code=201,
    summary="Set a budget",
    description="Set a spending cap for one category in one month for the given user.",
)
def create_budget(user_id: int, data: BudgetCreate, db: Session = Depends(get_db)) -> BudgetResponse:
    """Create a budget from the request body and return the saved budget.

    Uniqueness check (user, category, month) is not enforced yet. Once added to
    the service, this should map the ValueError to HTTP 409.
    """
    return budget_service.register_budget(db, user_id, data)


@router.get(
    "/",
    response_model=list[BudgetResponse],
    summary="List all budgets for a user",
)
def get_all_budgets(user_id: int, db: Session = Depends(get_db)) -> list[BudgetResponse]:
    """Return every budget that belongs to the given user. Empty list is a valid response."""
    return budget_service.get_all_budgets(db, user_id)


@router.get(
    "/{budget_id}",
    response_model=BudgetResponse,
    summary="Get one budget by id",
)
def get_budget_by_id(budget_id: int, db: Session = Depends(get_db)) -> BudgetResponse:
    """Fetch one budget by id. Maps ValueError ("Budget not found") to HTTP 404."""
    try:
        return budget_service.get_budget(db, budget_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/{budget_id}",
    response_model=BudgetResponse,
    status_code=200,
    summary="Update budget info",
)
def update_budget(budget_id: int, data: BudgetUpdate, db: Session = Depends(get_db)) -> BudgetResponse:
    """Update fields on an existing budget.

    Only `amount_cents` actually changes because the CRUD whitelist ignores
    other fields. Maps ValueError ("Budget not found") to HTTP 404.
    """
    try:
        return budget_service.update_budget(db, budget_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{budget_id}",
    response_model=bool,
    status_code=200,
    summary="Delete a budget",
)
def delete_budget(budget_id: int, db: Session = Depends(get_db)) -> bool:
    """Delete a budget by id and return True on success.

    Maps ValueError ("Budget not found") to HTTP 404.
    """
    try:
        return budget_service.delete_budget(db, budget_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
