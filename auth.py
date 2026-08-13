from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from database.session import get_session
from models.user import User
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
def hash_password(password: str) -> str:
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pass


def create_access_token(data: dict, expires_delta=None):
    pass


def decode_access_token(token: str):
    pass


def get_current_user(
    token=None,
    session=None
):
    pass


def get_current_active_user(current_user):
    pass


def get_current_doctor(current_user):
    pass


def get_current_admin(current_user):
    pass