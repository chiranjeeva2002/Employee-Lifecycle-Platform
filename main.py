from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException,status
import models, crud, schemas
from database import engine, get_db
from fastapi.security import OAuth2PasswordRequestForm
from auth import (verify_password,create_access_token,get_current_user)

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# .....Auth Routes....
@app.post("/register",response_model=schemas.UserResponse)
def register(user: schemas.UserCreate,db:Session=Depends(get_db)):
    try:
        import traceback
        print(f"User data: {user}")
        print(f"Password: '{user.password}' (len={len(user.password)})")
        existing=crud.get_user_by_email(db,user.email)
        if existing:
            raise HTTPException(status_code=400,detail="Email already registered")
        return crud.create_user(db,user)
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Register Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/login",response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login-json",response_model=schemas.Token)
def login_json(login: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, login.email)
    if not user or not verify_password(login.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me",response_model=schemas.UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user


#.... emaployee get,post,put,delete    

@app.get("/employees", response_model=list[schemas.ItemResponse])
def read_items(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.get_all(db)

@app.get("/employees/{employee_id}", response_model=schemas.ItemResponse)
def read_item(employee_id: int, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    item = crud.get_by_id(db, employee_id)
    if not item:
        raise HTTPException(status_code=404, detail="Employee ID not found")
    return item

@app.post("/employees/", response_model=schemas.ItemResponse, status_code=201)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    return crud.create(db, item)

@app.put("/employees/{employee_id}", response_model=schemas.ItemResponse)
def update_item(employee_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    updated_item = crud.update(db, employee_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/employees/{employee_id}", response_model=schemas.ItemResponse)
def delete_item(employee_id: int, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    deleted = crud.delete(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted