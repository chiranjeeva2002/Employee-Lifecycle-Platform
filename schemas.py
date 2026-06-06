from pydantic import BaseModel  # type: ignore[import]
from typing import Optional

class ItemBase(BaseModel):
    employeeid: int
    employeename: str
    emailid: str

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    employeeid: Optional[int] = None
    employeename: Optional[str] = None
    emailid: Optional[str] = None

class ItemResponse(ItemBase):
    employeeid: int

    model_config = {
        "from_attributes": True,
    }