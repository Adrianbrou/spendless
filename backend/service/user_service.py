from crud import user as user_crud
from models import User
from schemas import UserCreate, UserUpdate
from sqlalchemy.orm import Session


def register_user(db: Session, data: UserCreate) -> User:
    """Create a new user. Raises ValueError if the email is already taken.

    Email is the natural uniqueness check for users (it's what they log in with).
    """
    existing = user_crud.get_user_by_email(db, data.email)
    if existing:
        raise ValueError("User already exists")

    user = User(**data.model_dump())
    return user_crud.create_user(db, user)


def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    """Change one user. Only fields the client actually sent are applied (partial update).

    `exclude_unset=True` strips out fields that weren't in the request body,
    so optional fields don't get overwritten with None. Raises ValueError if the user does not exist.
    """
    updates = data.model_dump(exclude_unset=True)
    result = user_crud.update_user(db, user_id, updates)
    if not result:
        raise ValueError("User not found")
    return result


def get_user(db: Session, user_id: int) -> User:
    """Fetch one user by id. Raises ValueError if the user does not exist."""
    existing = user_crud.get_user_by_id(db, user_id)
    if not existing:
        raise ValueError("User not found")
    return existing


def get_all_users(db: Session) -> list[User]:
    """Return every user in the database.

    No existence check because an empty list is a valid answer.
    In a real app this would be admin-only and probably paginated.
    """
    return user_crud.list_users(db)


def delete_user(db: Session, user_id: int) -> bool:
    """Delete one user. Raises ValueError if the user does not exist.

    Cascade rules in the model mean the user's categories, expenses,
    incomes, budgets, and subscriptions all get deleted with them.
    """
    deleted = user_crud.delete_user(db, user_id)
    if not deleted:
        raise ValueError("User not found")
    return True
