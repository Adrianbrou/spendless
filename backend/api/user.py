from fastapi import Depends, APIRouter, HTTPException
from service import user_service
from schemas import UserCreate, UserUpdate, UserResponse
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/",
    response_model=UserResponse,
    summary="Register a new user",
    description="Create a user account. Returns 400 if the email is already taken.",
    status_code=201,
)
def create_user(data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """Create a user from the request body and return the saved user.

    Translates the service layer's `ValueError` (raised when the email is
    already in use) into HTTP 400. Any unexpected failure bubbles up to
    FastAPI and becomes a 500 by default.
    """
    try:
        return user_service.register_user(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
