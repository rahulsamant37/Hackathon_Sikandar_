from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.schemas.token import TokenPayload
from app.schemas.user import User, UserCreate
from app.services.db import get_supabase_client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str) -> Optional[User]:
    supabase = get_supabase_client()
    response = supabase.table("users").select("*").eq("email", email).execute()
    
    if not response.data:
        return None
    
    user_data = response.data[0]
    if not verify_password(password, user_data["password_hash"]):
        return None
    
    return User(
        id=user_data["user_id"],
        email=user_data["email"],
        username=user_data["username"],
        role=user_data["role"],
        learning_preferences=user_data.get("learning_preferences")
    )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def register_user(user_data: UserCreate) -> User:
    supabase = get_supabase_client()
    
    # Check if user already exists
    response = supabase.table("users").select("*").eq("email", user_data.email).execute()
    if response.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_id = str(uuid4())
    new_user = {
        "user_id": user_id,
        "email": user_data.email,
        "username": user_data.username,
        "password_hash": get_password_hash(user_data.password),
        "role": user_data.role,
        "created_at": datetime.utcnow().isoformat(),
        "learning_preferences": {}
    }
    
    supabase.table("users").insert(new_user).execute()
    
    return User(
        id=user_id,
        email=user_data.email,
        username=user_data.username,
        role=user_data.role,
        learning_preferences={}
    )

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenPayload(sub=email)
    except JWTError:
        raise credentials_exception
    
    supabase = get_supabase_client()
    response = supabase.table("users").select("*").eq("email", token_data.sub).execute()
    
    if not response.data:
        raise credentials_exception
    
    user_data = response.data[0]
    
    return User(
        id=user_data["user_id"],
        email=user_data["email"],
        username=user_data["username"],
        role=user_data["role"],
        learning_preferences=user_data.get("learning_preferences")
    )
