from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models

SECRET_KEY= "938Y42CHIRANJEEVAUPPALA28946323"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

pwd_context=CryptContext(schemas=["bcrypt"], deprecated="auto")
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_pasword:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict)-> str:
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_token(token:str)->dict:
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
def get_current_user(token: str= Depends(oauth2_scheme),
                     db: Session=Depends(get_db)):
    credentials_exception=HTTPException(
        ststus_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticatie":"Bearer"}
    )
    payload=verify_token(token)
    if payload in None:
        raise credentials_exception
    email: str =payload.get("sub")
    if email is None:
        raise credentials_exception
    user=db.query(models.User).filter(models.User.email==email).first()
    if user is None:
        raise credentials_exception
    return user