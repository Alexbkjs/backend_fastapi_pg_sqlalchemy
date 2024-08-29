from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models import User as UserModel, Quest as QuestModel, UserQuestProgress as UserQuestProgressModel, Achievement as AchievementModel, UserAchievementModel
from app.schemas import User as UserSchema, Quest as QuestSchema
from uuid import UUID

from sqlalchemy.future import select  # Import select for query building
from sqlalchemy.orm import selectinload, joinedload  # Import selectinload for eager loading of related rows

# Function to delete a user by their ID (Telegram_id) in a cascade manner
async def delete_user_by_id(db: AsyncSession, user_id: int):
    # Create a select query to find a user with the given ID and load related entities if necessary
    query = select(UserModel).filter_by(telegram_id=user_id).options(selectinload(UserModel.quest_progress), selectinload(UserModel.achievements)) 
    result = await db.execute(query)  # Execute the query asynchronously
    user = result.scalar_one_or_none()  # Get the single result (or None if no user found)
    
    # If a user is found, delete it and commit the transaction
    if user:
        await db.delete(user)
        await db.commit()
        return True  # Return True if the deletion was successful
    return False  # Return False if no user was found


async def create_user(db: AsyncSession, user: UserSchema) -> UserModel:
    """
    Create a new user in the database.

    - **db**: Database session dependency.
    - **user**: Pydantic model containing user data.
    
    Returns the created user instance.
    """
    # Create a new User model instance, including the selected role
    new_user = UserModel(
        telegram_id=user.telegram_id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        language_code=user.language_code,
        is_premium=user.is_premium,
        allows_write_to_pm=user.allows_write_to_pm,
        role=user.role  # Include the selected role
    )
    
    # Add the new User instance to the session
    db.add(new_user)
    
    # Commit the transaction to persist the new User instance
    await db.commit()
    
    # Refresh the instance to load any database-generated fields like 'id'
    await db.refresh(new_user)
    
    return new_user



# Function to retrieve a user by their Telegram ID (tID)

    # Since Telegram ID is bigint in regarding to Postgres integer type make sure that you are defining the User model for the "users" table
    # with telegram_id = Column(BigInteger, unique=True, index=True)  # Telegram ID

# async def get_user_by_tID(db: AsyncSession, telegram_id: int):
#     # Create a select query to find a user with the given tID

#     query = select(UserModel).where(UserModel.telegram_id == telegram_id)
#     result = await db.execute(query)  # Execute the query asynchronously
#     user = result.scalars().first()  # Get the first result (or None if no user found)
#     # Return the user as a User if found, otherwise None

#     # Convert the SQLAlchemy model instance to a dictionary before validating
#     user_dict = user.__dict__ if user else None
    
#     # Return the user as a User if found, otherwise None
#     return User.model_validate(user_dict) if user_dict else None


async def get_user_by_tID(db: AsyncSession, telegram_id: int):
    # Create a select query to find a user with the given telegram_id and load related quest progress and quests
    query = (
        select(UserModel)
        .where(UserModel.telegram_id == telegram_id)
        .options(
            joinedload(UserModel.quest_progress).joinedload(UserQuestProgressModel.quest),
            joinedload(UserModel.achievements).joinedload(UserAchievementModel.achievement)  # Load the Achievement through UserAchievementModel

        )
    )

    # new_user_data = await db.query(User).options(joinedload(User.achievements)).filter_by(telegram_id=user_data.get('telegram_id')).first()

    
    result = await db.execute(query)  # Execute the query asynchronously
    user = result.scalars().first()  # Get the first result (or None if no user found)
    
    # Convert the SQLAlchemy model instance to a dictionary before validating
    user_dict = user.__dict__ if user else None
    
    # Return the user as a UserSchema with loaded quests if found, otherwise None
    return UserSchema.model_validate(user_dict) if user_dict else None



# Function to create a new quest in the database
async def create_quest(quest: QuestSchema, db: AsyncSession):
    # Create an insert query for the QuestModel table with the provided quest data
    query = QuestModel.__table__.insert().values(title=quest.title, description=quest.description)
    result = await db.execute(query)  # Execute the query asynchronously
    await db.commit()  # Commit the transaction
    # Return the quest data with the newly inserted ID
    return {**quest.model_dump(), "id": result.inserted_primary_key[0]}

# Function to retrieve a list of quests with optional pagination
async def get_quests(db: AsyncSession, skip: int = 0, limit: int = 10):
    # Create a select query to retrieve quests with pagination (offset and limit)
    query = select(QuestModel).offset(skip).limit(limit)
    result = await db.execute(query)  # Execute the query asynchronously
    # Return a list of quests
    return result.scalars().all()
    



async def assign_initial_quests(db: AsyncSession, user_id: UUID):
    """
    Assign 4 quests to a new user, with 2 being blocked and 2 being active.

    - **db**: Database session dependency.
    - **user_id**: ID of the newly created user.
    """

    # Fetch quests from the database (modify as needed to suit your schema and requirements)
    result = await db.execute(
        select(QuestModel).limit(4)  # Fetching 4 quests; adjust as needed
    )
    quests = result.scalars().all()

    if len(quests) < 4:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Not enough quests available to assign."
        )

    # Assign quests, with 2 blocked and 2 not blocked
    for idx, quest in enumerate(quests):
        status = "active" if idx >= 2 else "blocked"
        await db.execute(
            UserQuestProgressModel.__table__.insert().values(
                user_id=user_id,
                quest_id=quest.id,
                status=status,
                is_locked=status == "blocked"  # Using is_locked to reflect blocked status
            )
        )
    
    await db.commit()

async def assign_initial_achievements(db: AsyncSession, user_id: UUID):
    """
    Assign specific achievements to a new user, such as basic achievements for registration.

    - **db**: Database session dependency.
    - **user_id**: ID of the newly created user.
    """

    # Predefine the list of specific achievements (e.g., by achievement name or type)
    achievement_names = ["Початківець", "Новачок", "Дослідник", "Воїн"]

    # Fetch the specific achievements from the database
    result = await db.execute(
        select(AchievementModel).where(AchievementModel.name.in_(achievement_names))
    )
    achievements = result.scalars().all()

    if len(achievements) < 4:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Not enough specific achievements available to assign."
        )
    # Assign achievements, with 2 active and 2 blocked
    for idx, achievement in enumerate(achievements):
        status = "active" if idx >= 2 else "blocked"
        is_locked = False if status == "active" else True
        await db.execute(
            UserAchievementModel.__table__.insert().values(
                user_id=user_id,
                achievement_id=achievement.id,
                status=status,
                is_locked=is_locked
            )
        )
    
    await db.commit()
