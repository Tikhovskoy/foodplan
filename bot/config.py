import os
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(project_root, ".env"))

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN is not set in .env")

_admins = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(x) for x in _admins.split(",") if x.strip().isdigit()]
