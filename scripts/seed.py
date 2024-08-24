import asyncio
from sqlalchemy.future import select
from sqlalchemy import insert
from app.database import engine, Base, AsyncSessionLocal
from app.models import Quest

async def seed_db():
    # Example data to seed
    quests_data = [
        {"title": "First Quest", "description": "Complete your first challenge."},
        {"title": "Second Quest", "description": "Explore the application."},
    ]

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Insert data into the "quests" table
    async with AsyncSessionLocal() as session:
        async with session.begin():
            for quest_data in quests_data:
                query = insert(Quest).values(**quest_data)
                await session.execute(query)
            await session.commit()

if __name__ == "__main__":
    asyncio.run(seed_db())
