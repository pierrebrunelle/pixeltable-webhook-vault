"""Queries over the webhooks table."""
import pixeltable as pxt

from models import Webhooks


@pxt.query
def deliveries_for(event: str):
    """Signed deliveries for one event type."""
    return Webhooks.where(Webhooks.event == event).select(
        Webhooks.id, Webhooks.name, Webhooks.host, Webhooks.signature
    ).order_by(Webhooks.name)
