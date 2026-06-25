from sqlalchemy.orm import Session
from models import Item, User
from schemas import ItemCreate, ItemUpdate, UserCreate
from auth import hash_password


def get_all(db: Session):
    return db.query(Item).all()

def get_by_id(db: Session, employee_id: int):
    return db.query(Item).filter(Item.employeeid == employee_id).first()

def create(db: Session, item: ItemCreate):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update(db: Session, employee_id: int, item: ItemUpdate):
    db_item = db.query(Item).filter(Item.employeeid == employee_id).first()
    if not db_item:
        return None
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete(db: Session, employee_id: int):
    db_item = db.query(Item).filter(Item.employeeid == employee_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item

def create_user(db:Session, user: UserCreate):
    hashed= hash_password(user.password)
    db_user=User(
        username=user.username,
        email=user.email,
        password=hashed,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email==email).first()
