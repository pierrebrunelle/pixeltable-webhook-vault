"""The webhooks table: payloads plus digest and signature computed columns."""
import pixeltable as pxt
import pixeltable.functions as pxtf

from udfs import digest_payload, sign_payload, target_host

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
