from sqlalchemy.orm import Session
from models import Subscription


ALLOWED_SUBSCRIPTION_UPDATES = {"name", "frequency", "active"}


def create_subscription(db: Session, subscription: Subscription) -> Subscription:
    """Save a new subscription to the database. Returns the saved subscription with its new id filled in."""
    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return subscription


def get_subscription_by_id(db: Session, subscription_id: int) -> Subscription | None:
    """Fetch one subscription by its unique id. Returns None if no row matches.

    Note: not scoped by user. The caller should check the returned subscription
    actually belongs to the logged-in user before exposing it.
    """
    return db.query(Subscription).filter(Subscription.id == subscription_id).first()


def get_subscription_by_name(db: Session, user_id: int, subscription_name: str) -> Subscription | None:
    """Fetch one of a given user's subscriptions by name.

    Scoped by user_id because two users can both have a "Netflix" subscription
    and they must not collide.
    """
    return db.query(Subscription).filter(Subscription.name == subscription_name, Subscription.user_id == user_id).first()


def list_subscriptions(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list[Subscription]:
    """Return a page of one user's subscriptions. `skip` is how many rows to jump over, `limit` is the max returned."""
    return db.query(Subscription).filter(Subscription.user_id == user_id).offset(skip).limit(limit).all()


def update_subscription(db: Session, subscription_id: int, updates: dict) -> Subscription | None:
    """Change one subscription. Only keys in ALLOWED_SUBSCRIPTION_UPDATES are written; other keys are ignored.

    To cancel a subscription, set `active` to False through this function instead of deleting it.
    That keeps the history around. Returns None if no subscription matches.
    """
    subscription = get_subscription_by_id(db, subscription_id)
    if not subscription:
        return None

    for key, value in updates.items():
        if key in ALLOWED_SUBSCRIPTION_UPDATES:
            setattr(subscription, key, value)

    db.commit()
    db.refresh(subscription)

    return subscription


def delete_subscription(db: Session, subscription_id: int) -> bool:
    """Delete one subscription. Returns True if a row was deleted, False if no subscription matched.

    Prefer setting `active` to False via update_subscription if you want to keep
    the row around for history. Use this only for genuine removal.
    """
    subscription = get_subscription_by_id(db, subscription_id)
    if not subscription:
        return False

    db.delete(subscription)
    db.commit()

    return True
