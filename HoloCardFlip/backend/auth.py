# backend/auth.py
import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models import User

# --- Config ---
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set in environment or .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(tags=["auth"])


# --- Pydantic schemas for JSON requests
class SignupRequest(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str


# --- Helpers ---
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT with expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[str]:
    """Decode a JWT and return username (sub) if valid, else None."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


# --- Routes ---
@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="username already exists")

    user = User(username=data.username, password_hash=hash_password(data.password), full_name=data.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "user created", "username": user.username}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

    access_token = create_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_token(
        data={"sub": user.username},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "username": user.username
    }


@router.post("/refresh")
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh an access token using a valid refresh token."""
    username = decode_token(refresh_token)
    if not username:
        raise HTTPException(status_code=401, detail="invalid or expired refresh token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    new_access_token = create_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get("/me")
def get_me(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return {"username": user.username, "full_name": user.full_name}
