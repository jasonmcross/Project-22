# scr/users/users_model.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import users_service, database_module

router = APIRouter()

@router.post("/")
async def create_user(create_user_dto: users_service.UserCreateInput, db: Session = Depends(database_module.get_db)):
    return users_service.create_user(db, create_user_dto)

@router.get("/")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database_module.get_db)):
    return users_service.get_users(db, skip=skip, limit=limit)

@router.get("/{email}")
async def read_user(email: str, db: Session = Depends(database_module.get_db)):
    return users_service.get_user_by_email(db, email)

@router.patch("/{email}")
async def update_user(email: str, update_user_dto: users_service.UserCreateInput, db: Session = Depends(database_module.get_db)):
    return users_service.update_user(db, email, update_user_dto)

@router.delete("/{email}")
async def delete_user(email: str, db: Session = Depends(database_module.get_db)):
    return users_service.delete_user(db, email)


