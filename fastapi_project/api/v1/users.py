from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from fastapi_project.db.database import (
    get_db,
)
from fastapi_project.schemas.users import (
    User,
)


router = APIRouter(prefix="/api/v1/users")

users = []

@router.get("", response_model=list[User])
async def get_users(db=Depends(get_db)):
    return users

@router.post("", response_model=User)
async def create_user(user: User, db=Depends(get_db)):
    users.append(user)
    return user

@router.put("/{id}", response_model=User)
async def update_user(id: int, updated: User, db=Depends(get_db)):
    for i, user in enumerate(users):
        if user.id == id:
            users[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{id}", response_model=User)
async def delete_user(id: int, db=Depends(get_db)):
    for i, user in enumerate(users):
        if user.id == id:
            users.pop(i)
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/{id}", response_model=User)
async def get_user(id: int, db=Depends(get_db)):
    for i, user in enumerate(users):
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

