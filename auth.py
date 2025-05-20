from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .database import get_db
import psycopg2
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s", (form_data.username,))
        user = cur.fetchone()
    
    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=400, detail="Email atau password salah")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email'], "role": user['role'], "user_id": user['id']},
        expires_delta=access_token_expires
    )
    
    # Redirect berdasarkan role
    if user['role'] == 'mahasiswa':
        redirect_url = "/mahasiswa/dashboard"
    else:
        redirect_url = "/dosen/dashboard"
    
    response = RedirectResponse(url=redirect_url, status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response