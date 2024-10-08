from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.user_routes import router as usesr_router
from app.api.quest_routes import router as quest_router

# Create an instance of the FastAPI application
app = FastAPI()

# Add CORS (Cross-Origin Resource Sharing) middleware to allow requests from the specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify the frontend origin allowed to make requests to the backend
    allow_credentials=True,  # Allow cookies and credentials to be included in requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers in requests
)

# Include the user routes from the user_routes module under the /api prefix with the tag "users"
app.include_router(usesr_router, prefix="/api", tags=["users"])

# Include the quest routes from the quest_routes module under the /api prefix with the tag "quests"
app.include_router(quest_router, prefix="/api", tags=["quests"])  # Include quest routes
