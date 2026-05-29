from sqlalchemy.orm import Session
from models import User


# whitelist for users updates that use email and name
ALLOWED_USER_UPDATES = {"email", "name"}


def create_user(db: Session, user: User) -> User:
    """Save a new user to the database. Returns the saved user with its new id filled in."""
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Fetch one user by their unique id. Returns None if no row matches."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str) -> User | None:
    """Fetch one user by email. Returns None if no row matches."""
    return db.query(User).filter(User.email == user_email).first()


def get_user_by_name(db: Session, user_name: str) -> User | None:
    """Fetch one user by name. Returns None if no row matches. Names are not unique, so this returns the first match."""
    return db.query(User).filter(User.name == user_name).first()


def list_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    """Return a page of users. `skip` is how many rows to jump over, `limit` is the max returned."""
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, updates: dict) -> User | None:
    """Change one user. Only keys in ALLOWED_USER_UPDATES are written; other keys are ignored.

    This protects fields like id, password_hash, or created_at from being
    overwritten by whatever the API client sends. Returns None if no user matches.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    for key, value in updates.items():
        if key in ALLOWED_USER_UPDATES:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete one user. Returns True if a row was deleted, False if no user matched."""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
