# scr/users/users_service.py
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import models

class UserCreateInput(BaseModel):
    username: str
    email: str
    password: str

def create_user(db: Session, create_user_dto: UserCreateInput):
    db_user = models.User(**create_user_dto.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Rest of the code remains unchanged

# scr/users/users_service.py
from sqlalchemy.orm import Session
from . import models

def create_user(db: Session, create_user_dto: UserCreateInput):
    db_user = models.User(**create_user_dto.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def update_user(db: Session, email: str, update_user_dto: UserCreateInput):
    db_user = get_user_by_email(db, email)
    for field, value in update_user_dto.dict().items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, email: str):
    db_user = get_user_by_email(db, email)
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

