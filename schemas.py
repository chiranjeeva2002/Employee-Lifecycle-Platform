from pydantic import BaseModel  # type: ignore[import]
from typing import Optional
from typing import Literal


#----- employees schemas----

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


# ----  Users schemas-----

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Literal["admin","employee"] = "employee"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    role:str
    class Config:
        from_attributes=True
class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

#----- HR Q&A Schemas ----

class HRQuestion(BaseModel):
    question: str

class HRAnswer(BaseModel):
    question: str
    answer: str
    sources: list[str]

class IngestResponse(BaseModel):
    message: str
    chunks_created: int