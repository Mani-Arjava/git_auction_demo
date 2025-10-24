from fastapi import APIRouter

router = APIRouter()

@router.get("/getall", tags=["test"])
async def get_all():
    return {"message": "hello world"}