"""Seed a few webhook registrations (needs WEBHOOK_HMAC_SECRET in the environment).

Usage:
    python seed.py            # seeds the local `vault` catalog directory
    python seed.py my_dir     # or another directory you passed to `pxt schema update`
"""
import sys
from pathlib import Path

import pixeltable as pxt

target = sys.argv[1] if len(sys.argv) > 1 else 'vault'
HERE = Path(__file__).resolve().parent

SEED = {
    'webhooks': [
        {'name': 'orders-to-erp', 'url': 'https://erp.example.com/hooks/orders', 'event': 'order.created', 'payload': '{"order_id": 1042, "total": 59.9}'},
        {'name': 'refunds-to-slackbot', 'url': 'https://bot.example.net/refunds', 'event': 'refund.issued', 'payload': '{"order_id": 977, "amount": 12.5}'},
        {'name': 'orders-to-warehouse', 'url': 'https://wh.example.org/in', 'event': 'order.created', 'payload': '{"order_id": 1043, "total": 18.0}'},
    ],
}

for table_name, rows in SEED.items():
    t = pxt.get_table(f'{target}/{table_name}')
    if t.count() > 0:
        print(f'{target}/{table_name} already has {t.count()} rows; skipping')
        continue
    for row in rows:
        for k, v in row.items():
            if isinstance(v, str) and v.startswith('data/'):
                row[k] = str(HERE / v)   # local sample media file
    t.insert(rows)
    print(f'inserted {len(rows)} rows into {target}/{table_name}')
