from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class QueryRequest(BaseModel):
    question: str
    context: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
