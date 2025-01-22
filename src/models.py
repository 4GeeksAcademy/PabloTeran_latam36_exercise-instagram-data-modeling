import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)

    # Relaciones
    user_posts = relationship("Post", back_populates="author")
    user_comments = relationship("Comment", back_populates="commenter")
    followers = relationship("Follower", foreign_keys='Follower.following_id', back_populates="followed_user")
    following = relationship("Follower", foreign_keys='Follower.follower_id', back_populates="follower_user")

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)

    # Relaciones
    author = relationship("User", back_populates="user_posts")
    post_comments = relationship("Comment", back_populates="related_post")
    media_files = relationship("Media", back_populates="attached_post")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    commenter_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    # Relaciones
    commenter = relationship("User", back_populates="user_comments")
    related_post = relationship("Post", back_populates="post_comments")

class Media(Base):
    __tablename__ = 'media_files'
    id = Column(Integer, primary_key=True)
    media_type = Column(String(50), nullable=False)
    url = Column(String(300), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    # Relaciones
    attached_post = relationship("Post", back_populates="media_files")

class Follower(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    following_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relaciones
    follower_user = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed_user = relationship("User", foreign_keys=[following_id], back_populates="followers")

## SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
