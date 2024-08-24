from pydantic import BaseModel

# Base model for Quest data used for validation and serialization
class QuestBase(BaseModel):
    title: str  # Title of the quest
    description: str  # Detailed description of the quest

# Model for creating a new quest, inherits from QuestBase
class QuestCreate(QuestBase):
    pass  # No additional fields or modifications

# Model representing a quest including an ID, inherits from QuestBase
class Quest(QuestBase):
    id: int  # Unique identifier for the quest

# Base model for User data used for validation and serialization
class UserBase(BaseModel):
    first_name: str  # User's first name
    last_name: str  # User's last name
    username: str  # User's username
    language_code: str  # Language code for the user
    is_premium: bool  # Indicates if the user has a premium account
    allows_write_to_pm: bool  # Indicates if the user allows receiving private messages

# Model for creating a new user, inherits from UserBase
class UserCreate(UserBase):  # Inherit from UserBase to avoid duplication
    id: int  # Unique identifier for the user

# Model representing a user including additional fields, inherits from UserBase
class User(UserBase):  # Inherit from UserBase to avoid duplication
    id: int  # Unique identifier for the user
    tID: int  # Telegram ID of the user

    class Config:
        from_attributes = True  # Enable reading from attributes in Pydantic V2
