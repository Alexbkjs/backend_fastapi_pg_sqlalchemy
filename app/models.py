from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base  # Import the base class for declarative table definitions from your database module

# Define the Quest model for the "quests" table
class Quest(Base):
    __tablename__ = "quests" # The table name in the database

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

# Define the User model for the "users" table
class User(Base):
    __tablename__ = 'users' # The table name in the database

    id = Column(Integer, primary_key=True, index=True)
    tID = Column(Integer, unique=True, index=True)  # Telegram ID
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    language_code = Column(String)
    is_premium = Column(Boolean)
    allows_write_to_pm = Column(Boolean)
