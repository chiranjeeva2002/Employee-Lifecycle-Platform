from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import models, crud, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/items", response_model=list[schemas.ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return crud.get_all(db)

@app.get("/items/{employee_id}", response_model=schemas.ItemResponse)
def read_item(employee_id: int, db: Session = Depends(get_db)):
    item = crud.get_by_id(db, employee_id)
    if not item:
        raise HTTPException(status_code=404, detail="Employee ID not found")
    return item

@app.post("/items/", response_model=schemas.ItemResponse, status_code=201)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create(db, item)

@app.put("/items/{employee_id}", response_model=schemas.ItemResponse)
def update_item(employee_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    updated_item = crud.update(db, employee_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/items/{employee_id}", response_model=schemas.ItemResponse)
def delete_item(employee_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted