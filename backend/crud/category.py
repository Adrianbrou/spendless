from models import Category, CategoryType
from sqlalchemy.orm import Session

ALLOWED_CATEGORIES_UPDATES = {"name", "type", "color"}


def create_category(db: Session, category: Category) -> Category:
    """Save a new category to the database. Returns the saved category with its new id filled in."""
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category_by_id(db: Session, category_id: int) -> Category | None:
    """Fetch one category by its unique id. Returns None if no row matches.

    Note: not scoped by user. The caller (router or service layer) should check
    that the returned category actually belongs to the logged-in user before exposing it.
    """
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_name(db: Session, user_id: int, category_name: str) -> Category | None:
    """Fetch one of a given user's categories by name.

    Scoped by user_id because two users can have the same category name
    (User A's "Food" must not collide with User B's "Food").
    """
    return db.query(Category).filter(Category.name == category_name, Category.user_id == user_id).first()


def get_category_by_type(db: Session, user_id: int, category_type: CategoryType) -> Category | None:
    """Fetch one of a given user's categories by type (EXPENSE or INCOME).

    Scoped by user_id for the same reason as get_category_by_name.
    """
    return db.query(Category).filter(Category.type == category_type, Category.user_id == user_id).first()


def list_categories(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list[Category]:
    """Return a page of one user's categories. `skip` is how many rows to jump over, `limit` is the max returned."""
    return db.query(Category).filter(Category.user_id == user_id).offset(skip).limit(limit).all()


def update_category(db: Session, category_id: int, updates: dict) -> Category | None:
    """Change one category. Only keys in ALLOWED_CATEGORIES_UPDATES are written; other keys are ignored.

    This protects fields like id, user_id, or created_at from being
    overwritten by whatever the API client sends. Returns None if no category matches.
    """
    category = get_category_by_id(db, category_id)
    if not category:
        return None

    for key, value in updates.items():
        if key in ALLOWED_CATEGORIES_UPDATES:
            setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> bool:
    """Delete one category. Returns True if a row was deleted, False if no category matched.

    Because of the CASCADE rule on the foreign keys in models.py, deleting a category
    also deletes its expenses, incomes, budgets, and subscriptions.
    """
    category = get_category_by_id(db, category_id)
    if not category:
        return False

    db.delete(category)
    db.commit()

    return True
