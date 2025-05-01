from datetime import datetime, timezone, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict, token_expire: int):
    expire = datetime.now(timezone.utc) + timedelta(days=token_expire)
    data.update({"exp": expire})
    token = jwt.encode(
        data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return token


def decode_jwt_token(token: str):
    try:
        decode_token = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except (JWTError, AttributeError):
        return None
    if set(decode_token.keys()) != {"id", "exp"}:
        return None
    return decode_token
