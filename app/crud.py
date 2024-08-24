from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User as UserModel, Quest as QuestModel
from app.schemas import UserCreate, User as UserSchema, QuestCreate

# Function to create a new user in the database
async def create_user(db: AsyncSession, user: UserCreate):
    # Create an insert query for the UserModel table with the provided user data
    query = UserModel.__table__.insert().values(
        tID=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        language_code=user.language_code,
        is_premium=user.is_premium,
        allows_write_to_pm=user.allows_write_to_pm,
    )
    result = await db.execute(query)  # Execute the query asynchronously
    await db.commit()  # Commit the transaction
    # Return the user data with the newly inserted ID
    return {**user.dict(), "id": result.inserted_primary_key[0]}

# Function to retrieve a user by their Telegram ID (tID)
async def get_user_by_tID(db: AsyncSession, tID: int):
    # Create a select query to find a user with the given tID
    query = select(UserModel).where(UserModel.tID == tID)
    result = await db.execute(query)  # Execute the query asynchronously
    user = result.scalars().first()  # Get the first result (or None if no user found)
    # Return the user as a UserSchema if found, otherwise None
    return UserSchema.from_orm(user) if user else None

# Function to delete a user by their ID(TelegramID)
async def delete_user_by_id(db: AsyncSession, user_id: int):
    # Create a select query to find a user with the given ID
    query = select(UserModel).filter_by(tID=user_id)
    result = await db.execute(query)  # Execute the query asynchronously
    user = result.scalar_one_or_none()  # Get the single result (or None if no user found)
    
    # If a user is found, delete it and commit the transaction
    if user:
        await db.delete(user)
        await db.commit()
        return True  # Return True if the deletion was successful
    return False  # Return False if no user was found

# Function to create a new quest in the database
async def create_quest(quest: QuestCreate, db: AsyncSession):
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
