from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    query: str
    content: str

class UserResponse(BaseModel):
    resultCode: int
    message: str