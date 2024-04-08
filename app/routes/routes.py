from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.connection import startup_db_client
from app.models.Student import Student
# from database.connection import startup_db_client
# from models.Student import Student, Address
# from database.connection import startup_db_client


router = APIRouter()

@router.post("/students/", status_code=201, tags=["Students"])
async def create_student(student: Student):
    """
    Endpoint to create a student in the system.
    """
    # Connect to MongoDB
    db = await startup_db_client()

    if db is not None:
        print('yess')
        print(db)
    
    # Check if the connection to the database was successful
    if db is None:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        # Insert the student data into the database
        result = await db["studentsDB.studentFast"].insert_one(student.dict())
        if result.inserted_id:
            # Return the ID of the newly created student record
            return {"id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Failed to create student")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating student: {e}")

@router.get("/students/", tags=["Students"])
async def list_students():
    """
    Endpoint to list all students.
    """
    # Connect to MongoDB
    db = await startup_db_client()
    
    # Check if the connection to the database was successful
    if db is None:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        # Retrieve all students from the database
        students = await db["studentsDB.studentFast"].find().to_list(length=None)
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing students: {e}")

@router.get("/students/{id}", tags=["Students"])
async def fetch_student(id: str):
    """
    Endpoint to fetch a student by ID.
    """
    # Connect to MongoDB
    db = await startup_db_client()
    
    # Check if the connection to the database was successful
    if db is None:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        # Retrieve the student from the database by ID
        student = await db["students"].find_one({"_id": id})
        if student:
            return student
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching student: {e}")

@router.patch("/students/{id}", tags=["Students"])
async def update_student(id: str, student: Student):
    """
    Endpoint to update a student by ID.
    """
    # Connect to MongoDB
    db = await startup_db_client()
    
    # Check if the connection to the database was successful
    if db is None:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        # Update the student in the database by ID
        result = await db["students"].update_one({"_id": id}, {"$set": student.dict()})
        if result.modified_count == 1:
            return {"message": "Student updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating student: {e}")

@router.delete("/students/{id}", tags=["Students"])
async def delete_student(id: str):
    """
    Endpoint to delete a student by ID.
    """
    # Connect to MongoDB
    db = await startup_db_client()
    
    # Check if the connection to the database was successful
    if db is None:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        # Delete the student from the database by ID
        result = await db["students"].delete_one({"_id": id})
        if result.deleted_count == 1:
            return {"message": "Student deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting student: {e}")
