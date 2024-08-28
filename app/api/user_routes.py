# Standard Library Imports
import hashlib  # For hashing functions
import hmac  # For HMAC (hash-based message authentication code)
import json  # For JSON parsing
import urllib.parse  # For URL parsing and decoding

# Third-Party Imports
from fastapi import APIRouter, HTTPException, Depends, Request, status  # FastAPI components for routing and error handling
from pydantic import BaseModel  # Pydantic for data validation
from sqlalchemy.ext.asyncio import AsyncSession  # SQLAlchemy for asynchronous database operations

# Local Application Imports
from app.schemas import UserCreate, User, RoleSelection  # User data validation schema
from app.crud import get_user_by_tID, create_user, delete_user_by_id, assign_initial_quests  # CRUD operations
from app.database import get_db  # Database session dependency

from dotenv import load_dotenv  # For loading environment variables from .env file
import os  # For accessing environment variables

# Load environment variables from .env file
load_dotenv()

# Access environment variables using os.getenv
bot_token = os.getenv("BOT_TOKEN")  # Retrieve the bot token from environment variables

from app.utils.validate import validate_init_data

router = APIRouter()  # Create an APIRouter instance for handling routes

# Endpoint to verify initial data and handle user authentication
@router.get("/users")
async def verify_init_data(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Verify the initial data received from the client.

    - **request**: The incoming request containing headers.
    - **db**: Database session dependency, automatically provided by FastAPI.

    Returns a redirect URL based on whether the user exists or is newly created.
    """

    # Extract Authorization header
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("tma "):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization header missing or improperly formatted"
        )
    
    # Extract initDataRaw from the header (after "tma ")
    init_data_raw = auth_header[len("tma "):]

    # Validate the initial data (separate logic)
    params = validate_init_data(init_data_raw, bot_token)

    # Extract user data after validation
    user_data_str = params.get('user', '')
    user_data = json.loads(user_data_str) if user_data_str else {}

    # Map the received field names to the model's expected names if needed
    user_data['telegram_id'] = user_data.pop('id')
    user_data['is_premium'] = False
    user_data['user_class'] = 'Mage'


    # Check if the user exists in the database
    existing_user = await get_user_by_tID(db, user_data.get('telegram_id'))
    if existing_user:
        return {"user": existing_user, "redirect": "/profile", "message": "User already exists, user data from db"}
    else:
        return {"redirect": "/choose-role", "message": "Please choose a role to complete your registration."}


@router.post("/users")
async def create_user_after_role_selection(
    role_selection: RoleSelection,  # Extracting the role from the request body
    request: Request,  # Retrieving user data from the Authorization header
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user after the role has been selected.

    - **role_selection**: The data containing the selected role (received from the request body).
    - **request**: The incoming request containing headers.
    - **db**: Database session dependency, automatically provided by FastAPI.

    Returns the created user and redirects to the profile page.
    """

    # Extract Authorization header
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("tma "):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization header missing or improperly formatted"
        )
    
    # Extract initDataRaw from the header (after "tma ")
    init_data_raw = auth_header[len("tma "):]

    # Validate the initial data (separate logic)
    params = validate_init_data(init_data_raw, bot_token)

    # Extract user data after validation
    user_data_str = params.get('user', '')
    user_data = json.loads(user_data_str) if user_data_str else {}

    # Map the received field names to the model's expected names if needed
    user_data['telegram_id'] = user_data.pop('id')
    user_data['is_premium'] = False
    user_data['user_class'] = 'Mage'

    # Add the selected role to the user data
    user_data['role'] = role_selection.role


    # Check if the user exists in the database
    existing_user = await get_user_by_tID(db, user_data.get('telegram_id'))
    if existing_user:
        return {"user": existing_user, "redirect": "/profile", "message": "User already exists, preventing multiple user creation!"}
    else:
        # Create the new user with the selected role
        new_user = await create_user(db, UserCreate(**user_data))
  
        await assign_initial_quests(db, new_user.id)
    
        return {"user": new_user, "redirect": "/profile", "message": "User created successfully with selected role. Initial quests has been asigned."}


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
