from sqlalchemy.orm import Session
from models import User


# whitelist for users updates that use email and name
ALLOWED_USER_UPDATES = {"email", "name"}


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str) -> User | None:
    return db.query(User).filter(User.email == user_email).first()


def get_user_by_name(db: Session, user_name: str) -> User | None:
    return db.query(User).filter(User.name == user_name).first()


def list_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, updates: dict) -> User | None:
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
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
