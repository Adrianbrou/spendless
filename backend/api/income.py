from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from schemas import IncomeCreate, IncomeResponse, IncomeUpdate
from service import income_service
from database import get_db


router = APIRouter(prefix="/incomes", tags=["incomes"])


# Note: until auth is wired up, routes that need the logged-in user's id take
# `user_id` as a query parameter. Once auth exists, this comes from the token.


@router.post(
    "/",
    response_model=IncomeResponse,
    status_code=201,
    summary="Log a new income",
    description="Record one earning event for the given user.",
)
def create_income(user_id: int, data: IncomeCreate, db: Session = Depends(get_db)) -> IncomeResponse:
    """Create an income from the request body and return the saved income.

    No uniqueness check at this layer: a user can be paid the same source twice.
    """
    return income_service.register_income(db, user_id, data)


@router.get(
    "/",
    response_model=list[IncomeResponse],
    summary="List all incomes for a user",
)
def get_all_incomes(user_id: int, db: Session = Depends(get_db)) -> list[IncomeResponse]:
    """Return every income that belongs to the given user. Empty list is a valid response."""
    return income_service.get_all_incomes(db, user_id)


@router.get(
    "/{income_id}",
    response_model=IncomeResponse,
    summary="Get one income by id",
)
def get_income_by_id(income_id: int, db: Session = Depends(get_db)) -> IncomeResponse:
    """Fetch one income by id. Maps ValueError ("Income not found") to HTTP 404."""
    try:
        return income_service.get_income(db, income_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/{income_id}",
    response_model=IncomeResponse,
    status_code=200,
    summary="Update income info",
)
def update_income(income_id: int, data: IncomeUpdate, db: Session = Depends(get_db)) -> IncomeResponse:
    """Update fields on an existing income.

    Only the fields the client actually sent are applied (partial update).
    Maps ValueError ("Income not found") to HTTP 404.
    """
    try:
        return income_service.update_income(db, income_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{income_id}",
    response_model=bool,
    status_code=200,
    summary="Delete an income",
)
def delete_income(income_id: int, db: Session = Depends(get_db)) -> bool:
    """Delete an income by id and return True on success.

    Maps ValueError ("Income not found") to HTTP 404.
    """
    try:
        return income_service.delete_income(db, income_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
