from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel

from app.database.connection import startup_db_client
from app.models.Student import Student
# from database.connection import startup_db_client
# from models.Student import Student, Address
# from database.connection import startup_db_client
import logging
from fastapi.encoders import jsonable_encoder
from bson import ObjectId  # Import ObjectId from bson

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/students/", status_code=201, tags=["Students"])
async def create_student(student: Student):
    """
    Endpoint to create a student in the system.
    """
    # Connect to MongoDB
    db = await startup_db_client()

    # if db is not None:
    #     print('yess')
    #     print(db)
    student_collection = db.get_collection("students")
    # print(student_collection)
    # Check if the connection to the database was successful
    if db is None:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        # Insert the student data into the database
        result = await student_collection.insert_one(student.dict())
        if result.inserted_id:
            # Return the ID of the newly created student record
            return {"id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Failed to create student")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating student: {e}")


@router.get("/students/", tags=["Students"])
async def list_students(country: str = Query(None, description="Filter by country"),
                        age: int = Query(None, description="Filter by age")):
    """
    Endpoint to list students with optional filters.
    """
    try:
        # Connect to MongoDB
        db = await startup_db_client()
        student_collection = db.get_collection("students")

        # Construct filter based on query parameters
        filter_params = {}
        if country:
            filter_params["country"] = country
        if age is not None:
            filter_params["age"] = {"$gte": age}

        # Retrieve students based on filter
        students_cursor = student_collection.find(filter_params)
        students = await students_cursor.to_list(None)

        # Convert MongoDB documents to dictionaries and exclude _id and address fields
        students_data = [{"name": student["name"], "age": student["age"]} for student in students]

        return {"data": students_data}
    except Exception as e:
        logger.error(f"Error listing students: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/students/{id}", tags=["Students"])
async def get_student(id: str = Path(..., description="The ID of the student previously created")):
    """
    Endpoint to fetch a student by ID.
    """
    try:
        # Connect to MongoDB
        db = await startup_db_client()
        student_collection = db.get_collection("students")

        # Find student by ID
        student = await student_collection.find_one({"_id": ObjectId(id)})

        # If student not found, raise HTTPException with status code 404
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Prepare response in the specified format
        response_data = {
            "name": student["name"],
            "age": student["age"],
            "address": student["address"]
        }

        return response_data
    except Exception as e:
        logger.error(f"Error fetching student: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/students/{id}", tags=["Students"])
async def update_student(id: str, student: Student):
    """
    Endpoint to update a student by ID.
    """
    # Connect to MongoDB
    db = await startup_db_client()
    student_collection = db.get_collection("students")
    # Check if the connection to the database was successful
    if db is None:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        # Update the student in the database by ID
        result = await student_collection.update_one({"_id": id}, {"$set": student.dict()})
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
    student_collection = db.get_collection("students")
    # Check if the connection to the database was successful
    if db is None:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        # Delete the student from the database by ID
        result = await student_collection.delete_one({"_id": id})
        if result.deleted_count == 1:
            return {"message": "Student deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting student: {e}")
