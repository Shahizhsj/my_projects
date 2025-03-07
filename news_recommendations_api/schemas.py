from typing import Optional, List
from pydantic import BaseModel

class User_Sign(BaseModel):
    name: str
    email: str
    password: str

class User_Login(BaseModel):
    name: str
    email: str

class Article(BaseModel):
    source: str  # Changed from source_name to source
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    urlToImage: Optional[str]
    publishedAt: str
    content: Optional[str]

class NewsResponse(BaseModel):
    status: str
    totalResults: int
    articles: List[Article]