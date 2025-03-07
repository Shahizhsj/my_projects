from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text,DateTime
from datetime import datetime
class User(Base):
    __tablename__ = 'usertable'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

class News(Base):
    __tablename__ = 'new'
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String,nullable=True)  # Changed from source_name to match NewsAPI structure
    author = Column(String, nullable=True)
    title = Column(String,nullable=True)
    description = Column(Text, nullable=True)
    url = Column(String,nullable=True)
    urlToImage = Column(String, nullable=True)
    publishedAt = Column(String,nullable=True)
    content = Column(Text, nullable=True)

class UserNewsInteraction(Base):
    __tablename__='user_news_interactions'
    post_id= Column(Integer, primary_key=True)
    user_id=Column(Integer)
    interaction_type=Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

