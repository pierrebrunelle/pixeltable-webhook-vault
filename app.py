"""Webhook Vault API built with Pixeltable.

    export WEBHOOK_HMAC_SECRET=<any-long-random-string>
    pxt schema update app.py vault
    pxt service run app.py vault
"""
from pixeltable.serving import FastAPIRouter

from models import TableModel, Webhooks  # noqa: F401  (TableModel lets `pxt schema` find the models)
from queries import deliveries_for

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
