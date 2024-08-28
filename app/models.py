from app.database import Base  # Import the base class for declarative table definitions from your database module
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Float, DateTime, func, ForeignKey, Enum as PyEnum
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum

class UserRole(Enum):
    adventurer = "adventurer"
    avatar = "avatar"
    kingdom = "kingdom"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    user_class = Column(String, nullable=True)
    image_url = Column(String, nullable=True, default="https://quests-app-bucket.s3.eu-north-1.amazonaws.com/images/02.jpg")
    level = Column(Integer, default=1)
    points = Column(Integer, default=100)
    coins = Column(Integer, default=1000)
    role = Column(PyEnum(UserRole), nullable=True)  # Use Enum as the column type
    language_code = Column(String, nullable=True)
    is_premium = Column(Boolean, nullable=True)
    allows_write_to_pm = Column(Boolean, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    achievements = relationship("Achievement", back_populates="user")
    quests = relationship("UserQuestProgress", back_populates="user")

class Quest(Base):
    __tablename__ = "quests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    image_url = Column(String, default="")
    description = Column(String, default="")
    award = Column(String, default="")
    goal = Column(String, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    requirements = relationship("Requirement", back_populates="quest")
    rewards = relationship("Reward", back_populates="quest")
    user_quest_progress = relationship("UserQuestProgress", back_populates="quest")

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    is_locked = Column(Boolean, default=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    user = relationship("User", back_populates="achievements")

class UserQuestProgress(Base):
    __tablename__ = "user_quest_progress"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    quest_id = Column(UUID(as_uuid=True), ForeignKey('quests.id'), nullable=False)
    status = Column(String, nullable=False)
    progress = Column(Float, default=0.0)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    is_locked = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    user = relationship("User", back_populates="quests")
    quest = relationship("Quest", back_populates="user_quest_progress")

    

class Requirement(Base):
    __tablename__ = "requirements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String, nullable=False)
    quest_id = Column(UUID(as_uuid=True), ForeignKey('quests.id'), nullable=False)
    
    quest = relationship("Quest", back_populates="requirements")

class Reward(Base):
    __tablename__ = "rewards"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String, nullable=False)
    quest_id = Column(UUID(as_uuid=True), ForeignKey('quests.id'), nullable=False)
    
    quest = relationship("Quest", back_populates="rewards")
