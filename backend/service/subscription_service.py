from sqlalchemy.orm import Session
from models import Subscription
from schemas import SubscriptionCreate, SubscriptionUpdate
from crud import subscription as subscription_crud


def register_subscription(db: Session, user_id: int, data: SubscriptionCreate) -> Subscription:
    """Create a new subscription for the given user.

    Raises ValueError if the user already has a subscription with this name
    ("Netflix" twice for the same user is confusing in the UI).
    """
    existing = subscription_crud.get_subscription_by_name(db, user_id, data.name)
    if existing:
        raise ValueError("Subscription already exists")
    subscription = Subscription(**data.model_dump(), user_id=user_id)
    return subscription_crud.create_subscription(db, subscription)


def update_subscription(db: Session, subscription_id: int, data: SubscriptionUpdate) -> Subscription:
    """Change one subscription. Only fields the client actually sent are applied.

    To cancel a subscription, set `active` to False through this rather than deleting.
    Raises ValueError if the subscription does not exist.
    """
    updates = data.model_dump(exclude_unset=True)
    result = subscription_crud.update_subscription(db, subscription_id, updates)
    if not result:
        raise ValueError("Subscription not found")
    return result


def get_subscription(db: Session, subscription_id: int) -> Subscription:
    """Fetch one subscription by id. Raises ValueError if the subscription does not exist."""
    existing = subscription_crud.get_subscription_by_id(db, subscription_id)
    if not existing:
        raise ValueError("Subscription not found")
    return existing


def get_all_subscriptions(db: Session, user_id: int) -> list[Subscription]:
    """Return every subscription that belongs to one user.

    Empty list is a valid answer. Includes inactive (cancelled) ones too.
    """
    return subscription_crud.list_subscriptions(db, user_id)


def delete_subscription(db: Session, subscription_id: int) -> bool:
    """Delete one subscription. Raises ValueError if the subscription does not exist.

    Prefer setting `active` to False via update_subscription if you want to keep
    the row around for history. Use this only for genuine removal.
    """
    deleted = subscription_crud.delete_subscription(db, subscription_id)
    if not deleted:
        raise ValueError("Subscription not found")
    return True
