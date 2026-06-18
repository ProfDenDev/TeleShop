# app/config.py
# ver 1.3
# updated: 2026-06-16 01:10 UTC+3

import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)

ADMIN_ID = int(
    os.getenv(
        "ADMIN_ID",
        "0",
    )
)

DB_PATH = os.getenv(
    "DB_PATH",
    "storage/db/shop.db",
)

IMPORT_PHOTOS_CHAT_ID = int(
    os.getenv(
        "IMPORT_PHOTOS_CHAT_ID",
        "0",
    )
)
