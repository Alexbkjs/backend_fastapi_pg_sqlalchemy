# Standard Library Imports
import hashlib  # For hashing functions
import hmac  # For HMAC (hash-based message authentication code)
import json  # For JSON parsing
import urllib.parse  # For URL parsing and decoding

# Third-Party Imports
from fastapi import APIRouter, HTTPException, Depends  # FastAPI components for routing and error handling
from pydantic import BaseModel  # Pydantic for data validation
from sqlalchemy.ext.asyncio import AsyncSession  # SQLAlchemy for asynchronous database operations

# Local Application Imports
from app.schemas import UserCreate  # User data validation schema
from app.crud import get_user_by_tID, create_user, delete_user_by_id  # CRUD operations
from app.database import get_db  # Database session dependency

from dotenv import load_dotenv  # For loading environment variables from .env file
import os  # For accessing environment variables

# Load environment variables from .env file
load_dotenv()

# Access environment variables using os.getenv
bot_token = os.getenv("BOT_TOKEN")  # Retrieve the bot token from environment variables

router = APIRouter()  # Create an APIRouter instance for handling routes

# Define the data model for the initial data payload
class InitData(BaseModel):
    initDataRaw: str  # Raw data received from the client


# Endpoint to verify initial data and handle user authentication
@router.get("/users")
async def verify_init_data(init_data: InitData, db: AsyncSession = Depends(get_db)):
    return {"Testing get response": 'Hello'}

# Endpoint to delete a user by ID
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a user by their ID.

    - **user_id**: The ID of the user to delete.
    - **db**: Database session dependency, automatically provided by FastAPI.
    
    Returns a success message if the user is deleted, or raises a 404 error if not found.
    """
    user_deleted = await delete_user_by_id(db, user_id)
    if user_deleted:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Endpoint to verify initial data and handle user authentication
@router.post("/users")
async def verify_init_data(init_data: InitData, db: AsyncSession = Depends(get_db)):
    return {"InitData": init_data}
    """
    Verify the initial data received from the client.

    - **init_data**: The raw data to verify.
    - **db**: Database session dependency, automatically provided by FastAPI.

    Returns a redirect URL based on whether the user exists or is newly created.
    """
    # Parse initDataRaw into a dictionary
    params = dict(x.split('=', 1) for x in init_data.initDataRaw.split('&'))

    # Decode the 'user' field from URL encoding
    params['user'] = urllib.parse.unquote(params.get('user', ''))

    # Extract and decode user data
    user_data_str = params.get('user', '')
    try:
        user_data_str = urllib.parse.unquote(user_data_str)  # URL-decode the user data string
        user_data = json.loads(user_data_str) if user_data_str else {}  # Parse JSON data
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid user data format")

    # Create the data_check_string for HMAC validation
    data_check_string = '\n'.join(f"{key}={value}" for key, value in sorted(params.items()) if key != "hash")
    
    # Create the secret key for HMAC
    secret_key = f"{bot_token}WebAppData".encode()

    # Generate the HMAC hash for validation
    calculated_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    # Compare the calculated hash with the provided hash
    if calculated_hash != params.get("hash", ""):
        raise HTTPException(status_code=400, detail="Invalid hash")

    # Check if the user exists in the database
    existing_user = await get_user_by_tID(db, user_data.get('id'))
    
    if existing_user:
        # If user exists, return redirect to the profile page
        print({"message": "Data verified successfully", "user": params["user"]})
        return {"redirect": "/profile"}
    else:
        # If user does not exist, create the user and return redirect to choose role page
        user_data = UserCreate(**user_data)  # Create a UserCreate schema instance
        await create_user(db, user_data)  # Create the user in the database
        return {"user_data": user_data, "redirect": "/choose-role"}

    # # Uncomment if needed to validate auth_date for outdated data
    # # current_time = int(time.time())
    # # if current_time - int(params["auth_date"]) > 86400:  # Check if it's older than 24 hours
    # #     raise HTTPException(status_code=400, detail="Outdated data")
