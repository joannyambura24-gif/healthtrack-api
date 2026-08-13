from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from database import create_db, get_session
from sqlmodel import Session

from models.user import User, UserCreate, UserResponse

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_current_active_user,
)

app = FastAPI(title="HealthTrack API")


@app.on_event("startup")
def startup():
    create_db()


@app.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, session: Session = Depends(get_session)):

    existing = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")

    existing_email = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):

    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@app.get("/users/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Logged out successfully"}
