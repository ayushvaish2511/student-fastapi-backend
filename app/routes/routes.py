from fastapi import APIRouter, HTTPException, Query, Path, status, Response
from pydantic import BaseModel

from app.database.connection import startup_db_client
from app.models.Student import Student
import logging
from fastapi.encoders import jsonable_encoder
from bson import ObjectId  

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/students/", status_code=201)
async def create_student(student: Student):
    
    db = await startup_db_client()

    
    student_collection = db.get_collection("students")
    if db is None:
        raise HTTPException(status_code=500, detail="Failed to connect to database")

    try:
        result = await student_collection.insert_one(student.dict())
        if result.inserted_id:
            return {"id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Failed to create student")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating student: {e}")


@router.get("/students/")
async def list_students(country: str = Query(None, description="Filter by country"),
                        age: int = Query(None, description="Filter by age")):
    """
    Endpoint to list students with optional filters.
    """
    try:
        db = await startup_db_client()
        student_collection = db.get_collection("students")

        filter_params = {}
        if country:
            filter_params["country"] = country
        if age is not None:
            filter_params["age"] = {"$gte": age}

        students_cursor = student_collection.find(filter_params)
        students = await students_cursor.to_list(None)

        students_data = [{"name": student["name"], "age": student["age"]} for student in students]

        return {"data": students_data}
    except Exception as e:
        logger.error(f"Error listing students: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/students/{id}")
async def get_student(id: str = Path(..., description="The ID of the student previously created")):
    """
    Endpoint to fetch a student by ID.
    """
    try:
        db = await startup_db_client()
        student_collection = db.get_collection("students")

        student = await student_collection.find_one({"_id": ObjectId(id)})

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        response_data = {
            "name": student["name"],
            "age": student["age"],
            "address": student["address"]
        }

        return response_data
    except Exception as e:
        logger.error(f"Error fetching student: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.patch("/students/{id}")
async def update_student(
    student_update: Student,
    id: str = Path(..., description="The ID of the student to update")
):
    """
    Endpoint to update a student's properties based on information provided.
    """
    try:
        db = await startup_db_client()
        student_collection = db.get_collection("students")

        student = await student_collection.find_one({"_id": ObjectId(id)})

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        update_data = {k: v for k, v in student_update.dict().items() if v is not None}
        await student_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error updating student: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@router.delete("/students/{id}")
async def delete_student(id: str = Path(..., description="The ID of the student to delete")):
    """
    Endpoint to delete a student based on the provided ID.
    """
    try:
        db = await startup_db_client()
        student_collection = db.get_collection("students")

        result = await student_collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {}
    except Exception as e:
        logger.error(f"Error deleting student: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

