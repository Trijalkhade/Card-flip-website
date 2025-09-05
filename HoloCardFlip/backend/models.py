# backend/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)  # long enough for bcrypt
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # link to member profile
    member = relationship("Member", back_populates="user", uselist=False)

class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)
    bio = Column(Text, default="")

    # link back to user
    user = relationship("User", back_populates="member")

    achievements = relationship("Achievement", back_populates="member", cascade="all, delete-orphan")

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    title = Column(String)

    member = relationship("Member", back_populates="achievements")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    start_time = Column(DateTime)
    seats = Column(Integer, default=0)
