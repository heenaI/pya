
from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

# Family Table
class Family(Base):
    __tablename__ = "family"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    members = relationship("User", back_populates="family", cascade="all, delete")


# Users Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=True)
    role = Column(String(50), CheckConstraint("role IN ('parent', 'child', 'grand_parent', 'friend')"), nullable=False)
    family_id = Column(Integer, ForeignKey("family.id", ondelete="CASCADE"), index=True)
    family = relationship("Family", back_populates="members")
    google_token = Column(String, nullable=True)


# Preferences Table
class Preferences(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(String(50), CheckConstraint("type IN ('meal', 'allergy', 'shopping', 'other')"), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(Text, nullable=False)

    user = relationship("User", back_populates="preferences") 


# Events Table
class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    source = Column(String(50), CheckConstraint("source IN ('manual', 'google_calendar')"), default="manual")
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), index=True)
    user = relationship("User", back_populates="events")

User.events = relationship("Events", back_populates="user")
User.preferences = relationship("Preferences", back_populates="user")
