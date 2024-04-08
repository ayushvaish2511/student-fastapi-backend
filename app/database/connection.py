
from motor.motor_asyncio import AsyncIOMotorClient

import urllib.parse




async def startup_db_client():
    """
    Connects to MongoDB using an async client and sets up the database connection.
    """
    try:
        username = urllib.parse.quote_plus('klsayushvaish')
        password = urllib.parse.quote_plus('Admin@123')

        uri = f"mongodb+srv://{username}:{password}@studentfastapidb.senyoch.mongodb.net/?retryWrites=true&w=majority&appName=studentFastAPIDB"

        db_client = AsyncIOMotorClient(uri)
        db = db_client['studentsDB']

        print("Successfully connected to MongoDB!")
        return db

    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise  




