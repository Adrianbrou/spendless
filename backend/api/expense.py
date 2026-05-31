from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from service import expense_service
from database import get_db


router = APIRouter(prefix="/expenses", tags=["expenses"])


# Note: until auth is wired up, routes that need the logged-in user's id take
# `user_id` as a query parameter. Once auth exists, this comes from the token.


@router.post(
    "/",
    response_model=ExpenseResponse,
    status_code=201,
    summary="Log a new expense",
    description="Record one spending event for the given user.",
)
def create_expense(user_id: int, data: ExpenseCreate, db: Session = Depends(get_db)) -> ExpenseResponse:
    """Create an expense from the request body and return the saved expense.

    No uniqueness check at this layer: a user can have two coffees in one day.
    """
    return expense_service.register_expense(db, user_id, data)


@router.get(
    "/",
    response_model=list[ExpenseResponse],
    summary="List all expenses for a user",
)
def get_all_expenses(user_id: int, db: Session = Depends(get_db)) -> list[ExpenseResponse]:
    """Return every expense that belongs to the given user. Empty list is a valid response."""
    return expense_service.get_all_expenses(db, user_id)


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Get one expense by id",
)
def get_expense_by_id(expense_id: int, db: Session = Depends(get_db)) -> ExpenseResponse:
    """Fetch one expense by id. Maps ValueError ("Expense not found") to HTTP 404."""
    try:
        return expense_service.get_expense(db, expense_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/{expense_id}",
    response_model=ExpenseResponse,
    status_code=200,
    summary="Update expense info",
)
def update_expense(expense_id: int, data: ExpenseUpdate, db: Session = Depends(get_db)) -> ExpenseResponse:
    """Update fields on an existing expense.

    Only the fields the client actually sent are applied (partial update).
    Maps ValueError ("Expense not found") to HTTP 404.
    """
    try:
        return expense_service.update_expense(db, expense_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{expense_id}",
    response_model=bool,
    status_code=200,
    summary="Delete an expense",
)
def delete_expense(expense_id: int, db: Session = Depends(get_db)) -> bool:
    """Delete an expense by id and return True on success.

    Maps ValueError ("Expense not found") to HTTP 404.
    """
    try:
        return expense_service.delete_expense(db, expense_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
