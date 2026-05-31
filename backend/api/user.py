from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from schemas import UserCreate, UserResponse, UserUpdate
from service import user_service
from database import get_db


router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Register a new user",
    description="Create a user account. Returns 409 if the email is already taken.",
)
def create_user(data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """Create a user from the request body and return the saved user.

    Maps the service layer's ValueError ("User already exists") to HTTP 409.
    Any unexpected failure bubbles up to FastAPI and becomes a 500.
    """
    try:
        return user_service.register_user(db, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="List all users",
)
def get_all_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    """Return every user. Empty list is a valid response, so no try/except is needed."""
    return user_service.get_all_users(db)


@router.get("/{user_id}",
            response_model=UserResponse,
            summary="Get the user by id"
            )
def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    """Fetch one user by id. Maps ValueError ("User not found") to HTTP 404."""
    try:
        return user_service.get_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{user_id}",
              response_model=UserResponse,
              summary="updates user info",
              status_code=200)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)) -> UserResponse:
    """Update fields on an existing user.

    Only the fields the client actually sent are applied (partial update).
    Maps ValueError ("User not found") to HTTP 404.
    """
    try:
        return user_service.update_user(db, user_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}",
               response_model=bool,
               summary="delete user",
               status_code=200)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> bool:
    """Delete a user by id and return True on success.

    Maps ValueError ("User not found") to HTTP 404. Note: REST convention is to
    return 204 No Content with no body for DELETE; this route returns 200 with
    a boolean instead. Either works, this is a style choice.
    """
    try:
        return user_service.delete_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
