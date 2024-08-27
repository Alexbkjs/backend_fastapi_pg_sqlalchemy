from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

# Enum for UserRole
class UserRole(str, Enum):
    adventurer = "adventurer"
    avatar = "avatar"
    kingdom = "kingdom"

# Base model for Quest data used for validation and serialization
class QuestBase(BaseModel):
    name: str
    image_url: str = ""
    description: str = ""
    award: str = ""
    goal: str = ""

# Model for creating a new quest, inherits from QuestBase
class QuestCreate(QuestBase):
    pass

# Model representing a quest including an ID, inherits from QuestBase
class Quest(QuestBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

# Base model for User data used for validation and serialization
class UserBase(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str
    username: str
    language_code: Optional[str]
    allows_write_to_pm: Optional[bool]
    is_premium: Optional[bool]
    user_class: Optional[str]
    image_url: Optional[str] = "https://quests-app-bucket.s3.eu-north-1.amazonaws.com/images/02.jpg"
    level: Optional[int] = 1
    points: Optional[int] = 100
    coins: Optional[int] = 1000
    role: Optional[UserRole] = None

# Model for creating a new user, inherits from UserBase
class UserCreate(UserBase):
    pass

# Model representing a user including an ID, inherits from UserBase
class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

# Base model for Achievement data used for validation and serialization
class AchievementBase(BaseModel):
    name: str
    description: str
    image_url: Optional[str]
    is_locked: Optional[bool] = True

# Model for creating a new achievement, inherits from AchievementBase
class AchievementCreate(AchievementBase):
    pass

# Model representing an achievement including an ID, inherits from AchievementBase
class Achievement(AchievementBase):
    id: UUID
    user_id: Optional[UUID]
    created_at: datetime
    updated_at: Optional[datetime] = None

# Base model for UserQuestProgress data used for validation and serialization
class UserQuestProgressBase(BaseModel):
    user_id: UUID
    quest_id: UUID
    status: str
    progress: Optional[float] = 0.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    is_locked: Optional[bool] = True

# Model for creating a new user quest progress, inherits from UserQuestProgressBase
class UserQuestProgressCreate(UserQuestProgressBase):
    pass

# Model representing user quest progress including an ID, inherits from UserQuestProgressBase
class UserQuestProgress(UserQuestProgressBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

# Base model for Requirement data used for validation and serialization
class RequirementBase(BaseModel):
    description: str
    quest_id: UUID

# Model for creating a new requirement, inherits from RequirementBase
class RequirementCreate(RequirementBase):
    pass

# Model representing a requirement including an ID, inherits from RequirementBase
class Requirement(RequirementBase):
    id: UUID

# Base model for Reward data used for validation and serialization
class RewardBase(BaseModel):
    description: str
    quest_id: UUID

# Model for creating a new reward, inherits from RewardBase
class RewardCreate(RewardBase):
    pass

# Model representing a reward including an ID, inherits from RewardBase
class Reward(RewardBase):
    id: UUID
