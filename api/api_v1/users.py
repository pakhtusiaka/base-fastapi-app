from fastapi import APIRouter


router = APIRouter(
    tags=["User"],
)

@router.get("/users")
async def get_users():
    pass