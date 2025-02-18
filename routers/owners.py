from datetime import datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from starlette import status
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Owners

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

class OwnerRequest(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    date_created: Optional[datetime] = None
    date_modified: Optional[datetime] = None

# Create new owner
@router.post("/owners", status_code=status.HTTP_201_CREATED)
async def create_owner(db: db_dependency, owner_request: OwnerRequest):
    owner_model = Owners(**owner_request.model_dump())
    
    db.add(owner_model)
    db.commit()

# Read all owners
@router.get("/owners", status_code=status.HTTP_200_OK)
async def read_all_owners(db: db_dependency):
    owner_model = db.query(Owners).all()
    
    if not owner_model:
        raise HTTPException(status_code=404, detail='Owners not found.')
    
    return owner_model

# Find owners the user created on particular date
@router.get("/owners/by-date", status_code=status.HTTP_200_OK)
async def find_owner_by_date_created(db: db_dependency, date_created: datetime = Query(...)):
    
    start_datetime = datetime.combine(date_created, datetime.min.time())
    end_datetime = datetime.combine(date_created, datetime.max.time())
    
    owner_model = db.query(Owners).filter(Owners.date_created >= start_datetime, Owners.date_created <= end_datetime).all()
    
    if not owner_model:
        raise HTTPException(status_code=404, detail='Owner not found.')
    
    return owner_model

    
