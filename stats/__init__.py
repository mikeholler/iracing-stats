import os
from pyracing.client import Client

__all__ = [
    "MICROS_IN_DAY",
    "MY_CUSTOMER_ID",
    "pyracing_client",
]


MICROS_IN_DAY = 24 * 60 * 60 * 1_000_000
MY_CUSTOMER_ID = 404787

username = os.getenv("IRACING_USERNAME")
password = os.getenv("IRACING_PASSWORD")
pyracing_client = Client(username=username, password=password)
