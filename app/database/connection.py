import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

import urllib.parse

async def startup_db_client():
    """
    Connects to MongoDB using an async client and sets up the database connection.
    """
    try:
        # Escape username and password
        username = urllib.parse.quote_plus('klsayushvaish')
        password = urllib.parse.quote_plus('Admin@123')

        # Construct the connection URI with escaped username and password
        uri = f"mongodb+srv://{username}:{password}@studentfastapidb.senyoch.mongodb.net/?retryWrites=true&w=majority&appName=studentFastAPIDB"

        # Connect to MongoDB
        db_client = AsyncIOMotorClient(uri)
        db = db_client['studentsDB']

        print("Successfully connected to MongoDB!")
        return db
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise  


# async def test_connection():
#     """
#     Tests the database connection.
#     """
#     db = await startup_db_client()
#     if db is not None:
#         # Perform some test queries or operations here
#         # For example:
#         # result = await db.some_collection.find_one({})
#         # print(result)
#         print("Connection test successful.")
#     else:
#         print("Connection test failed.")

# # Run the test function
# asyncio.run(test_connection())


