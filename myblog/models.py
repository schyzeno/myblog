from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from myblog.database import Base
import datetime

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    body = Column(Text, nullable=True)
    timestamp = Column(DateTime)
    hidden = Column(Boolean, nullable=False)
    

    def __init__(self, title=None, body=None, timestamp=datetime.datetime.now(), hidden = False):
        self.title = title
        self.body = body
        self.timestamp = timestamp
        self.hidden = hidden

    def __repr__(self):
        return '<Post %r, %r>' % (self.id,self.title)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50),nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))

    post = relationship("Post", backref="posts")

    def __init__(self, name=None, post_id=None):
        self.name = name
        self.post_id = post_id

    def __repr__(self):
        return "<Category (%r)>" % self.name
