"""Webhook Vault API built with Pixeltable.

    export WEBHOOK_HMAC_SECRET=<any-long-random-string>
    pxt schema update app.py vault
    pxt service run app.py vault
"""
import pixeltable as pxt
import pixeltable.functions as pxtf
from pixeltable.serving import FastAPIRouter

from udfs import digest_payload, sign_payload, target_host

# ---- tables ----
TableModel = pxt.model_base()


class Webhooks(TableModel, name='webhooks'):
    id = pxt.Column(value=pxtf.uuid.uuid7(), primary_key=True)
    name: pxt.String
    url: pxt.String
    event: pxt.String
    payload: pxt.String

    host = target_host(url)
    digest = digest_payload(payload)
    signature = sign_payload(event, payload)


# ---- queries ----
@pxt.query
def deliveries_for(event: str):
    """Signed deliveries for one event type."""
    return Webhooks.where(Webhooks.event == event).select(
        Webhooks.id, Webhooks.name, Webhooks.host, Webhooks.signature
    ).order_by(Webhooks.name)


# ---- routes ----
vault_api = FastAPIRouter(name='vault_api')
vault_api.add_insert_route(
    Webhooks, path='/webhooks',
    inputs=[Webhooks.name, Webhooks.url, Webhooks.event, Webhooks.payload],
    outputs=[Webhooks.id, Webhooks.host, Webhooks.digest, Webhooks.signature],
)
vault_api.add_compute_route(Webhooks, path='/sign', inputs=[Webhooks.event, Webhooks.payload],
                            outputs=[Webhooks.digest, Webhooks.signature])
vault_api.add_delete_route(Webhooks, path='/webhooks/delete')
vault_api.add_query_route(path='/webhooks/by-event', query=deliveries_for, method='get')
