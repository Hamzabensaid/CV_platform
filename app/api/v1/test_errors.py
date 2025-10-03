from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/test", tags=["Test Errors"])

@router.get("/http")
async def http_error():
    raise HTTPException(status_code=404, detail="CV not found")

@router.get("/validation")
async def validation_error(age: int):
    return {"age": age}   # If you pass ?age=abc it will trigger 422

@router.get("/value")
async def value_error():
    raise ValueError("Something went wrong")

@router.get("/key")
async def key_error():
    data = {"name": "Hamza"}
    return data["age"]   # This will trigger KeyError

@router.get("/crash")
async def crash():
    1 / 0   # ZeroDivisionError
