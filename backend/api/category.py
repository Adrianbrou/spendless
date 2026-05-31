from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from service import category_service
from database import get_db


router = APIRouter(prefix="/categories", tags=["categories"])


# Note: until auth is wired up, routes that need the logged-in user's id take
# `user_id` as a query parameter. Once auth exists, this comes from the token
# instead and these query params go away.


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=201,
    summary="Register a new category",
    description="Create a category for the given user. Returns 409 if the user already has a category with this name.",
)
def create_category(user_id: int, data: CategoryCreate, db: Session = Depends(get_db)) -> CategoryResponse:
    """Create a category from the request body and return the saved category.

    Maps the service layer's ValueError ("Category already exists") to HTTP 409.
    """
    try:
        return category_service.register_category(db, user_id, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get(
    "/",
    response_model=list[CategoryResponse],
    summary="List all categories for a user",
)
def get_all_categories(user_id: int, db: Session = Depends(get_db)) -> list[CategoryResponse]:
    """Return every category that belongs to the given user. Empty list is a valid response."""
    return category_service.get_all_categories(db, user_id)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Get one category by id",
)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)) -> CategoryResponse:
    """Fetch one category by id. Maps ValueError ("Category not found") to HTTP 404."""
    try:
        return category_service.get_category(db, category_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=200,
    summary="Update category info",
)
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)) -> CategoryResponse:
    """Update fields on an existing category.

    Only the fields the client actually sent are applied (partial update).
    Maps ValueError ("Category not found") to HTTP 404.
    """
    try:
        return category_service.update_category(db, category_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{category_id}",
    response_model=bool,
    status_code=200,
    summary="Delete a category",
)
def delete_category(category_id: int, db: Session = Depends(get_db)) -> bool:
    """Delete a category by id and return True on success.

    Maps ValueError ("Category not found") to HTTP 404. Cascade rules in the
    model mean every expense, income, budget, and subscription that pointed at
    this category gets deleted too.
    """
    try:
        return category_service.delete_category(db, category_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
