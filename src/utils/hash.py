import os
import hashlib
import secrets

from dotenv import load_dotenv

load_dotenv()
prefix = os.getenv("KEY_PREFIX")

def generate_api_key() -> str:
    token = secrets.token_urlsafe(32)
    return f"{prefix}_{token}"

def hash(s: str) -> str:
    m = hashlib.sha256()
    m.update(s.encode())
    return str(m.hexdigest())
