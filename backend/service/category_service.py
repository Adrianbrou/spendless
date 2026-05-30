from sqlalchemy.orm import Session
from models import Category
from schemas import CategoryCreate, CategoryUpdate
from crud import category as category_crud


def register_category(db: Session, user_id: int, data: CategoryCreate) -> Category:
    """Create a new category for the given user. Raises ValueError if they already have one with this name.

    The client doesn't send user_id (that would be a security hole). The router
    reads it from the logged-in user and passes it in here, then we stitch it onto
    the model with `**data.model_dump(), user_id=user_id`.
    """
    existing = category_crud.get_category_by_name(db, user_id, data.name)
    if existing:
        raise ValueError("Category already exists")
    category = Category(**data.model_dump(), user_id=user_id)
    return category_crud.create_category(db, category)


def update_category(db: Session, category_id: int, data: CategoryUpdate) -> Category:
    """Change one category. Only fields the client actually sent are applied.

    Raises ValueError if the category does not exist.
    """
    updates = data.model_dump(exclude_unset=True)
    result = category_crud.update_category(db, category_id, updates)
    if not result:
        raise ValueError("Category not found")
    return result


def get_category(db: Session, category_id: int) -> Category:
    """Fetch one category by id. Raises ValueError if the category does not exist."""
    existing = category_crud.get_category_by_id(db, category_id)
    if not existing:
        raise ValueError("Category not found")
    return existing


def get_all_categories(db: Session, user_id: int) -> list[Category]:
    """Return every category that belongs to one user.

    Empty list is a valid answer (a new user has zero categories).
    """
    return category_crud.list_categories(db, user_id)


def delete_category(db: Session, category_id: int) -> bool:
    """Delete one category. Raises ValueError if the category does not exist.

    Cascade rules mean every expense, income, budget, and subscription
    pointing to this category gets deleted too.
    """
    deleted = category_crud.delete_category(db, category_id)
    if not deleted:
        raise ValueError("Category not found")
    return True
