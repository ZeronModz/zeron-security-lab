import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_api_key(key: str) -> str:
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    return pwd_context.hash(key_hash)


def verify_api_key(plain_key: str, hashed_key: str) -> bool:
    key_hash = hashlib.sha256(plain_key.encode()).hexdigest()
    return pwd_context.verify(key_hash, hashed_key)


def generate_api_key() -> str:
    return f"zsl_{secrets.token_urlsafe(32)}"


def create_jwt_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.jwt_expiration_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_jwt_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None
