from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas, security
from app.db import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed = security.hash_password(user.password)
    new_user = models.User(username=user.username, password=hashed)
    db.add(new_user); db.commit()
    return {"message": "User registered"}

@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=form.username).first()
    if not user or not security.verify_password(form.password, user.password):
        return {"error": "Invalid credentials"}
    token = security.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}