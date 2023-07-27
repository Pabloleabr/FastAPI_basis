from fastapi import APIRouter, HTTPException, Response
from models.todos import Todo
from config.dabase import collection
from schema.schemas import list_serial, indivial_serializer
from bson import ObjectId, errors #for mongodB to identify the ID

router = APIRouter()

# Handles Invalid ObjectIds  
def handle_invalid_id_exception(exc: errors.InvalidId):
    error_msg = str(exc)
    raise HTTPException(status_code=400, detail=error_msg)

# makes sure the id is valid
def check_id(id:str):
    try:
        # Convert the received item_id to an ObjectId
        object_id = ObjectId(id)
        return object_id
    except errors.InvalidId as e:
        # Catch InvalidId error and handle it using the registered exception handler
        return handle_invalid_id_exception(e)

# GET ALL request methoid
@router.get("/")
async def get_todos():
    todos = list_serial(collection.find())
    return todos

# GET request methoid
@router.get("/{id}")
async def get_todo(id: str):
    confirmed_id = check_id(id)
    todo = collection.find_one({"_id": confirmed_id})
    if(todo):
        return indivial_serializer(todo)
    else:
        raise HTTPException(status_code=404, detail=f"Todo with id:'{id}' not found")


# POST request methoid
@router.post("/")
async def insert(todo: Todo):
    inserted = collection.insert_one(dict(todo)).inserted_id
    return inserted

# PUT request method
@router.put("/{id}")
async def update_todo(id: str, todo: Todo,): 
    confirmed_id = check_id(id)
    todo = collection.find_one_and_update({"_id": confirmed_id}, {"$set": dict(todo)})
    if(todo):
        return Response("Todo updated correctly")
    else:
        raise HTTPException(status_code=404, detail=f"Todo with id:'{id}' not found")

# DELETE request method
@router.delete("/{id}")
async def delete_todo(id: str): 
    confirmed_id = check_id(id)
    todo = collection.find_one_and_delete({"_id": ObjectId(confirmed_id)})
    if(todo):
        return Response("Todo deleted")
    else:
        raise HTTPException(status_code=404, detail=f"Todo with id:'{id}' not found")
    