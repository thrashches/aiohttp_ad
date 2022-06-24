import hashlib


def get_password_hash(raw_password: str) -> str:
    return hashlib.sha256(raw_password.encode()).hexdigest()
