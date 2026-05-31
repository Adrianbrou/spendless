from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from schemas import SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate
from service import subscription_service
from database import get_db


router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


# Note: until auth is wired up, routes that need the logged-in user's id take
# `user_id` as a query parameter. Once auth exists, this comes from the token.


@router.post(
    "/",
    response_model=SubscriptionResponse,
    status_code=201,
    summary="Add a subscription",
    description="Add a recurring charge for the given user. Returns 409 if a subscription with this name already exists.",
)
def create_subscription(user_id: int, data: SubscriptionCreate, db: Session = Depends(get_db)) -> SubscriptionResponse:
    """Create a subscription from the request body and return the saved subscription.

    Maps the service layer's ValueError ("Subscription already exists") to HTTP 409.
    """
    try:
        return subscription_service.register_subscription(db, user_id, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get(
    "/",
    response_model=list[SubscriptionResponse],
    summary="List all subscriptions for a user",
)
def get_all_subscriptions(user_id: int, db: Session = Depends(get_db)) -> list[SubscriptionResponse]:
    """Return every subscription that belongs to the given user, including inactive ones.

    Empty list is a valid response.
    """
    return subscription_service.get_all_subscriptions(db, user_id)


@router.get(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
    summary="Get one subscription by id",
)
def get_subscription_by_id(subscription_id: int, db: Session = Depends(get_db)) -> SubscriptionResponse:
    """Fetch one subscription by id. Maps ValueError ("Subscription not found") to HTTP 404."""
    try:
        return subscription_service.get_subscription(db, subscription_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
    status_code=200,
    summary="Update subscription info",
)
def update_subscription(subscription_id: int, data: SubscriptionUpdate, db: Session = Depends(get_db)) -> SubscriptionResponse:
    """Update fields on an existing subscription.

    To cancel a subscription, send `active: false` through this rather than
    deleting. Maps ValueError ("Subscription not found") to HTTP 404.
    """
    try:
        return subscription_service.update_subscription(db, subscription_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{subscription_id}",
    response_model=bool,
    status_code=200,
    summary="Delete a subscription",
)
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)) -> bool:
    """Delete a subscription by id and return True on success.

    Prefer setting `active` to False via PATCH if you want to keep history.
    Maps ValueError ("Subscription not found") to HTTP 404.
    """
    try:
        return subscription_service.delete_subscription(db, subscription_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
