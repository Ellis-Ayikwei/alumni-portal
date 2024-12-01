from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Text
from sqlalchemy.orm import relationship, backref
from models.basemodel import BaseModel, Base
from datetime import datetime

class Post(BaseModel, Base):
    __tablename__ = 'posts'
    
    title = Column(String(255), nullable=False)  # Allow for longer titles
    description = Column(Text, nullable=True)
    image_url = Column(String(255))  # URL to the image or video for the post/reel
    date_created = Column(DateTime, default=datetime.utcnow)
    
    # Foreign key relationship with User (post belongs to a user)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    
    # Foreign key relationship with Workout (post can be related to a specific workout)
    workout_id = Column(String(60), ForeignKey('workouts.id'), nullable=True)
    
    # One-to-many relationship with Comment (post can have many comments)
    comments = relationship('Comment', backref='post', lazy='dynamic')  # Consider dynamic for performance reasons
    
    # Add a date_updated field for tracking updates
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Comment(BaseModel, Base):
    __tablename__ = 'comments'
    content = Column(Text, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    
    # Foreign key relationship with Post (comment belongs to a post)
    post_id = Column(String(60), ForeignKey('posts.id'), nullable=False)
    
    # Foreign key relationship with User (comment belongs to a user)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    # Add a date_updated field for tracking updates
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
