from pydantic import BaseModel  # type: ignore[import]
from typing import Optional

class ItemBase(BaseModel):
    employeeid: int
    employeename: str
    emailid: Optional[str]=None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    #employeeid: Optional[int] = None
    employeename: Optional[str] = None
    emailid: Optional[str] = None

class ItemResponse(ItemBase):
    #employeeid: int

    model_config = {
        "from_attributes": True,
    }
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    class Config:
        from_attributes=True
class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str